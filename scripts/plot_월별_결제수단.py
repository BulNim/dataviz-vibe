import os
os.chdir(os.path.dirname(os.path.abspath(__file__)) + "/..")

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl

mpl.rcParams["font.family"] = "Malgun Gothic"
mpl.rcParams["axes.unicode_minus"] = False
mpl.rcParams["font.size"] = 13

df = pd.read_csv("data/핀테크_정제완료.csv", encoding="utf-8-sig")
df["거래일시"] = pd.to_datetime(df["거래일시"], format="mixed")
df["연월"] = df["거래일시"].dt.to_period("M").astype(str)

os.makedirs("output/charts", exist_ok=True)

# ---------- 1) 월별 거래금액 합계 - 선 그래프 ----------
monthly = df.groupby("연월")["거래금액"].sum().sort_index()

fig1, ax1 = plt.subplots(figsize=(10, 6))
ax1.plot(monthly.index, monthly.values, marker="o", color="#D9822B", linewidth=2)
ax1.set_title("월별 거래금액 합계", fontsize=18, fontweight="bold")
ax1.set_xlabel("연월", fontsize=14, fontweight="bold")
ax1.set_ylabel("총 거래금액 (원)", fontsize=14, fontweight="bold")
ax1.tick_params(axis="x", rotation=45, labelsize=11)
ax1.tick_params(axis="y", labelsize=12)
ax1.grid(axis="y", linestyle="--", alpha=0.4)

for x, y in zip(monthly.index, monthly.values):
    ax1.annotate(f"{y:,.0f}", xy=(x, y), xytext=(0, 6), textcoords="offset points",
                 ha="center", fontsize=8)

fig1.tight_layout()
fig1.savefig("output/charts/월별_거래금액_추이.png", dpi=150)
print("저장 완료: output/charts/월별_거래금액_추이.png")

# ---------- 2) 결제수단별 거래금액 비중 - 도넛 차트 ----------
pay = df.groupby("결제수단")["거래금액"].sum().sort_values(ascending=False)
pct = pay / pay.sum() * 100

fig2, ax2 = plt.subplots(figsize=(8, 8))
colors = plt.cm.Oranges_r([i / len(pay) * 0.7 for i in range(len(pay))])
wedges, texts, autotexts = ax2.pie(
    pay.values, labels=pay.index, autopct="%.1f%%", startangle=90,
    pctdistance=0.8, colors=colors,
    wedgeprops=dict(width=0.4, edgecolor="white"),
    textprops=dict(fontsize=12, fontweight="bold"),
)
ax2.set_title("결제수단별 거래금액 비중", fontsize=18, fontweight="bold")
ax2.axis("equal")

fig2.tight_layout()
fig2.savefig("output/charts/결제수단별_금액비중.png", dpi=150)
print("저장 완료: output/charts/결제수단별_금액비중.png")

plt.show()
