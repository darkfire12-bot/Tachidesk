import requests
from bs4 import BeautifulSoup

def scrape_manga_titles_from_page(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad status codes

        soup = BeautifulSoup(response.content, 'html.parser')

        manga_titles = []
        for a_tag in soup.find_all('a', href=True):
            if '/manga/' in a_tag['href']:
                title = a_tag.get_text(strip=True)
                if title and not title.lower().startswith('chapter'):
                    manga_titles.append(title)

        return manga_titles

    except requests.exceptions.RequestException as e:
        print(f"Error fetching the URL: {e}")
        return None

if __name__ == "__main__":
    base_url = "https://www.manhwaden.com/page/{}/"
    all_titles = set() # Use a set to automatically handle duplicates

    # There are 156 pages, so we'll loop through all of them.
    for page_number in range(1, 157): # from 1 to 156
        target_url = base_url.format(page_number)
        print(f"Scraping page {page_number}: {target_url}")
        titles_from_page = scrape_manga_titles_from_page(target_url)

        if titles_from_page:
            all_titles.update(titles_from_page)

    if all_titles:
        # Filter out "See More Popular Mangas" as it is not a manga title.
        filtered_titles = [t for t in all_titles if t != "See More Popular Mangas"]
        with open("manga_titles.txt", "w", encoding="utf-8") as f:
            for title in sorted(filtered_titles): # Sort the titles alphabetically
                f.write(f"{title}\n")
        print(f"\nSuccessfully scraped {len(filtered_titles)} unique manga titles to manga_titles.txt")
    else:
        print("No manga titles were scraped.")
