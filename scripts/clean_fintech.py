import pandas as pd

SRC = "data/01_핀테크결제_dirty.csv"
DST = "data/핀테크_정제완료.csv"

df = pd.read_csv(SRC, encoding="utf-8-sig")
n_before = len(df)

report = []

# 1. 완전 중복행 제거
n_dup = df.duplicated().sum()
df = df.drop_duplicates()
report.append(("완전 중복행 제거", n_dup, "8개 컬럼 값이 모두 동일한 중복 레코드 삭제"))

# 2. 결제수단 공백 정제
mask_ws = df["결제수단"].astype(str).str.strip().ne(df["결제수단"].astype(str))
n_ws = mask_ws.sum()
df["결제수단"] = df["결제수단"].astype(str).str.strip()
df.loc[df["결제수단"] == "nan", "결제수단"] = pd.NA
report.append(("결제수단 앞뒤 공백 제거", n_ws, "' 신용카드 ' -> '신용카드' 등 트림 처리"))

# 3. 거래일시 포맷 표준화 (YYYY-MM-DD HH:MM:SS)
n_dt_mixed = (df["거래일시"].astype(str).str.len() != 19).sum()
df["거래일시"] = pd.to_datetime(df["거래일시"], format="mixed").dt.strftime("%Y-%m-%d %H:%M:%S")
report.append(("거래일시 포맷 표준화", n_dt_mixed, "'YYYY/MM/DD HH:MM' 등 혼재 포맷을 'YYYY-MM-DD HH:MM:SS'로 통일"))

# 4. 거래금액 결측 -> 행 제외 (임의 대체 시 분석 왜곡 위험)
n_amt_na = df["거래금액"].isna().sum()
df = df[df["거래금액"].notna()]
report.append(("거래금액 결측행 제외", n_amt_na, "금액을 임의로 채우면 매출 집계가 왜곡되므로 행 삭제"))

# 5. 음수 거래금액 절대값 보정 (전부 거래상태='성공' -> 부호 입력 오류로 판단)
neg_mask = df["거래금액"] < 0
n_neg = neg_mask.sum()
df.loc[neg_mask, "거래금액"] = df.loc[neg_mask, "거래금액"].abs()
report.append(("음수 거래금액 절대값 보정", n_neg, "전건 거래상태='성공'으로 환불이 아닌 부호 입력 오류로 판단, 절댓값으로 보정"))

# 6. 결측 카테고리(결제수단/지역/연령대) -> '미상'으로 채움
for col in ["결제수단", "지역", "연령대"]:
    n_na = df[col].isna().sum()
    df[col] = df[col].fillna("미상")
    report.append((f"{col} 결측 -> '미상' 대체", n_na, "임의 값 추정 대신 '미상' 카테고리로 명시적 표기"))

n_after = len(df)

df.to_csv(DST, index=False, encoding="utf-8-sig")

rep_df = pd.DataFrame(report, columns=["처리 항목", "처리 건수", "사유"])
rep_df.to_csv("scripts/_clean_report.csv", index=False, encoding="utf-8-sig")

print(f"정제 전 행 수: {n_before}")
print(f"정제 후 행 수: {n_after}")
print(f"저장 완료: {DST}")
print()
print(rep_df.to_string(index=False))
