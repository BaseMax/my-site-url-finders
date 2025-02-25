import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin, urlunparse
import time

visited = set()

start_url = "https://aloghesti.com/"

def clean_url(url):
    """ Remove query parameters from the URL and return the clean URL """
    parsed_url = urlparse(url)
    cleaned_url = urlunparse(parsed_url._replace(query=""))
    return cleaned_url

def get_links(url):
    """ Fetch all links from a webpage and return a list of URLs """
    try:
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            print(f"Failed to retrieve {url}")
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

def crawl_website(url):
    """ Recursively crawl the website and collect all unique links """
    global visited
    if url in visited:
        return

    if url.startswith(start_url + "shop/"):
        print(f"Ignoring shop URL: {url}")
        return

    visited.add(url)

    links = get_links(url)
    print(f"Found {len(links)} links on {url}")

    cleaned_links = {clean_url(link) for link in links}

    cleaned_links.discard(url)

    for link in cleaned_links:
        if link not in visited:
            print(f"Crawling {link}")
            crawl_website(link)
            time.sleep(1)

crawl_website(start_url)
