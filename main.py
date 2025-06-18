# 온라인 서점 도서 정보 수집 및 분석 메인 파일
# 작성자: (작성자 이름)
# -*- coding: utf-8 -*-
import sys
from crawler import crawl_books
from analyzer import analyze_and_print

if __name__ == "__main__":
    print("수집할 도서 주제를 선택하세요:")
    print("1. 인공지능/데이터 과학")
    print("2. 자기계발/재테크")
    print("3. 환경/지속가능성")
    topic_map = {"1": "인공지능", "2": "자기계발", "3": "환경"}
    topic = input("번호 입력: ")
    if topic not in topic_map:
        print("잘못된 입력입니다.")
        sys.exit(1)
    print(f"선택된 주제: {topic_map[topic]}")
    csv_path = "data/book_data.csv"
    crawl_books(topic_map[topic], csv_path)
    analyze_and_print(csv_path) 