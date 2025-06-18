# analyzer.py
# 도서 데이터 분석 및 출력
import pandas as pd

def analyze_and_print(csv_path):
    df = pd.read_csv(csv_path)
    print(f"총 {len(df)}권의 도서가 수집되었습니다.")
    # 1년 이내 신간 중 판매가 2만원 이하 도서
    print("\n[1년 이내 신간, 판매가 2만원 이하 도서]")
    # 출판일, 판매가 컬럼이 있다고 가정
    # 실제 구현 시 컬럼명/포맷에 맞게 수정 필요
    # 예시: df['출판일']이 'YYYY-MM-DD' 형식
    import datetime
    one_year_ago = pd.Timestamp.now() - pd.Timedelta(days=365)
    if '출판일' in df.columns:
        cond = (pd.to_datetime(df['출판일'], errors='coerce') > one_year_ago) & (df['sale_price'] <= 20000)
        print(df[cond][['title', 'author', 'sale_price', '출판일']])
    else:
        print("출판일 정보가 없습니다.")
    # 평점 4.5 이상 도서
    print("\n[평점 4.5 이상 도서]")
    if 'rating' in df.columns:
        print(df[df['rating'] >= 4.5][['title', 'author', 'rating']])
    else:
        print("평점 정보가 없습니다.")
    # 판매지수(가장 많이 팔린 도서)
    print("\n[판매지수 Top 5]")
    if '판매지수' in df.columns:
        print(df.sort_values('판매지수', ascending=False).head(5)[['title', 'author', '판매지수']])
    else:
        print("판매지수 정보가 없습니다.") 