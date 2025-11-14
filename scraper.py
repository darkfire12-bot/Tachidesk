import requests
from bs4 import BeautifulSoup

def scrape_manga_titles(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad status codes

        soup = BeautifulSoup(response.content, 'html.parser')

        manga_titles = []
        for a_tag in soup.find_all('a', href=True):
            if '/manga/' in a_tag['href']:
                title = a_tag.get_text(strip=True)
                if title and title not in manga_titles and not title.lower().startswith('chapter'):
                    manga_titles.append(title)

        return manga_titles

    except requests.exceptions.RequestException as e:
        print(f"Error fetching the URL: {e}")
        return None

if __name__ == "__main__":
    target_url = "https://www.manhwaden.com/"
    titles = scrape_manga_titles(target_url)

    if titles:
        # Filter out "See More Popular Mangas" as it is not a manga title.
        filtered_titles = [t for t in titles if t != "See More Popular Mangas"]
        with open("manga_titles.txt", "w", encoding="utf-8") as f:
            for title in filtered_titles:
                f.write(f"{title}\n")
        print(f"Successfully scraped {len(filtered_titles)} manga titles to manga_titles.txt")
    else:
        print("No manga titles were scraped.")
