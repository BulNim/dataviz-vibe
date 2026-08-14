import os
os.chdir(os.path.dirname(os.path.abspath(__file__)) + "/..")

import pandas as pd
import plotly.express as px

df = pd.read_csv("data/핀테크_정제완료.csv", encoding="utf-8-sig")

# 트리맵과 같은 계층(지역 -> 업종), 같은 값(거래금액 합계)을 원형(선버스트)으로 표현
# 안쪽 고리가 지역, 바깥쪽 고리가 업종 - 부채꼴 넓이가 클수록 거래금액이 큼
agg = df.groupby(["지역", "가맹점업종"], as_index=False)["거래금액"].sum()

fig = px.sunburst(
    agg,
    path=["지역", "가맹점업종"],
    values="거래금액",
    color="거래금액",
    color_continuous_scale="Oranges",
    title="지역 × 업종 거래금액 선버스트 (마우스를 올리면 값 표시)",
)
fig.update_traces(hovertemplate="%{label}<br>거래금액: %{value:,.0f}원<extra></extra>")
fig.update_layout(font=dict(family="Malgun Gothic", size=14))

os.makedirs("output/charts", exist_ok=True)
out_html = "output/charts/지역_업종_선버스트.html"
fig.write_html(out_html)
print(f"저장 완료: {out_html}")

fig.show()
