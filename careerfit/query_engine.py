from typing import List, Dict


class QueryEngine:
    """Handles filtering logic."""

    @staticmethod
    def filter_data(data: List[Dict], **kwargs) -> List[Dict]:
        """
        Filter data based on provided keyword arguments.

        Args:
            data (List[Dict]): The list of company data to filter.
            kwargs: Field filters such as industry, location, values, etc.

        Returns:
            List[Dict]: A list of filtered company data dictionaries.
        """
        filtered = data

        for key, value in kwargs.items():
            if not value:
                continue

            if key == "industry":
                filtered = [
                    company for company in filtered
                    if any(value.lower() in ind.lower() for ind in company.get("industry", []))
                ]
            elif key == "values":
                filtered = [
                    company for company in filtered
                    if value.lower() in [val.lower() for val in company.get("values", [])]
                ]
            elif key == "size":
                filtered = [
                    company for company in filtered
                    if company.get("size") and int(company.get("size")) == int(value)
                ]
            elif key == "ind_sponsor":
                filtered = [
                    company for company in filtered
                    if str(company.get("IND sponsor", "")).lower() == value.lower()
                ]
            elif key == "randstad":
                filtered = [
                    company for company in filtered
                    if company.get("has location in the randstad", "").lower() == "yes"
                ]
            elif key == "python":
                filtered = [
                    company for company in filtered
                    if company.get("has python jobs", "").lower() == "yes"
                ]
            elif key == "c":
                filtered = [
                    company for company in filtered
                    if company.get("has c or c++ jobs", "").lower() == "yes"
                ]
            elif key == "software":
                filtered = [
                    company for company in filtered
                    if company.get("has software or programming jobs", "").lower() == "yes"
                ]
            elif key == "has embedded programming jobs":
                filtered = [
                    company for company in filtered
                    if company.get("has python jobs", "").lower() == "yes"
                ]
            elif key == "english":
                filtered = [
                    company for company in filtered
                    if company.get("dutch is required", "").lower() == "no"
                ]
            elif key == "englishish":
                filtered = [
                    company for company in filtered
                    if company.get("dutch is required", "").lower() == "unsure"
                ]
            elif key == "global":
                filtered = [
                    company for company in filtered
                    if "countries with offices" in company and
                       isinstance(company["countries with offices"], list) and
                       len(company["countries with offices"]) > 1
                ]
            elif key == "name":
                filtered = [
                    company for company in filtered
                    if str(company.get("name", "")).lower() == value.lower()
                ]

        return filtered
