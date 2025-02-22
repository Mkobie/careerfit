import argparse

from careerfit import search
from careerfit.data_source import DataSource
from careerfit.globals import COMPANIES_DIR
from careerfit.query_engine import QueryEngine


def parse_arguments():
    """
    Parse command-line arguments.

    Returns:
        argparse.Namespace: Parsed arguments.
    """
    parser = argparse.ArgumentParser(description="Search for companies based on specific criteria.")

    parser.add_argument("--company", "-c", required=True, help="Name of the company whose field you want to see/update.")
    parser.add_argument("--field", "-f", required=True, help="The JSON field to display/update.")
    parser.add_argument("--value", "-v", nargs="?", default=-1, help="Value to set if updating. Will set empty string if given without an argument.")

    return parser.parse_args()

def main():
    """
    Main entry point for the CLI tool.
    Parses arguments, loads data, filters it, and prints the results.

    Example usage:
    $ careerfit-admin --company "050media" --field "website"
    $ careerfit-admin --company "050media" --field "website" --value "https://www.050media.nl/"
    """
    args = parse_arguments()

    data_source = DataSource(COMPANIES_DIR)
    data = data_source.load_data()

    company_name = search.resolve_company_argument(args.company)
    field = args.field
    if args.value == -1:
        for company in data:
            if company.get("name", "").lower() == company_name.lower():
                current_value = company.get(field, None)
                if current_value is None:
                    print(f"Field '{field}' not found for company '{company_name}'.")
                else:
                    print(current_value)
                break
        else:
            print(f"Company '{company_name}' not found in data. Nothing displayed.")

    else:
        value = args.value or ""
        company_data = QueryEngine.filter_data(data, name=company_name)
        if not company_data:
            print("Search failed - check the spelling")
        else:
            company_data = company_data[0]
            old_value = company_data[field]
            company_data[field] = value
            data_source.save_data(company_data)
            print(f"Updated {company_name} {field} from '{old_value}' to '{value}'")


if __name__ == "__main__":
    main()
