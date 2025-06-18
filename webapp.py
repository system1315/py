from flask import Flask, render_template, request
import pandas as pd
import os

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(base_dir, 'data', 'book_data_clean.csv')

    if not os.path.exists(csv_path):
        return '<h2>book_data.csv 파일이 없습니다. 먼저 크롤링을 실행하세요.</h2>'

    try:
        df = pd.read_csv(csv_path)
    except Exception as e:
        return f'<h2>CSV 파일 읽기 오류: {e}</h2>'

    total_count = len(df)

    # 검색어 처리
    query = request.form.get('query', '') if request.method == 'POST' else ''
    if query:
        mask = df['title'].astype(str).str.contains(query, na=False) | \
               df['author'].astype(str).str.contains(query, na=False) | \
               df['publisher'].astype(str).str.contains(query, na=False)
        search_result = df[mask][['img_url', 'title', 'author', 'publisher', 'pubdate']].copy()
        search_result['img_url'] = search_result['img_url'].fillna('')  # NaN 방지

        # 이미지 태그로 변환
        def img_tag(url):
            if pd.isna(url) or url == '':
                return ''
            return f'<img src="{url}" width="60">'
        search_result['img_url'] = search_result['img_url'].apply(img_tag)

        # 표로 변환 (escape=False로 이미지 태그 적용)
        search_result_html = search_result.to_html(index=False, escape=False, classes='table table-bordered')
    else:
        search_result_html = None

    # 1년 이내 신간, 판매가 2만원 이하 도서
    one_year_ago = pd.Timestamp.now() - pd.Timedelta(days=365)
    if 'pubdate' in df.columns and 'sale_price' in df.columns:
        try:
            cond = (pd.to_datetime(df['pubdate'], errors='coerce') > one_year_ago) & \
                   (pd.to_numeric(df['sale_price'], errors='coerce').fillna(0) <= 20000)
            new_books = df[cond][['title', 'author', 'sale_price', 'pubdate']]
        except Exception:
            new_books = pd.DataFrame()
    else:
        new_books = pd.DataFrame()

    # 평점 4.5 이상 도서
    if 'rating' in df.columns:
        try:
            high_rating = df[pd.to_numeric(df['rating'], errors='coerce').fillna(0) >= 4.5][['title', 'author', 'rating']]
        except Exception:
            high_rating = pd.DataFrame()
    else:
        high_rating = pd.DataFrame()

    # 판매지수 Top 5
    if '판매지수' in df.columns:
        try:
            top_sales = df.copy()
            top_sales['판매지수'] = pd.to_numeric(top_sales['판매지수'], errors='coerce').fillna(0)
            top_sales = top_sales.sort_values('판매지수', ascending=False).head(5)[['title', 'author', '판매지수']]
        except Exception:
            top_sales = pd.DataFrame()
    else:
        top_sales = pd.DataFrame()

    return render_template(
        'result.html',
        total_count=total_count,
        new_books=new_books.to_html(index=False, classes='table table-striped') if not new_books.empty else None,
        high_rating=high_rating.to_html(index=False, classes='table table-striped') if not high_rating.empty else None,
        top_sales=top_sales.to_html(index=False, classes='table table-striped') if not top_sales.empty else None,
        query=query,
        search_result=search_result_html  # ✅ HTML로 변환된 검색 결과 전달
    )

if __name__ == '__main__':
    app.run(debug=True)