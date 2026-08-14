import os
os.chdir(os.path.dirname(os.path.abspath(__file__)) + "/..")

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.patheffects as pe

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
# 비율(pay) 순서에 맞춰 건수도 같이 뽑음 - 조각 옆에 "39.2%\n(4,605건)"처럼 같이 보여주기 위함
cnt = df["결제수단"].value_counts().reindex(pay.index)
total_cnt = df["결제수단"].notna().sum()

fig2, ax2 = plt.subplots(figsize=(8, 8))
colors = plt.cm.Oranges_r([i / len(pay) * 0.7 for i in range(len(pay))])
wedges, texts, autotexts = ax2.pie(
    pay.values, labels=pay.index,
    autopct=lambda p: f"{p:.1f}%",  # 아래에서 건수 줄을 직접 덧붙이므로 우선 비율만 넣음
    startangle=90,
    pctdistance=0.78, colors=colors,
    wedgeprops=dict(width=0.4, edgecolor="white"),
    textprops=dict(fontsize=12, fontweight="bold"),
)

# 비율 글씨는 밝은/어두운 조각 어디에 있든 잘 보이도록 흰색 + 검정 테두리(outline)로 그림
for at, c in zip(autotexts, cnt.values):
    at.set_color("white")
    at.set_fontsize(12)
    at.set_fontweight("bold")
    at.set_text(f"{at.get_text()}\n({c:,}건)")
    at.set_path_effects([pe.withStroke(linewidth=2.5, foreground="black")])

ax2.set_title("결제수단별 거래금액 비중", fontsize=18, fontweight="bold")

# 도넛 가운데 빈 공간에 전체 결제 건수를 적음 - 비중만 보여주고 전체 규모(모수)가 안 보이면 오해하기 쉬움
ax2.text(0, 0, f"전체\n{total_cnt:,}건", ha="center", va="center",
          fontsize=15, fontweight="bold")

ax2.axis("equal")

fig2.tight_layout()
fig2.savefig("output/charts/결제수단별_금액비중.png", dpi=150)
print("저장 완료: output/charts/결제수단별_금액비중.png")

plt.show()
