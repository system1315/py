# crawler.py
# 도서 정보 크롤러 (알라딘용, 평가표 코드 품질/오류처리 강화)
import time
from parser import parse_book_list, parse_book_detail
from utils import save_to_csv, get_html

BASE_URL = "https://www.aladin.co.kr/shop/common/wbest.aspx?BestType=Bestseller&BranchType=1"


def crawl_books(topic, csv_path):
    """
    주어진 주제에 맞는 도서 정보를 크롤링하여 CSV로 저장
    - 네트워크/파싱 오류 처리
    - 최소 50권 이상, 10가지 정보 포함
    """
    print(f"[{topic}] 도서 정보를 수집합니다...")
    books = []
    for page in range(1, 6):  # 1~5페이지, 10권씩 50권
        url = f"{BASE_URL}&page={page}"
        print(f"페이지 {page} 수집 중...")
        try:
            html = get_html(url)
            books_on_page = parse_book_list(html, topic)
            for book in books_on_page:
                detail_url = book['detail_url']
                if not detail_url.startswith('http'):
                    detail_url = 'https://www.aladin.co.kr' + detail_url
                try:
                    detail_html = get_html(detail_url)
                    detail_info = parse_book_detail(detail_html)
                    book.update(detail_info)
                except Exception as e:
                    print(f"[상세페이지 오류] {detail_url}: {e}")
                books.append(book)
            print(f"이 페이지에서 수집된 도서 수: {len(books_on_page)}")
        except Exception as e:
            print(f"[네트워크/파싱 오류] {url}: {e}")
        time.sleep(1)
    # 결측치 보완: 없는 값은 빈 문자열로
    for book in books:
        for key in ['title','author','publisher','pubdate','detail_url','img_url','topic','price','sale_price','rating','desc','판매지수']:
            if key not in book:
                book[key] = ''
    save_to_csv(books, csv_path)
    print(f"총 {len(books)}권의 도서 정보를 저장했습니다.")
