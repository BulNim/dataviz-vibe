import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl

mpl.rcParams["font.family"] = "Malgun Gothic"
mpl.rcParams["axes.unicode_minus"] = False

df = pd.read_csv("data/핀테크_정제완료.csv", encoding="utf-8-sig")

grouped = df.groupby("가맹점업종")["거래금액"].sum().sort_values(ascending=True)

fig, ax = plt.subplots(figsize=(9, 6))
bars = ax.barh(grouped.index, grouped.values, color="#4C72B0")
ax.set_title("업종별 총 거래금액 (큰 순서)")
ax.set_xlabel("총 거래금액 (원)")
ax.set_ylabel("가맹점업종")

for bar in bars:
    width = bar.get_width()
    ax.annotate(f"{width:,.0f}원", xy=(width, bar.get_y() + bar.get_height() / 2),
                xytext=(5, 0), textcoords="offset points", ha="left", va="center", fontsize=9)

ax.margins(x=0.18)
fig.tight_layout()

plt.show()
