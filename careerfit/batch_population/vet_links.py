from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup


def check_link_validity(url, timeout=5):
    """
    Checks the validity of a given URL by making an HTTP GET request.
    """
    try:
        response = requests.get(url, timeout=timeout)
        return 200 <= response.status_code < 300
    except requests.exceptions.RequestException:
        return False

def post_process_links(json_data):
    """
    Removes invalid HTTP links from the JSON data,
    and swaps a valid link to a careers page where possible.
    """
    for key, value in list(json_data.items()):
        if isinstance(value, str) and value.startswith("http"):
            if not check_link_validity(value):
                json_data[key] = ""
            else:
                careers_page = find_careers_page(value)
                if careers_page:
                    json_data[key] = careers_page

    return json_data

def find_careers_page(base_url):
    """
    Given a website URL, look for a link to a careers or jobs page.

    Args:
        base_url (str): The URL of the website to scrape.

    Returns:
        str or None: The careers page URL if found, otherwise None.
    """
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(base_url, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')

        links = soup.find_all('a', href=True)

        job_keywords = ["career", "careers", "job", "jobs", "work-with-us", "join-us", "vacancies", "employment", "hiring",
                        "carrière", "carrières", "baan", "banen", "werken-bij", "bij-ons-werken", "vacatures", "werkgelegenheid", "aanwerving"]

        for link in links:
            href = link['href'].lower()
            text = link.get_text(strip=True).lower()

            if any(keyword in href or keyword in text for keyword in job_keywords):
                return urljoin(base_url, link['href'])

        return None

    except requests.RequestException as e:
        print(f"Error fetching {base_url}: {e}")
        return None


if __name__ == "__main__":
    careers_url = find_careers_page("https://bird.com/en-nl/applications/video-scheduling")
    print("Careers Page:", careers_url)
    careers_url = find_careers_page("https://www.a10networks.com/")
    print("Careers Page:", careers_url)
