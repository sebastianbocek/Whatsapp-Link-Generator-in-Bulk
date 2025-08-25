import requests
from bs4 import BeautifulSoup
import re

COMMON_PATHS = ['/contact', '/about', '/support', '/contact-us', '/contacts']
HEADERS = {"User-Agent": "Mozilla/5.0"}
TIMEOUT = 10

# Regex para detectar links de WhatsApp
WHATSAPP_REGEX = re.compile(r"(https?://(wa\.me|api\.whatsapp\.com)/[^\s\"'>]+|whatsapp://[^\s\"'>]+)", re.IGNORECASE)

def extract_whatsapp_links(html):
    soup = BeautifulSoup(html, 'html.parser')
    links = set()

    # Buscar en los href de <a>
    for a in soup.find_all('a', href=True):
        href = a['href']
        match = WHATSAPP_REGEX.search(href)
        if match:
            links.add(match.group(0))

    # Buscar en texto plano también (por si están escritos sin <a>)
    text_matches = WHATSAPP_REGEX.findall(soup.get_text(separator=' '))
    for match in text_matches:
        if isinstance(match, tuple):  # regex devuelve tuplas a veces
            links.add(match[0])
        else:
            links.add(match)

    return links

def scrape_page(url):
    try:
        response = requests.get(url, headers=HEADERS, timeout=TIMEOUT)
        if response.status_code == 200:
            return extract_whatsapp_links(response.text)
    except Exception as e:
        print(f"❌ Error fetching {url}: {e}")
    return set()

def normalize_url(url):
    if not url.startswith("http"):
        url = "http://" + url
    return url.rstrip("/")

def main():
    input_file = "websites.txt"
    output_file = "whatsapp_links.txt"

    with open(input_file, 'r', encoding='utf-8') as f:
        raw_urls = [line.strip() for line in f if line.strip()]

    all_whatsapp_links = set()

    for base_url in raw_urls:
        base_url = normalize_url(base_url)
        print(f"\n🔍 Scraping: {base_url}")

        all_whatsapp_links |= scrape_page(base_url)

        for path in COMMON_PATHS:
            full_url = base_url + path
            all_whatsapp_links |= scrape_page(full_url)

    final_links = sorted(all_whatsapp_links)

    with open(output_file, 'w', encoding='utf-8') as out:
        out.write('\n'.join(final_links))

    print(f"\n✅ Done! {len(final_links)} WhatsApp links saved to {output_file}")

if __name__ == "__main__":
    main()
