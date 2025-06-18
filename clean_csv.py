import pandas as pd
import re

def extract_price(text):
    m = re.search(r'→\s*([\d,]+)원', str(text))
    return int(m.group(1).replace(',', '')) if m else None

def extract_rating(text):
    m = re.search(r'(\d+\.\d+)\s*\(', str(text))
    return float(m.group(1)) if m else None

def extract_pubdate(text):
    m = re.search(r'(\d{4})년\s*(\d{1,2})월', str(text))
    if m:
        return f"{m.group(1)}-{int(m.group(2)):02d}-01"
    return None

def extract_author(text):
    m = re.search(r'([가-힣a-zA-Z0-9·\\s]+)\\s*\\(지은이\\)', str(text))
    return m.group(1).strip() if m else str(text).strip()

df = pd.read_csv('data/book_data_clean.csv')

df['sale_price'] = df['pubdate'].apply(extract_price)
df['rating'] = df['pubdate'].apply(extract_rating)
df['pubdate_clean'] = df['pubdate'].apply(extract_pubdate)
df['author_clean'] = df['author'].apply(extract_author)

df = df.rename(columns={'pubdate_clean': 'pubdate', 'author_clean': 'author'})

df.to_csv('data/book_data_clean.csv', index=False)
print('정제 완료: data/book_data_clean.csv')