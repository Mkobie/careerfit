import json
import os
import pathlib as Path
from typing import List, Dict, Union


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

    def load_data(self) -> List[Dict[str, Union[str, int, List[str]]]]:
        """
        Load all company data from JSON files in the source path.

        Returns:
            List[Dict[str, Union[str, int, List[str]]]]: A list of dictionaries containing company data.
        """
        data = []
        for filename in os.listdir(self.source_path):
            if filename.endswith(".json"):
                try:
                    with open(os.path.join(self.source_path, filename), "r") as f:
                        company_data = json.load(f)
                        data.append(company_data)
                        self.list_of_company_names.append(company_data['name'])
                except json.JSONDecodeError as e:
                    print(f"Error loading {filename}: {e}")
        return data

    def save_data(self, company_info: Dict) -> None:
        """
        Save updated data back to the corresponding JSON files.
        We match the updated record by its 'name' field to find the correct file.

        Args:
            company_info (Dict): Company info to save.
        """
        filename = f"{company_info['name'].replace(' ', '_')}.json"
        with open(self.source_path / filename, "w", encoding="utf-8") as file:
            json.dump(company_info, file, indent=4, ensure_ascii=False)

    def get_company_names(self):
        """
        Return the list of companies in the loaded user-made list.
        :return:
        """
        return self.list_of_company_names
