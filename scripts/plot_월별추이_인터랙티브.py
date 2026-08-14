import os
os.chdir(os.path.dirname(os.path.abspath(__file__)) + "/..")

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.ticker import FuncFormatter
import mplcursors

mpl.rcParams["font.family"] = "Malgun Gothic"
mpl.rcParams["axes.unicode_minus"] = False
mpl.rcParams["font.size"] = 13

df = pd.read_csv("data/핀테크_정제완료.csv", encoding="utf-8-sig")
df["거래일시"] = pd.to_datetime(df["거래일시"], format="mixed")
df["연월"] = df["거래일시"].dt.to_period("M").astype(str)

monthly = df.groupby("연월")["거래금액"].sum().sort_index()

fig, ax = plt.subplots(figsize=(11, 6))
line, = ax.plot(monthly.index, monthly.values, marker="o", markersize=8,
                 linewidth=2, color="#D9822B")
ax.set_title("월별 거래금액 합계 (마우스를 올리면 값 표시)", fontsize=16, fontweight="bold")
ax.set_xlabel("연월", fontsize=14, fontweight="bold")
ax.set_ylabel("거래금액 (원)", fontsize=14, fontweight="bold")
ax.tick_params(axis="x", rotation=45, labelsize=11)
ax.tick_params(axis="y", labelsize=12)
ax.yaxis.set_major_formatter(FuncFormatter(lambda x, _: f"{x:,.0f}"))
ax.grid(axis="y", linestyle="--", alpha=0.4, zorder=0)
ax.set_axisbelow(True)

fig.tight_layout()

# 점(마커)에 커서를 올리면 해당 연월과 정확한 금액을 말풍선으로 보여줌
cursor = mplcursors.cursor(line, hover=True)


@cursor.connect("add")
def on_hover(sel):
    idx = round(sel.index)
    month = monthly.index[idx]
    val = monthly.values[idx]
    sel.annotation.set_text(f"{month}\n{val:,.0f}원")


plt.show()
