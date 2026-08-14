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

os.makedirs("output/charts", exist_ok=True)

# ---------- 1) 연령대별 거래금액 분포 - 박스플롯 ----------
# 연령대를 나이 순서로 정렬 - 그냥 두면 문자열 순서(10대,20대,30대...)라 상관없어 보이지만
# '알수없음'/'미상' 같은 결측 라벨이 섞이면 순서가 뒤섞이므로 명시적으로 순서를 지정함
age_order = ["10대", "20대", "30대", "40대", "50대", "60대 이상"]
present_ages = [a for a in age_order if a in df["연령대"].unique()]
other_ages = [a for a in df["연령대"].unique() if a not in age_order]
order = present_ages + other_ages

# 박스플롯을 그릴 때만 초고액 이상치를 뺌(정제 파일 자체는 건드리지 않음).
# IQR(사분위범위) 기준 상한을 넘는 값은 소수의 극단치라서 그대로 두면 박스가 눌려 보임
q1, q3 = df["거래금액"].quantile(0.25), df["거래금액"].quantile(0.75)
iqr = q3 - q1
upper_fence = q3 + 1.5 * iqr
n_excluded = (df["거래금액"] > upper_fence).sum()
df_box = df[df["거래금액"] <= upper_fence]
print(f"박스플롯용 이상치 제외: {n_excluded}건 (상한 {upper_fence:,.0f}원 초과)")

data_by_age = [df_box.loc[df_box["연령대"] == a, "거래금액"].dropna().values for a in order]

fig1, ax1 = plt.subplots(figsize=(10, 6))
bp = ax1.boxplot(data_by_age, tick_labels=order, patch_artist=True,
                  medianprops=dict(color="#8B3A00", linewidth=2),
                  flierprops=dict(marker="o", markersize=3, markerfacecolor="#C0392B", markeredgecolor="none", alpha=0.5))
for patch in bp["boxes"]:
    patch.set_facecolor("#F0A868")
    patch.set_edgecolor("#8B3A00")

ax1.set_xlabel("연령대", fontsize=14, fontweight="bold")
ax1.set_ylabel("거래금액 (천원)", fontsize=14, fontweight="bold")
ax1.tick_params(axis="x", labelsize=12)
ax1.tick_params(axis="y", labelsize=12)
ax1.yaxis.set_major_formatter(FuncFormatter(lambda x, _: f"{x/1000:,.0f}"))
ax1.grid(axis="y", linestyle="--", alpha=0.4, zorder=0)
ax1.set_axisbelow(True)

ax1.set_title(f"연령대별 거래금액 분포 (IQR 상한 초과 이상치 {n_excluded}건 제외)",
              fontsize=16, fontweight="bold")

fig1.tight_layout()
fig1.savefig("output/charts/연령대별_거래금액_분포.png", dpi=150)
print("저장 완료: output/charts/연령대별_거래금액_분포.png")

# ---------- 2) 요일별 거래 건수 - 막대그래프 ----------
weekday_kr = ["월", "화", "수", "목", "금", "토", "일"]
df["요일"] = df["거래일시"].dt.dayofweek.map(dict(enumerate(weekday_kr)))
weekday_counts = df["요일"].value_counts().reindex(weekday_kr)

fig2, ax2 = plt.subplots(figsize=(9, 6))
colors = ["#D9822B"] * 5 + ["#C0392B"] * 2  # 주말(토,일)만 강조색으로 구분
bars = ax2.bar(weekday_counts.index, weekday_counts.values, color=colors)
ax2.set_title("요일별 거래 건수", fontsize=18, fontweight="bold")
ax2.set_xlabel("요일", fontsize=14, fontweight="bold")
ax2.set_ylabel("거래 건수", fontsize=14, fontweight="bold")
ax2.tick_params(axis="x", labelsize=12)
ax2.tick_params(axis="y", labelsize=12)
ax2.grid(axis="y", linestyle="--", alpha=0.4, zorder=0)
ax2.set_axisbelow(True)

for bar in bars:
    height = bar.get_height()
    ax2.annotate(f"{height:,}건", xy=(bar.get_x() + bar.get_width() / 2, height),
                 xytext=(0, 4), textcoords="offset points", ha="center", va="bottom",
                 fontsize=11, fontweight="bold")

ax2.margins(y=0.12)
fig2.tight_layout()
fig2.savefig("output/charts/요일별_거래건수.png", dpi=150)
print("저장 완료: output/charts/요일별_거래건수.png")

plt.show()
