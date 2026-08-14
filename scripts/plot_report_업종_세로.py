import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.ticker import FuncFormatter

mpl.rcParams["font.family"] = "Malgun Gothic"
mpl.rcParams["axes.unicode_minus"] = False
mpl.rcParams["font.size"] = 13

df = pd.read_csv("data/핀테크_정제완료.csv", encoding="utf-8-sig")

grouped = df.groupby("가맹점업종")["거래금액"].sum().sort_values(ascending=False)

colors = ["#C0392B"] + ["#F0A868"] * (len(grouped) - 1)

fig, ax = plt.subplots(figsize=(10, 6))
bars = ax.bar(grouped.index, grouped.values, color=colors)
ax.set_title("업종별 총 거래금액 (큰 순서)", fontsize=18, fontweight="bold")
ax.set_xlabel("가맹점업종", fontsize=14, fontweight="bold")
ax.set_ylabel("총 거래금액 (천원)", fontsize=14, fontweight="bold")
ax.tick_params(axis="x", rotation=30, labelsize=12)
ax.tick_params(axis="y", labelsize=12)

# 원 단위 그대로 쓰면 자릿수가 너무 길어(예: 126,354,008) 눈에 안 들어오므로
# 1000으로 나눈 천원 단위로 눈금·막대 라벨을 표시함. 배경 눈금선도 켜서 막대 높이를 눈으로 비교하기 쉽게 함
ax.yaxis.set_major_formatter(FuncFormatter(lambda x, _: f"{x/1000:,.0f}"))
ax.grid(axis="y", linestyle="--", alpha=0.4, zorder=0)
ax.set_axisbelow(True)

for bar in bars:
    height = bar.get_height()
    ax.annotate(f"{height/1000:,.0f}천원", xy=(bar.get_x() + bar.get_width() / 2, height),
                xytext=(0, 4), textcoords="offset points", ha="center", va="bottom",
                fontsize=11, fontweight="bold")

ax.margins(y=0.12)
fig.tight_layout()

os.makedirs("output/charts", exist_ok=True)
fig.savefig("output/charts/업종별_총거래금액.png", dpi=150)
print("저장 완료: output/charts/업종별_총거래금액.png")

plt.show()
