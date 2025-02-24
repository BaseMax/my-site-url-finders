import requests
from bs4 import BeautifulSoup
import threading
import time

BASE_URL = "https://new.aloghesti.com/"

visited_links = set()
lock = threading.Lock()

def get_links(url):
    """Fetch all unique links from a given URL."""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        links = set()
        for a_tag in soup.find_all("a", href=True):
            href = a_tag["href"]
            if href.startswith(BASE_URL):
                links.add(href)

        return links
    except requests.RequestException:
        return set()

def save_links():
    """Save unique links to urls.txt safely."""
    with lock:
        try:
            with open("urls.txt", "w") as file:
                file.write("\n".join(visited_links))
        except Exception as e:
            print(f"Error saving file: {e}")

def crawl(url):
    """Recursively crawl and extract links."""
    if url in visited_links:
        return

    print(f"Crawling: {url}")
    visited_links.add(url)
    save_links()

    new_links = get_links(url)
    for link in new_links:
        crawl(link)

if __name__ == "__main__":
    start_url = BASE_URL
    crawl(start_url)
    print("Crawling completed.")
