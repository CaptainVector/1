# scripts/extract.py
import sys
import requests
from bs4 import BeautifulSoup

def main():
    # ۱. آدرس صفحه را از آرگومان خط فرمان می‌خوانیم
    if len(sys.argv) < 2:
        print("Usage: python extract.py <page_url>")
        sys.exit(1)
    page_url = sys.argv[1]

    # ۲. صفحه را دانلود می‌کنیم
    resp = requests.get(page_url, timeout=30)
    resp.raise_for_status()

    # ۳. با BeautifulSoup به دنبال تمام <a href> ها می‌گردیم
    soup = BeautifulSoup(resp.text, "html.parser")
    links = [a["href"] for a in soup.find_all("a", href=True)]

    # ۴. فایل خروجی را باز می‌کنیم و همه‌ی لینک‌ها را اضافه می‌کنیم
    with open("urls.txt", "a", encoding="utf-8") as f:
        for link in links:
            f.write(link + "\n")

    print(f"✅ {len(links)} لینک به urls.txt افزوده شد.")

if __name__ == "__main__":
    main()
