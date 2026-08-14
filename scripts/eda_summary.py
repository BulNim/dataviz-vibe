import os
# 스크립트를 어디서 실행하든 data 폴더를 못 찾는 일이 없게, 항상 프로젝트 루트로 이동
os.chdir(os.path.dirname(os.path.abspath(__file__)) + "/..")

import pandas as pd

# 지수표기(1.234e+05) 대신 소수점 2자리로 보이게 설정 - 발표·보고용으로 더 읽기 쉬움
pd.set_option("display.float_format", "{:.2f}".format)

df = pd.read_csv("data/01_핀테크결제_dirty.csv", encoding="utf-8-sig")

print("=== 크기 ===")
print(df.shape)

print()
print("=== 앞 5행 ===")
print(df.head())

print()
print("=== 자료형 ===")
print(df.dtypes)

print()
print("=== 거래금액 요약 ===")
print(df[["거래금액"]].describe())

print()
print("=== 결제수단 값별 개수 ===")
# dropna=False 로 결측(NaN)도 하나의 항목으로 같이 세어야 빠진 개수를 놓치지 않음
print(df["결제수단"].value_counts(dropna=False))
