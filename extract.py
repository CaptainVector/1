import sys
import requests
from bs4 import BeautifulSoup

def main():
    if len(sys.argv) < 2:
        print("Usage: python extract.py <page_url>")
        sys.exit(1)
    page_url = sys.argv[1]

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

    soup = BeautifulSoup(resp.text, "html.parser")
    links = [a["href"] for a in soup.find_all("a", href=True)]

    with open("urls.txt", "a", encoding="utf-8") as f:
        for link in links:
            f.write(link + "\n")

    print(f"✅ {len(links)} لینک به urls.txt افزوده شد.")

if __name__ == "__main__":
    main()
