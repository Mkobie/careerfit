from pathlib import Path

data_dir = Path(__file__).resolve().parent.parent / "data"
COMPANIES_DIR = data_dir / "companies"
ORG_LIST_FILE = data_dir / "organizations_from_ind.txt"
SAVE_DIR = data_dir / "saved_lists"
LAST_SEARCH_RESULTS_FILE = data_dir / "careerfit_last_search.txt"
