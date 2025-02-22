import requests
from bs4 import BeautifulSoup

from careerfit.globals import ORG_LIST_FILE

IND_SPONSORS_URL = 'https://ind.nl/en/public-register-recognised-sponsors/public-register-regular-labour-and-highly-skilled-migrants'
POSSIBLE_HEADERS = ['Company/organisation', 'Comp.Reg.nr.', 'Organisation', 'KVK number']


def scrape_ind_organisations(ind_sponsors_url: str = IND_SPONSORS_URL) -> list:
    """
    Scrape the list of organisations from the IND sponsor URL.

    :param ind_sponsors_url: The URL of the IND sponsors page.
    :return: A list of scraped organizations.
    """

    response = requests.get(ind_sponsors_url)
    soup = BeautifulSoup(response.content, 'html.parser')

    organisation_elements = soup.select('tbody th')
    organisations = [element.get_text(strip=True) for element in organisation_elements
                     if element.get_text(strip=True) not in POSSIBLE_HEADERS]

    return organisations

def save_organizations_to_file(organizations: list):
    with open(ORG_LIST_FILE, "w", encoding="utf-8") as file:
        for org in organizations:
            file.write(org + "\n")


if __name__=="__main__":
    save_organizations_to_file(scrape_ind_organisations())
