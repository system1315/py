# parser.py
# BeautifulSoup을 이용한 HTML 파서 (알라딘용, 평가표 10가지 정보 최대 반영)
from bs4 import BeautifulSoup

def parse_book_list(html, topic):
    """
    도서 목록 페이지에서 도서 정보(제목, 저자, 출판사, 출간일, 상세URL, 이미지, 주제 등) 추출
    """
    soup = BeautifulSoup(html, 'html.parser')
    books = []
    for item in soup.select('div.ss_book_box'):
        try:
            title_tag = item.select_one('.bo3')
            title = title_tag.get_text(strip=True) if title_tag else ''
            detail_url = title_tag['href'] if title_tag and title_tag.has_attr('href') else ''
            img_url = item.select_one('.cover img')['src'] if item.select_one('.cover img') else ''
            # 저자/출판사/출간일 정보는 ss_book_list에서 추출
            info = item.select_one('.ss_book_list')
            author, publisher, pubdate = '', '', ''
            if info:
                info_text = info.get_text(' ', strip=True)
                parts = info_text.split('|')
                if len(parts) >= 3:
                    author, publisher, pubdate = parts[0].strip(), parts[1].strip(), parts[2].strip()
            books.append({
                'title': title,
                'author': author,
                'publisher': publisher,
                'pubdate': pubdate,
                'detail_url': detail_url,
                'img_url': img_url,
                'topic': topic
            })
        except Exception as e:
            print(f"[목록 파싱 오류] {e}")
    return books

def parse_book_detail(html):
    """
    도서 상세 페이지에서 정가, 판매가, 평점, 소개, 판매지수, 이미지 등 추가 정보 추출
    """
    soup = BeautifulSoup(html, 'html.parser')
    price = ''
    sale_price = ''
    rating = ''
    desc = ''
    sales_point = ''
    # 정가/판매가
    try:
        price_tag = soup.select_one('.price2')
        if price_tag:
            price = price_tag.get_text(strip=True)
        sale_tag = soup.select_one('.price2 .ss_p2')
        if sale_tag:
            sale_price = sale_tag.get_text(strip=True)
    except Exception as e:
        print(f"[가격 파싱 오류] {e}")
    # 평점
    try:
        rating_tag = soup.select_one('.rating2 span')
        if rating_tag:
            rating = rating_tag.get_text(strip=True)
    except Exception as e:
        print(f"[평점 파싱 오류] {e}")
    # 소개
    try:
        desc_tag = soup.select_one('#Ere_prod_mconts')
        if desc_tag:
            desc = desc_tag.get_text(strip=True)[:100]
    except Exception as e:
        print(f"[소개 파싱 오류] {e}")
    # 판매지수
    try:
        sales_tag = soup.select_one('.Ere_sub2_title span.ss_p2')
        if sales_tag:
            sales_point = sales_tag.get_text(strip=True)
    except Exception as e:
        print(f"[판매지수 파싱 오류] {e}")
    return {
        'price': price,
        'sale_price': sale_price,
        'rating': rating,
        'desc': desc,
        '판매지수': sales_point
    }
