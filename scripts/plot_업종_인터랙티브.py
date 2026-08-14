import os
os.chdir(os.path.dirname(os.path.abspath(__file__)) + "/..")

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.ticker import FuncFormatter
import mplcursors  # 마우스를 막대 위에 올리면 값이 뜨는 툴팁 기능 - pip install mplcursors 필요

mpl.rcParams["font.family"] = "Malgun Gothic"
mpl.rcParams["axes.unicode_minus"] = False
mpl.rcParams["font.size"] = 13

df = pd.read_csv("data/핀테크_정제완료.csv", encoding="utf-8-sig")

grouped = df.groupby("가맹점업종")["거래금액"].sum().sort_values(ascending=False)

fig, ax = plt.subplots(figsize=(10, 6))
bars = ax.bar(grouped.index, grouped.values, color="#E08E45")
ax.set_title("업종별 총 거래금액 (마우스를 올리면 값 표시)", fontsize=16, fontweight="bold")
ax.set_xlabel("가맹점업종", fontsize=14, fontweight="bold")
ax.set_ylabel("총 거래금액 (원)", fontsize=14, fontweight="bold")
ax.tick_params(axis="x", rotation=30, labelsize=12)
ax.tick_params(axis="y", labelsize=12)
ax.yaxis.set_major_formatter(FuncFormatter(lambda x, _: f"{x:,.0f}"))
ax.grid(axis="y", linestyle="--", alpha=0.4, zorder=0)
ax.set_axisbelow(True)

fig.tight_layout()

# 막대(bars)에 커서를 올리면 해당 업종명과 정확한 금액을 말풍선으로 보여줌
cursor = mplcursors.cursor(bars, hover=True)


@cursor.connect("add")
def on_hover(sel):
    idx = sel.index
    cat = grouped.index[idx]
    val = grouped.values[idx]
    sel.annotation.set_text(f"{cat}\n{val:,.0f}원")


plt.show()
