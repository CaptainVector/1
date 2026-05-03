#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from datetime import datetime

def main():
    if len(sys.argv) < 2:
        print("Usage: python extract.py <page_url>")
        sys.exit(1)

    page_url = sys.argv[1]

    # ۱. پارس کردن دامنه برای نام‌گذاری فایل
    parsed = urlparse(page_url)
    domain = parsed.netloc  # مثال: www.pornhub.com

    # ۲. نام فایل با تاریخ و ساعت
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"{domain}_{timestamp}.txt"

    # ۳. ایجاد session (برای کوکی‌های خودکار)
    session = requests.Session()

    # ۴. هدرهای مطمئن (User‑Agent + Accept‑Language + Referer)
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (X11; Linux x86_64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/121.0.0.0 Safari/537.36"
        ),
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": page_url
    }
    session.headers.update(headers)

    # ۵. پیکربندی پروکسی (اختیاری)
    proxy_url = os.getenv("PROXY_URL")  # مثال: http://user:pass@proxy:3128
    if proxy_url:
        session.proxies.update({
            "http": proxy_url,
            "https": proxy_url
        })

    # ۶. ارسال درخواست
    try:
        resp = session.get(page_url, timeout=30, allow_redirects=True)
        resp.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print(f"⚠️  درخواست با کد {resp.status_code} مواجه شد: {e}")
        sys.exit(1)
    except requests.exceptions.RequestException as e:
        print(f"❌ خطای شبکه: {e}")
        sys.exit(1)

    # ۷. استخراج لینک‌ها
    soup = BeautifulSoup(resp.text, "html.parser")
    links = [a["href"] for a in soup.find_all("a", href=True)]

    # ۸. نوشتن در فایل
    with open(filename, "w", encoding="utf-8") as f:
        for link in links:
            f.write(link + "\n")

    print(f"✅ {len(links)} لینک در فایل '{filename}' ذخیره شد.")

if __name__ == "__main__":
    main()
