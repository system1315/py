# utils.py
# 공통 유틸리티 함수 (오류처리/주석 보강)
import requests
import csv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def get_html(url, use_selenium=False):
    """
    url의 HTML을 반환. 동적 페이지는 selenium 사용
    네트워크 오류 발생 시 안내 메시지 출력
    """
    try:
        if use_selenium:
            options = Options()
            options.add_argument('--headless')
            driver = webdriver.Chrome(options=options)
            driver.get(url)
            html = driver.page_source
            driver.quit()
            return html
        else:
            resp = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
            resp.raise_for_status()
            return resp.text
    except Exception as e:
        print(f"[get_html 오류] {url}: {e}")
        return ''

def save_to_csv(data, csv_path):
    """
    리스트(딕셔너리)의 데이터를 CSV로 저장
    파일 저장 오류 발생 시 안내 메시지 출력
    """
    if not data:
        print("[save_to_csv] 저장할 데이터가 없습니다.")
        return
    keys = data[0].keys()
    try:
        with open(csv_path, 'w', newline='', encoding='utf-8-sig') as f:
            writer = csv.DictWriter(f, fieldnames=keys)
            writer.writeheader()
            writer.writerows(data)
        print(f"[save_to_csv] {csv_path} 저장 완료.")
    except Exception as e:
        print(f"[save_to_csv 오류] {csv_path}: {e}")
