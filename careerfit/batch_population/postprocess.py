import json
from pathlib import Path

from careerfit.batch_population.locals import REQUESTS_FILE, RESULTS_FILE
from careerfit.batch_population.vet_links import post_process_links


def process_downloaded_results(results_file: Path, output_folder: Path):
    """
    Reads and processes the results stored in the local JSONL file.
    """
    if not results_file.exists():
        print(f"Results file {results_file} not found. Please download it first.")
        return

    with open(results_file, "r", encoding="utf-8") as file:
        for line in file:
            try:
                result = json.loads(line)

                content_str = result["response"]["body"]["choices"][0]["message"]["content"]
                company_info = json.loads(content_str)

                filename = f"{company_info['name'].replace(' ', '_')}.json"
                output_path = output_folder / filename

                if not output_path.exists():
                    company_info = post_process_links(company_info)

                    with open(output_path, "w", encoding="utf-8") as file:
                        json.dump(company_info, file, indent=4, ensure_ascii=False)
                    print(f"Results from {results_file} have been populated in {output_path}")

            except (json.JSONDecodeError, KeyError) as e:
                print(f"Error processing line: {line}\nError: {e}")

def clean_up_local_files():
    if REQUESTS_FILE.exists():
        REQUESTS_FILE.unlink()
    if RESULTS_FILE.exists():
        RESULTS_FILE.unlink()
