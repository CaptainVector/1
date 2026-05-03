#!/usr/bin/env python3
import sys
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from datetime import datetime
import os

def main():
    if len(sys.argv) < 2:
        print("Usage: python extract.py <page_url>")
        sys.exit(1)

    page_url = sys.argv[1]

    # ------------------- ۱. پارس کردن دامنه -------------------
    parsed = urlparse(page_url)
    domain = parsed.netloc   # مثال: "www.wikipedia.org"
    # اگر بخواهید فقط بخش اصلی دامنه (مثلاً wikipedia.org) را بگیرید:
    # domain_parts = domain.split('.')
    # if len(domain_parts) > 2:
    #     domain = '.'.join(domain_parts[-2:])   # wikipedia.org

    # ------------------- ۲. تعیین نام فایل با تاریخ و ساعت -------------------
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"{domain}_{timestamp}.txt"
    # اگر می‌خواهید فایل در پوشه‌ی `results` ذخیره شود:
    # os.makedirs("results", exist_ok=True)
    # filename = os.path.join("results", filename)

    # ------------------- ۳. درخواست HTTP (با User‑Agent) -------------------
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (X11; Linux x86_64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/121.0.0.0 Safari/537.36"
        ),
        "Accept-Language": "en-US,en;q=0.9"
    }

    try:
        resp = requests.get(page_url, headers=headers, timeout=30)
        resp.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print(f"⚠️  درخواست با کد {resp.status_code} مواجه شد: {e}")
        sys.exit(1)
    except requests.exceptions.RequestException as e:
        print(f"❌ خطای شبکه: {e}")
        sys.exit(1)

    # ------------------- ۴. استخراج لینک‌ها -------------------
    soup = BeautifulSoup(resp.text, "html.parser")
    links = [a["href"] for a in soup.find_all("a", href=True)]

    # ------------------- ۵. نوشتن در فایل -------------------
    with open(filename, "w", encoding="utf-8") as f:
        for link in links:
            f.write(link + "\n")

    print(f"✅ {len(links)} لینک در فایل '{filename}' ذخیره شد.")

if __name__ == "__main__":
    main()
