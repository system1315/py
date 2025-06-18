from parser import parse_book_list, parse_book_detail

if __name__ == "__main__":
    with open("data/naver_book_sample.html", encoding="utf-8") as f:
        html = f.read()
    books = parse_book_list(html, "테스트")
    print("목록 파싱 결과:")
    for book in books:
        print(book)

    with open("data/naver_book_detail_sample.html", encoding="utf-8") as f:
        detail_html = f.read()
    detail = parse_book_detail(detail_html)
    print("\n상세정보 파싱 결과:")
    print(detail) 