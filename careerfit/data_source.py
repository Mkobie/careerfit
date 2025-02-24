import json
import pathlib as Path
from typing import List, Dict

from careerfit.globals import COMPANIES_FILE


class DataSource:
    """Handles loading and fetching data from files or an API."""

    def __init__(self, source_path: Path):
        """
        Initialize the DataSource with a source path.

        Args:
            source_path (str): Path to the directory containing JSON data files.
        """
        self.source_path = source_path
        self.list_of_company_names = []

    def load_list_data(self, list_path):
        """
        Load company names from a user-made list.

        :param list_path:
        :return:
        """
        with list_path.open("r", encoding="utf-8") as f:
            list_company_names = [line.strip() for line in f]

        full_data = self.load_data()
        list_data = [company for company in full_data if company["name"] in list_company_names]
        return list_data

    def load_data(self) -> List[Dict]:
        """
        Load all company data from JSON file.

        Returns:
            List[Dict]: A list of dictionaries containing company data.
        """
        all_company_data = None
        try:
            with open(self.source_path, "r") as f:
                all_company_data = json.load(f)
        except json.JSONDecodeError as e:
            print(f"Error loading {self.source_path}")

        if all_company_data:
            for company in all_company_data:
                self.list_of_company_names.append(company['name'])

        return all_company_data

    def save_data(self, company_info) -> None:
        """
        Save updated data back to the JSON file.

        Args:
            company_info (Dict): All company info to be written back
        """
        with open(self.source_path, "w", encoding="utf-8") as file:
            json.dump(company_info, file, indent=4, ensure_ascii=False)

    def get_company_names(self):
        """
        Return the list of companies in the loaded user-made list.
        :return:
        """
        return self.list_of_company_names
