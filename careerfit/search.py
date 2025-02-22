import json
import os
import shlex
import subprocess
import webbrowser

from careerfit.globals import LAST_SEARCH_RESULTS_FILE


def save_last_search_results(search_results):
    """Saves the last search results to a temporary file."""
    with open(LAST_SEARCH_RESULTS_FILE, "w") as f:
        json.dump(search_results, f, indent=4)

def clear_last_search_results():
    with open(LAST_SEARCH_RESULTS_FILE, "w") as f:
        f.write("")

def construct_next_page_command(args):
    """
    Constructs a command string for fetching the next page with the same filters.
    """
    base_command = ["careerfit"]

    # Add all non-default filters
    for key, value in vars(args).items():
        if key not in ["command", "limit", "page"] and value:
            if isinstance(value, bool) and value:
                base_command.append(f"--{key}")
            elif isinstance(value, str) or isinstance(value, int):
                base_command.append(f"--{key} {shlex.quote(str(value))}")

    base_command.append(f"--page {args.page + 1}")

    return " ".join(base_command)

def open_links_in_browser(urls):
    """
    Tries to open a list of URLs in the default web browser.
    If the default fails, tries alternative methods.
    """
    urls = urls[::-1]
    if "WSL_DISTRO_NAME" in os.environ:  # Check if running inside WSL
        for url in urls:
            try:
                subprocess.run(["wslview", url], check=True)
            except FileNotFoundError:
                # If wslview is not available, fallback to PowerShell
                subprocess.run(["powershell.exe", "Start-Process", url], check=True, shell=True)
    else:
        # Normal Linux/Mac behavior
        try:
            browser = webbrowser.get()
            for url in urls:
                browser.open(url, new=2)  # Open in new tab
        except Exception:
            try:
                browser = webbrowser.get("firefox")
                for url in urls:
                    browser.open(url, new=2)
            except Exception as e:
                print(f"Could not open URLs: {e}")

def get_last_search_results():
    """Load the last search results from file."""
    if LAST_SEARCH_RESULTS_FILE.exists():
        return json.loads(LAST_SEARCH_RESULTS_FILE.read_text())
    return []

def resolve_company_argument(company_arg):
    """
    Resolve company argument to its name.
    If it's a number, fetch the corresponding company from last search results.
    """
    if company_arg.isdigit():
        last_results = get_last_search_results()
        index = int(company_arg) - 1
        if 0 <= index < len(last_results):
            return last_results[index]["name"]
        else:
            print(f"Error: Index {company_arg} is out of range (1-{len(last_results)}).")
            exit(1)
    return company_arg  # Return as-is if not a number
