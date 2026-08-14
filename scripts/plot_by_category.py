import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl

mpl.rcParams["font.family"] = "Malgun Gothic"
mpl.rcParams["axes.unicode_minus"] = False

df = pd.read_csv("data/핀테크_정제완료.csv", encoding="utf-8-sig")

grouped = df.groupby("가맹점업종")["거래금액"].sum().sort_values(ascending=False)

fig, ax = plt.subplots(figsize=(10, 6))
bars = ax.bar(grouped.index, grouped.values, color="#4C72B0")
ax.set_title("가맹점업종별 총 거래금액")
ax.set_xlabel("가맹점업종")
ax.set_ylabel("총 거래금액 (원)")
ax.tick_params(axis="x", rotation=30)

for bar in bars:
    height = bar.get_height()
    ax.annotate(
        f"{height:,.0f}",
        xy=(bar.get_x() + bar.get_width() / 2, height),
        xytext=(0, 3),
        textcoords="offset points",
        ha="center",
        va="bottom",
        fontsize=9,
    )

ax.margins(y=0.1)
fig.tight_layout()

plt.show()
