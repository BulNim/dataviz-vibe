import os
# 스크립트 위치와 무관하게 항상 프로젝트 루트를 기준으로 경로를 잡음 (CLAUDE.md 규칙)
os.chdir(os.path.dirname(os.path.abspath(__file__)) + "/..")

import pandas as pd

SRC = "data/01_핀테크결제_dirty.csv"
DST = "data/핀테크_정제완료.csv"

df = pd.read_csv(SRC, encoding="utf-8-sig")
n0 = len(df)
print(f"원본 행 수: {n0}")

# 1. 범주 컬럼 결측 채우기 - 행을 지우지 않고 값만 채움. 결제수단·지역은 '알수없음', 연령대는 '미상'
df["결제수단"] = df["결제수단"].fillna("알수없음")
df["지역"] = df["지역"].fillna("알수없음")
df["연령대"] = df["연령대"].fillna("미상")
n1 = len(df)
print(f"1단계(범주 결측 채우기) 후: {n1}행 (0건 감소 - 행을 지우지 않음)")

# 2. 거래일시·거래금액 결측 행 삭제 - 금액 없으면 합계 불가, 날짜 없으면 월별 집계 불가
before = len(df)
df = df.dropna(subset=["거래일시", "거래금액"])
n2 = len(df)
print(f"2단계(거래일시·거래금액 결측 삭제) 후: {n2}행 ({before - n2}건 감소)")

# 3. 완전 중복 제거 - 모든 컬럼이 같은 행을 첫 건만 남김. 반드시 마지막에 수행
before = len(df)
df = df.drop_duplicates()
n3 = len(df)
print(f"3단계(완전 중복 제거) 후: {n3}행 ({before - n3}건 감소)")

df.to_csv(DST, index=False, encoding="utf-8-sig")

print()
print(f"정제 전: {n0}행 -> 정제 후: {n3}행 (총 {n0 - n3}건 감소)")
print(f"저장 완료: {DST}")
