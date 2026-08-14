import os
os.chdir(os.path.dirname(os.path.abspath(__file__)) + "/..")

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.ticker import FuncFormatter

mpl.rcParams["font.family"] = "Malgun Gothic"
mpl.rcParams["axes.unicode_minus"] = False
mpl.rcParams["font.size"] = 11

df = pd.read_csv("data/핀테크_정제완료.csv", encoding="utf-8-sig")

# 지역을 행, 업종을 열로 놓고 거래금액 합계를 교차집계함 (pivot_table)
# 값이 없는 조합은 0으로 채움 - 거래가 아예 없었던 셀도 히트맵에서 빈칸 없이 보여야 비교가 편함
pivot = pd.pivot_table(df, index="지역", columns="가맹점업종", values="거래금액",
                        aggfunc="sum", fill_value=0)
# '알수없음'은 결측을 채운 값이라 실제 지역이 아님 - 다른 지역과 같이 순위에 섞이면
# 지역별 매출 순위처럼 오해될 수 있어서, 정렬 대상에서 빼고 맨 아래에 고정함
unknown_label = "알수없음"
known = pivot.drop(index=unknown_label, errors="ignore")
known = known.sort_index(ascending=True)  # 지역명 문자열(가나다) 기준 오름차순
if unknown_label in pivot.index:
    pivot = pd.concat([known, pivot.loc[[unknown_label]]])
else:
    pivot = known

fig, ax = plt.subplots(figsize=(11, 9))
im = ax.imshow(pivot.values, cmap="Oranges", aspect="auto")

ax.set_xticks(range(len(pivot.columns)))
ax.set_xticklabels(pivot.columns, rotation=30, ha="right")
ax.set_yticks(range(len(pivot.index)))
ax.set_yticklabels(pivot.index)

ax.set_title("지역 × 업종 거래금액 합계 (천원)", fontsize=16, fontweight="bold")

# 값이 큰 셀은 배경이 진해서 검정 글씨가 안 보이므로, 셀 배경 밝기에 따라 글씨색을 흰/검정으로 자동 전환
vmax = pivot.values.max()
for i in range(pivot.shape[0]):
    for j in range(pivot.shape[1]):
        val = pivot.values[i, j]
        color = "white" if val > vmax * 0.6 else "black"
        ax.text(j, i, f"{val/1000:,.0f}", ha="center", va="center", fontsize=8, color=color)

cbar = fig.colorbar(im, ax=ax, shrink=0.8)
cbar.set_label("거래금액 합계 (천원)", fontsize=11, fontweight="bold")
cbar.ax.yaxis.set_major_formatter(FuncFormatter(lambda x, _: f"{x/1000:,.0f}"))

fig.tight_layout()

os.makedirs("output/charts", exist_ok=True)
fig.savefig("output/charts/지역_업종_거래금액_히트맵.png", dpi=150)
print("저장 완료: output/charts/지역_업종_거래금액_히트맵.png")

plt.show()
