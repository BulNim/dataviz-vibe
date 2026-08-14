import os
os.chdir(os.path.dirname(os.path.abspath(__file__)) + "/..")

import pandas as pd
import plotly.express as px

df = pd.read_csv("data/핀테크_정제완료.csv", encoding="utf-8-sig")

# 지역을 상위 계층, 업종을 하위 계층으로 두고 거래금액 합계로 사각형 크기를 정함
# 사각형이 클수록 거래금액이 크다는 뜻 - 계층형이라 지역 안에 업종별 사각형이 다시 쪼개져 보임
agg = df.groupby(["지역", "가맹점업종"], as_index=False)["거래금액"].sum()

fig = px.treemap(
    agg,
    path=["지역", "가맹점업종"],
    values="거래금액",
    color="거래금액",
    color_continuous_scale="Oranges",
    title="지역 × 업종 거래금액 트리맵 (마우스를 올리면 값 표시)",
)
# hover 시 천단위 콤마가 찍힌 원 단위 금액이 뜨도록 지정 - 기본값은 지수표기라 알아보기 어려움
fig.update_traces(hovertemplate="%{label}<br>거래금액: %{value:,.0f}원<extra></extra>")
fig.update_layout(font=dict(family="Malgun Gothic", size=14))

os.makedirs("output/charts", exist_ok=True)
out_html = "output/charts/지역_업종_트리맵.html"
fig.write_html(out_html)
print(f"저장 완료: {out_html}")

fig.show()
