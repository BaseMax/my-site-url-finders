# My Site URL Finder

A simple Python-based web crawler that extracts and filters URLs from a given website while avoiding unwanted paths and file types. The crawler follows links recursively within the same domain and provides a clean list of URLs found across the website.

## Features

- Crawl a website recursively to extract all unique links.
- Exclude specific paths (e.g., shopping cart, login) and file extensions (e.g., PDFs, images, scripts).
- Clean URLs by removing query parameters.
- Filter out external links and only crawl within the specified domain.
- Randomized delay between requests to avoid overwhelming the server.

## Requirements

To run this script, you need Python 3 and the following libraries:

- `requests`
- `beautifulsoup4`

You can install these dependencies using `pip`:

```bash
pip install requests beautifulsoup4
```

### How to Use

Clone the repository:

```bash
git clone https://github.com/BaseMax/my-site-url-finders.git
cd my-site-url-finders
```

Modify the `start_url` variable in crawler.py to the website you want to crawl.

Run the script:

```bash
python crawler.py
```

The script will begin crawling the specified website, starting from the `start_url`, and output the links it finds to the console.

## Configuration

### `start_url`

The starting URL for the crawl. Change this to the website URL you want to crawl.

Example:

```python
start_url = "https://example.com/"
```

### `exclude_paths`

A list of URL path segments that should be ignored by the crawler. The crawler will skip links that match any of these paths.

Example:

```python
exclude_paths = [
    "shop/",
    "cart/",
    "checkout/",
    "my-account/",
    "wp-admin/",
    "wp-content/",
    "wp-includes/",
]
```

### `exclude_extensions`

A list of file extensions that should be ignored. The crawler will skip links that end with any of these file types.

Example:

```python
exclude_extensions = [
    ".pdf", ".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".css", ".js", ".zip", ".tar", ".mp3", ".mp4", ".rar"
]
```

### `clean_url`

This function removes query parameters from URLs to return the clean base URL.

Example:

```python
cleaned_url = clean_url("https://example.com/page?query=1&param=2")
print(cleaned_url)
# Output: https://example.com/page
```

### `get_links`

This function fetches all the links from a given webpage and returns them as a list.

Example:

```python
links = get_links("https://example.com/")
print(links)
# List of all the links on the page
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Author

2025 Max Base. All rights reserved.
