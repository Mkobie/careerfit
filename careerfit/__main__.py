import argparse

from careerfit import search
from careerfit.data_source import DataSource
from careerfit.display import get_description_with_hyperlink
from careerfit.globals import COMPANIES_DIR, SAVE_DIR
from careerfit.query_engine import QueryEngine
from careerfit.user_lists import save, show_saved, unsave


def parse_arguments():
    """
    Parse command-line arguments.

    Returns:
        argparse.Namespace: Parsed arguments.
    """
    parser = argparse.ArgumentParser(description="Search for companies based on specific criteria.")

    parser.add_argument("--verbose", "-v", action="store_true", help="Show all results (without pagination)")
    parser.add_argument("--industry", help="Filter by industry (e.g., 'Information Technology')")
    parser.add_argument("--name", help="Filter by name")
    parser.add_argument("--values", help="Filter by company values (e.g., 'Innovation')")
    parser.add_argument("--size", type=int, help="Filter by company size (e.g., 5000)")
    parser.add_argument("--ind_sponsor", help="Filter by IND sponsorship status (yes or no)")
    parser.add_argument("--randstad", action="store_true", help="Filter for companies in the Randstad area")
    parser.add_argument("--python", action="store_true", help="Filter for companies with python jobs")
    parser.add_argument("--c", action="store_true", help="Filter for companies with c or c++ jobs")
    parser.add_argument("--software", action="store_true", help="Filter for companies with software or programming jobs")
    parser.add_argument("--embedded", action="store_true", help="Filter for companies with embedded programming jobs")
    parser.add_argument("--english", action="store_true", help="Filter for companies where only english is required")
    parser.add_argument("--englishish", action="store_true", help="Filter for companies where it's uncertain whether only english is required")
    parser.add_argument("--global", action="store_true", help="Filter for companies with office outside the Netherlands")

    parser.add_argument("--limit", type=int, default=5, help="Number of results per page (default: 10)")
    parser.add_argument("--page", type=int, default=1, help="Page number of results (default: 1)")
    parser.add_argument("--open-links", "-o", action="store_true", help="Automatically open company links in the browser")
    parser.add_argument("--show-industry", action="store_true", help="Show the industries list")
    parser.add_argument("--show-website", action="store_true", help="Show the website url")

    parser.add_argument("--show-saved", metavar="LIST_NAME", help="View a user's saved companies.")
    parser.add_argument("--save", nargs="+", metavar=("LIST_NAME", "COMPANY_NAME"), help="Add a company to a user's list.")
    parser.add_argument("--unsave", nargs=2, metavar=("LIST_NAME", "COMPANY_NAME"), help="Remove a company from a user's list, by name or position (1-9).")
    parser.add_argument("--source", help="Filter a specific saved list as the source instead of the full company database.")

    return parser.parse_args()

def main():
    """
    Main entry point for the CLI tool.
    Parses arguments, loads data, filters it, and prints the results.

    Example usage:
    $ careerfit --python
    $ careerfit --save my_list 1

    Tip: compare results use comm like this:
    comm -3 <(careerfit --python -v | sort) <(careerfit --software -v | sort)
    """
    args = parse_arguments()

    data_source = DataSource(COMPANIES_DIR)

    if args.source:
        data = data_source.load_list_data(SAVE_DIR / f"{args.source}.txt")
    else:
        data = data_source.load_data()

    if args.save:
        list_name = args.save[0]
        company_name = args.save[1] if len(args.save) > 1 else None
        if company_name:
            company_name = search.resolve_company_argument(company_name)
            if company_name in data_source.get_company_names():
                save(list_name, company_name)
            else:
                print(f"'{company_name}' is not a valid company name.")
        else:
            save(list_name)
    elif args.unsave:
        list_name, company_name = args.unsave
        company_name = search.resolve_company_argument(company_name)
        unsave(list_name, company_name)
    elif args.show_saved:
        show_saved(args.show_saved)
    else:
        filters = {key: value for key, value in vars(args).items() if value is not None}
        filtered_data = QueryEngine.filter_data(data, **filters)

        if filtered_data:
            if args.verbose:
                print(f"Showing {len(filtered_data)} results:")

                urls_to_open = []
                for i, company in enumerate(filtered_data):
                    description = get_description_with_hyperlink(company)
                    url = company.get("website")
                    printout = f" - {description}"
                    if args.show_industry:
                        industries = company['industry'] if company['industry'] else ""
                        printout += f" {industries}"
                    if args.show_website:
                        website = company['website'] if company['website'] else ""
                        printout += f" {website}"

                    print(printout)
                    if args.open_links and url:
                        urls_to_open.append(url)

                search.clear_last_search_results()

            else:
                total_results = len(filtered_data)
                limit = max(1, args.limit)
                page = max(1, args.page)
                start_idx = (page - 1) * limit
                end_idx = start_idx + limit

                print(f"Showing results {start_idx + 1}-{min(end_idx, total_results)} out of {total_results}:")

                urls_to_open = []
                for i, company in enumerate(filtered_data[start_idx:end_idx]):
                    description = get_description_with_hyperlink(company)
                    url = company.get("website")
                    printout = f" - {description}"  # Prefer - over numbering, to make comm / diff work
                    if args.show_industry:
                        industries = company['industry'] if company['industry'] else ""
                        printout += f" {industries}"
                    if args.show_website:
                        website = company['website'] if company['website'] else ""
                        printout += f" {website}"

                    print(printout)
                    if args.open_links and url:
                        urls_to_open.append(url)

                if end_idx < total_results:
                    next_page_command = search.construct_next_page_command(args)
                    print(f"\nTo see more results, run:")
                    print(f"  {next_page_command}")

                search.save_last_search_results(filtered_data[start_idx:end_idx])

            if args.open_links and urls_to_open:
                print("\nOpening links in browser...")
                search.open_links_in_browser(urls_to_open)

        else:
            print("No matching companies found.")
            search.clear_last_search_results()


if __name__ == "__main__":
    main()
