import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin, urlunparse
import warnings
from urllib3.exceptions import InsecureRequestWarning
from concurrent.futures import ThreadPoolExecutor
from threading import Semaphore

warnings.simplefilter('ignore', InsecureRequestWarning)

visited = set()

start_url = "https://aloghesti.com/"
exclude_paths = [
    "shop/",
    "cart/",
    "checkout/",
    "my-account/",
    "wp-admin/",
    "wp-content/",
    "wp-includes/",
]

exclude_extensions = [
    ".pdf", ".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".css", ".js", ".zip", ".tar", ".mp3", ".mp4", ".rar"
]

MAX_WORKER = 5
semaphore = Semaphore(MAX_WORKER)

def clean_url(url):
    """ Remove query parameters and fragments from the URL and return the clean URL """
    parsed_url = urlparse(url)
    cleaned_url = urlunparse(parsed_url._replace(query="", fragment=""))
    return cleaned_url

def get_links(url):
    """ Fetch all links from a webpage and return a list of URLs """
    try:
        response = requests.get(url, timeout=10, verify=False)
        if response.status_code != 200:
            print(f"Failed to retrieve {url} (status code {response.status_code})")
            return []

        soup = BeautifulSoup(response.content, 'html.parser')
        links = []

        for a_tag in soup.find_all('a', href=True):
            link = a_tag['href']
            link = urljoin(url, link)
            links.append(link)

        return links

    except requests.exceptions.RequestException as e:
        print(f"Request failed for {url}: {e}")
        return []

def should_exclude(url):
    """ Check if a URL should be excluded based on the exclude_paths list or file extensions """
    for path in exclude_paths:
        if path in url:
            print(f"Ignoring URL: {url} (matches exclusion pattern: {path})")
            return True

    if any(url.endswith(ext) for ext in exclude_extensions):
        print(f"Ignoring URL: {url} (matches exclusion file extension)")
        return True

    return False

def crawl_website(url, executor):
    """ Recursively crawl the website and collect all unique links """
    global visited
    if url in visited:
        return

    if should_exclude(url):
        return

    parsed_url = urlparse(url)
    if parsed_url.netloc != urlparse(start_url).netloc:
        print(f"Ignoring external URL: {url}")
        return

    visited.add(url)

    links = get_links(url)
    print(f"Found {len(links)} links on {url}")

    cleaned_links = {clean_url(link) for link in links}

    cleaned_links.discard(url)

    futures = []
    for link in cleaned_links:
        if link not in visited:
            print(f"Submitting task for {link}")
            
            semaphore.acquire()
            futures.append(executor.submit(process_link, link, executor))

    for future in futures:
        future.result()

    semaphore.release()

def process_link(link, executor):
    """ Process each link by crawling it """
    try:
        crawl_website(link, executor)
    finally:
        semaphore.release()

def main():
    with ThreadPoolExecutor(max_workers=MAX_WORKER) as executor:
        crawl_website(start_url, executor)

if __name__ == "__main__":
    main()
