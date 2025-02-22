import json
import os

from careerfit.globals import SAVE_DIR, LAST_SEARCH_RESULTS_FILE

SAVE_DIR.mkdir(exist_ok=True)

def get_saved(username):
    """Returns the path of the user's list file."""
    file_path = SAVE_DIR / f"{username}.txt"
    file_path.touch(exist_ok=True)
    return file_path

def save(username, company_name=None):
    """Adds a company (or last search's results) to a user's list of saved companies."""
    file_path = get_saved(username)

    with file_path.open("r") as f:
        existing = {line.strip() for line in f}

        if company_name is None:
            if not os.path.exists(LAST_SEARCH_RESULTS_FILE):
                print("No previous search results found. Run a search first.")
                return

            with open(LAST_SEARCH_RESULTS_FILE, "r") as f:
                company_data = json.load(f)

            new_companies = {company["name"] for company in company_data}

            if not new_companies:
                print("Last command was not a search, no companies to add.")
                return

        else:
            new_companies = {company_name}

        new_companies = new_companies - existing

        if new_companies:
            with open(file_path, "a") as f:
                for company in new_companies:
                    f.write(company + "\n")
            if company_name:
                print(f"Saved {company_name} to {username}.")
            else:
                print(f"Saved {len(new_companies)} new companies to {username}.")
        else:
            if company_name:
                print(f"{company_name} is already saved for {username}.")
            else:
                print("All selected companies are already saved.")

def unsave(list_name, company_name):
    """Removes a company from a user's list of saved companies."""
    file_path = get_saved(list_name)

    if not os.path.exists(file_path):
        print(f"{list_name} has no saved companies.")
        return

    with open(file_path, "r") as f:
        companies = [line.strip() for line in f if line.strip()]

    if company_name in companies:
        companies.remove(company_name)

        with file_path.open("w") as f:
            if companies:
                f.write("\n".join(companies) + "\n")
            else:
                f.write("")

        print(f"Removed {company_name} from {list_name}'s list of saved companies.")
    else:
        print(f"{company_name} was not found in {list_name}'s list of saved companies.")

def show_saved(name):
    """Displays a user's saved companies."""
    file_path = get_saved(name)

    if not os.path.exists(file_path):
        print(f"{name} has no saved companies.")
        return

    with open(file_path, "r") as f:
        companies = [line.strip() for line in f]

    if companies:
        print(f"{name}'s saved companies:")
        for company in companies:
            print(f"{company}")
    else:
        print(f"{name}'s list of saved companies is empty.")
