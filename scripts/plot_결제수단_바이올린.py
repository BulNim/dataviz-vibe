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

# 공백 오염(' 신용카드' 등) 정리 - 안 하면 같은 결제수단이 다른 바이올린으로 갈라짐
df["결제수단"] = df["결제수단"].astype(str).str.strip()

# 20만원 미만만 사용 - 앞서 그린 히스토그램과 같은 기준으로 소액~중액 구간만 비교
df_sub = df[df["거래금액"] < 200000]

order = df_sub.groupby("결제수단")["거래금액"].median().sort_values(ascending=False).index.tolist()
data_by_method = [df_sub.loc[df_sub["결제수단"] == m, "거래금액"].values for m in order]

fig, ax = plt.subplots(figsize=(11, 7))
parts = ax.violinplot(data_by_method, showmedians=True, showextrema=True)

for body in parts["bodies"]:
    body.set_facecolor("#E08E45")
    body.set_edgecolor("#8B3A00")
    body.set_alpha(0.8)
parts["cmedians"].set_color("#8B3A00")
parts["cmedians"].set_linewidth(2)
parts["cmaxes"].set_color("#8B3A00")
parts["cmins"].set_color("#8B3A00")
parts["cbars"].set_color("#8B3A00")

ax.set_xticks(range(1, len(order) + 1))
ax.set_xticklabels(order, rotation=15)
ax.set_title("결제수단별 거래금액 분포 (20만원 미만, 바이올린)", fontsize=17, fontweight="bold")
ax.set_xlabel("결제수단", fontsize=14, fontweight="bold")
ax.set_ylabel("거래금액 (원)", fontsize=14, fontweight="bold")
ax.yaxis.set_major_formatter(FuncFormatter(lambda x, _: f"{x:,.0f}"))
ax.grid(axis="y", linestyle="--", alpha=0.4, zorder=0)
ax.set_axisbelow(True)

fig.tight_layout()

os.makedirs("output/charts", exist_ok=True)
fig.savefig("output/charts/결제수단별_금액분포_바이올린.png", dpi=150)
print("저장 완료: output/charts/결제수단별_금액분포_바이올린.png")

plt.show()
