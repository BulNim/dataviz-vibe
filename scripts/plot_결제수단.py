import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl

mpl.rcParams["font.family"] = "Malgun Gothic"
mpl.rcParams["axes.unicode_minus"] = False
mpl.rcParams["font.size"] = 13

df = pd.read_csv("data/01_핀테크결제_dirty.csv", encoding="utf-8-sig")

# 공백 오염(' 신용카드' 등) 정리 후 집계 - 안 하면 같은 결제수단이 다른 카테고리로 갈라져 비율이 왜곡됨
df["결제수단"] = df["결제수단"].astype(str).str.strip()
df.loc[df["결제수단"] == "nan", "결제수단"] = pd.NA

counts = df["결제수단"].value_counts(dropna=True).sort_values(ascending=False)
pct = counts / counts.sum() * 100

fig, ax = plt.subplots(figsize=(10, 6))
bars = ax.bar(counts.index, counts.values, color="#E08E45")
ax.set_title("결제수단별 거래 건수 및 비율", fontsize=18, fontweight="bold")
ax.set_xlabel("결제수단", fontsize=14, fontweight="bold")
ax.set_ylabel("거래 건수", fontsize=14, fontweight="bold")
ax.tick_params(axis="x", labelsize=12)
ax.tick_params(axis="y", labelsize=12)
ax.grid(axis="y", linestyle="--", alpha=0.4, zorder=0)
ax.set_axisbelow(True)

for bar, p in zip(bars, pct):
    height = bar.get_height()
    ax.annotate(f"{height:,}건\n({p:.1f}%)", xy=(bar.get_x() + bar.get_width() / 2, height),
                xytext=(0, 4), textcoords="offset points", ha="center", va="bottom",
                fontsize=11, fontweight="bold")

ax.margins(y=0.15)
fig.tight_layout()

os.makedirs("output/charts", exist_ok=True)
fig.savefig("output/charts/결제수단별_건수_비율.png", dpi=150)
print("저장 완료: output/charts/결제수단별_건수_비율.png")

plt.show()
