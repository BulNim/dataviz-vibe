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
df["거래일시"] = pd.to_datetime(df["거래일시"], format="mixed")
df["연월"] = df["거래일시"].dt.to_period("M").astype(str)

# 업종별 총 거래금액 상위 3개를 뽑음 - 전체 업종을 다 그리면 선이 겹쳐 알아보기 힘드므로
# 매출 기여도가 큰 업종만 골라 추이를 비교함
top3 = df.groupby("가맹점업종")["거래금액"].sum().sort_values(ascending=False).head(3).index.tolist()
print("업종 합계 상위 3개:", top3)

monthly = df[df["가맹점업종"].isin(top3)].pivot_table(
    index="연월", columns="가맹점업종", values="거래금액", aggfunc="sum"
).sort_index()

colors = ["#C0392B", "#D9822B", "#F0C078"]

fig, ax = plt.subplots(figsize=(11, 6))
for cat, color in zip(top3, colors):
    ax.plot(monthly.index, monthly[cat], marker="o", linewidth=2, label=cat, color=color)

ax.set_title("업종별 월별 거래금액 추이 (상위 3개 업종)", fontsize=18, fontweight="bold")
ax.set_xlabel("연월", fontsize=14, fontweight="bold")
ax.set_ylabel("거래금액 (원)", fontsize=14, fontweight="bold")
ax.tick_params(axis="x", rotation=45, labelsize=11)
ax.tick_params(axis="y", labelsize=12)
ax.yaxis.set_major_formatter(FuncFormatter(lambda x, _: f"{x:,.0f}"))
ax.grid(axis="y", linestyle="--", alpha=0.4, zorder=0)
ax.set_axisbelow(True)
ax.legend(fontsize=12)

fig.tight_layout()

os.makedirs("output/charts", exist_ok=True)
fig.savefig("output/charts/상위업종_월별_거래금액_추이.png", dpi=150)
print("저장 완료: output/charts/상위업종_월별_거래금액_추이.png")

plt.show()
