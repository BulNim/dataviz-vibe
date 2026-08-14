import os
os.chdir(os.path.dirname(os.path.abspath(__file__)) + "/..")

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.ticker import FuncFormatter

mpl.rcParams["font.family"] = "Malgun Gothic"
mpl.rcParams["axes.unicode_minus"] = False
mpl.rcParams["font.size"] = 13

df = pd.read_csv("data/핀테크_정제완료.csv", encoding="utf-8-sig")

# 20만원 미만 거래만 골라냄 - 소액~중액 구간의 실제 분포 모양을 보려면
# 고액 이상치가 섞인 전체 범위보다 이렇게 구간을 좁혀야 막대가 눌리지 않고 잘 보임
before = len(df)
df_sub = df[df["거래금액"] < 200000]
print(f"전체 {before}건 중 20만원 미만: {len(df_sub)}건 ({len(df_sub)/before*100:.1f}%)")

fig, ax = plt.subplots(figsize=(16, 7))
counts, edges, patches = ax.hist(df_sub["거래금액"], bins=40, color="#E08E45", edgecolor="white")
ax.set_title("거래금액 히스토그램 (20만원 미만, 40구간)", fontsize=18, fontweight="bold")
ax.set_xlabel("거래금액 (원)", fontsize=14, fontweight="bold")
ax.set_ylabel("거래 건수", fontsize=14, fontweight="bold")
ax.tick_params(axis="x", labelsize=11)
ax.tick_params(axis="y", labelsize=12)
ax.xaxis.set_major_formatter(FuncFormatter(lambda x, _: f"{x:,.0f}"))
ax.grid(axis="y", linestyle="--", alpha=0.4, zorder=0)
ax.set_axisbelow(True)

# 막대 40개 위에 정확한 건수를 다 적으면 서로 겹치므로, 세로로 회전시켜 작은 글씨로 표시
bin_centers = (edges[:-1] + edges[1:]) / 2
for x, y in zip(bin_centers, counts):
    if y > 0:
        ax.annotate(f"{y:,.0f}", xy=(x, y), xytext=(0, 3), textcoords="offset points",
                    ha="center", va="bottom", fontsize=7, rotation=90)

ax.margins(y=0.18)
fig.tight_layout()

os.makedirs("output/charts", exist_ok=True)
fig.savefig("output/charts/거래금액_히스토그램_20만원미만.png", dpi=150)
print("저장 완료: output/charts/거래금액_히스토그램_20만원미만.png")

plt.show()
