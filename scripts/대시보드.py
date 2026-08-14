"""
핀테크 결제 데이터 대시보드.
왼쪽 사이드바에서 지역·업종·기간을 고르면, 그 조건에 맞는 데이터만 다시 집계해서
탭별로 나눈 화면(요약/업종/추이/결제수단/원본표)이 오른쪽에 다시 그려진다.
Streamlit은 위젯 값이 바뀔 때마다 스크립트 전체를 다시 실행하는 구조라서
"필터 -> 다시 계산 -> 다시 그리기"가 별도 콜백 없이 자연스럽게 동작한다.
차트는 plotly를 써서 확대·축소·마우스 hover 값 확인이 가능하게 함(matplotlib은 정적 이미지라 이런 조작이 안 됨).
"""
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)) + "/..")

import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="핀테크 결제 데이터 대시보드", layout="wide", page_icon="💳")

# 상단 KPI 카드 글씨를 기본보다 크게 - 요청한 대로 "위에는 총액이랑 건수, 평균, 고객 수 크게"
# 눈에 확 들어와야 하므로 st.metric 기본 폰트 크기를 CSS로 키움
st.markdown(
    """
    <style>
    div[data-testid="stMetricValue"] { font-size: 2.2rem; }
    div[data-testid="stMetricLabel"] { font-size: 1.05rem; }
    </style>
    """,
    unsafe_allow_html=True,
)


# 데이터 로딩 - st.cache_data 를 붙이면 필터를 바꿔도 CSV를 매번 다시 읽지 않고
# 캐시에서 꺼내 쓰므로 화면이 훨씬 빨리 갱신됨
@st.cache_data
def load_data():
    df = pd.read_csv("data/핀테크_정제완료.csv", encoding="utf-8-sig")
    df["거래일시"] = pd.to_datetime(df["거래일시"], format="mixed")
    df["연월"] = df["거래일시"].dt.to_period("M").astype(str)
    df["결제수단"] = df["결제수단"].astype(str).str.strip()  # ' 신용카드' 같은 공백 오염 정리
    return df


df = load_data()

st.title("💳 핀테크 결제 데이터 대시보드")

# ---------- 사이드바 필터 ----------
st.sidebar.header("필터")

regions = sorted(df["지역"].unique().tolist())
categories = sorted(df["가맹점업종"].unique().tolist())
methods = sorted(df["결제수단"].unique().tolist())
months = sorted(df["연월"].unique().tolist())

selected_regions = st.sidebar.multiselect("지역 선택", regions, default=regions)
selected_categories = st.sidebar.multiselect("업종 선택", categories, default=categories)
selected_methods = st.sidebar.multiselect("결제수단 선택", methods, default=methods)

# 슬라이더로 기간(연월) 범위를 고를 수 있게 함 - 특정 구간만 보고 싶을 때 매번 날짜를 타이핑할 필요 없음
month_range = st.sidebar.select_slider(
    "기간(연월) 범위", options=months, value=(months[0], months[-1])
)

# 사이드바에서 조건을 다 고른 뒤 눌러야 화면이 갱신되게 함 - 지역·업종·수단·기간을 하나씩 바꿀 때마다
# 매번 다시 그리면 여러 항목을 연달아 고를 때 화면이 계속 깜빡여서 오히려 느리게 느껴짐
apply = st.sidebar.button("필터 적용", type="primary", use_container_width=True)

# 세션 상태에 마지막으로 적용된 필터를 저장해둠 - 버튼을 누르기 전까지는 이전 화면을 그대로 유지
if apply or "filters" not in st.session_state:
    st.session_state["filters"] = dict(
        regions=selected_regions, categories=selected_categories,
        methods=selected_methods, month_range=month_range,
    )

f = st.session_state["filters"]

if not f["regions"] or not f["categories"] or not f["methods"]:
    st.warning("지역·업종·결제수단을 최소 1개씩 선택해야 데이터가 표시됩니다.")
    st.stop()

df_filtered = df[
    df["지역"].isin(f["regions"])
    & df["가맹점업종"].isin(f["categories"])
    & df["결제수단"].isin(f["methods"])
    & df["연월"].between(f["month_range"][0], f["month_range"][1])
]

st.sidebar.markdown(f"**선택된 거래 건수: {len(df_filtered):,}건**")

if df_filtered.empty:
    st.info("선택한 조건에 해당하는 데이터가 없습니다. 필터를 조정해보세요.")
    st.stop()

# ---------- 상단 요약 지표 ----------
# 원 단위 그대로 쓰면 자릿수가 너무 길어서(예: 126,354,008원) 한눈에 안 들어오므로
# 1000으로 나눈 천원 단위로 표시함
col1, col2, col3, col4 = st.columns(4)
col1.metric("총 거래금액", f"{df_filtered['거래금액'].sum()/1000:,.0f}천원")
col2.metric("총 거래 건수", f"{len(df_filtered):,}건")
col3.metric("평균 거래금액", f"{df_filtered['거래금액'].mean()/1000:,.1f}천원")
col4.metric("고객 수", f"{df_filtered['사용자ID'].nunique():,}명")

st.divider()

# ---------- 탭으로 화면을 나눠서 스크롤 없이 원하는 내용만 골라보게 함 ----------
tab_trend, tab_compare, tab_detail = st.tabs(["추이", "비교", "상세"])

# ---------- 추이 : 시간축 흐름만 다루는 화면 ----------
with tab_trend:
    st.subheader("월별 거래금액 추이")
    monthly = df_filtered.groupby("연월")["거래금액"].sum().sort_index().reset_index()
    fig_trend = px.line(monthly, x="연월", y="거래금액", markers=True,
                         labels={"거래금액": "거래금액(원)"})
    fig_trend.update_traces(line_color="#D9822B", hovertemplate="%{x}<br>%{y:,.0f}원<extra></extra>")
    st.plotly_chart(fig_trend, use_container_width=True)

    st.subheader("월별 거래 건수 추이")
    monthly_cnt = df_filtered.groupby("연월").size().reset_index(name="건수")
    fig_trend_cnt = px.bar(monthly_cnt, x="연월", y="건수", color_discrete_sequence=["#F0A868"])
    fig_trend_cnt.update_traces(hovertemplate="%{x}<br>%{y:,}건<extra></extra>")
    st.plotly_chart(fig_trend_cnt, use_container_width=True)

# ---------- 비교 : 카테고리끼리 나란히 놓고 크기를 비교하는 화면 ----------
with tab_compare:
    col_a, col_b = st.columns(2)

    with col_a:
        st.subheader("업종별 총 거래금액")
        cat_sum = df_filtered.groupby("가맹점업종")["거래금액"].sum().sort_values(ascending=False).reset_index()
        fig_cat = px.bar(cat_sum, x="가맹점업종", y="거래금액", color="거래금액",
                          color_continuous_scale="Oranges", labels={"거래금액": "거래금액(원)"})
        fig_cat.update_traces(hovertemplate="%{x}<br>%{y:,.0f}원<extra></extra>")
        st.plotly_chart(fig_cat, use_container_width=True)

    with col_b:
        st.subheader("결제수단별 거래금액 비중")
        pay_sum = df_filtered.groupby("결제수단")["거래금액"].sum().sort_values(ascending=False).reset_index()
        fig_pay = px.pie(pay_sum, names="결제수단", values="거래금액", hole=0.4,
                          color_discrete_sequence=px.colors.sequential.Oranges_r)
        fig_pay.update_traces(hovertemplate="%{label}<br>%{value:,.0f}원 (%{percent})<extra></extra>")
        st.plotly_chart(fig_pay, use_container_width=True)

    st.subheader("지역별 총 거래금액")
    region_sum = df_filtered.groupby("지역")["거래금액"].sum().sort_values(ascending=False).reset_index()
    fig_region = px.bar(region_sum, x="지역", y="거래금액", color="거래금액",
                         color_continuous_scale="Oranges", labels={"거래금액": "거래금액(원)"})
    fig_region.update_traces(hovertemplate="%{x}<br>%{y:,.0f}원<extra></extra>")
    st.plotly_chart(fig_region, use_container_width=True)

# ---------- 상세 : 교차 분석 + 원본 데이터를 파고드는 화면 ----------
with tab_detail:
    st.subheader("지역 × 업종 거래금액 트리맵")
    agg = df_filtered.groupby(["지역", "가맹점업종"], as_index=False)["거래금액"].sum()
    fig_tree = px.treemap(agg, path=["지역", "가맹점업종"], values="거래금액",
                           color="거래금액", color_continuous_scale="Oranges")
    fig_tree.update_traces(hovertemplate="%{label}<br>%{value:,.0f}원<extra></extra>")
    st.plotly_chart(fig_tree, use_container_width=True)

    st.subheader("원본 표")
    st.dataframe(df_filtered, use_container_width=True)
    # 필터링된 데이터를 그대로 CSV로 내려받을 수 있게 함 - 화면에서 본 조건 그대로 엑셀 등에서 추가 분석 가능
    csv_bytes = df_filtered.to_csv(index=False, encoding="utf-8-sig").encode("utf-8-sig")
    st.download_button(
        "필터링된 데이터 CSV 다운로드",
        data=csv_bytes,
        file_name="핀테크_필터링결과.csv",
        mime="text/csv",
        use_container_width=True,
    )
