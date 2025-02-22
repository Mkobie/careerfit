import openai

from careerfit.globals import ORG_LIST_FILE, COMPANIES_DIR
from careerfit.batch_population import openai_batch
from careerfit.batch_population import postprocess
from careerfit.batch_population import prepare
from careerfit.batch_population.locals import REQUESTS_FILE, RESULTS_FILE

if __name__ == "__main__":
    if not REQUESTS_FILE.exists():
            print(f"Creating {REQUESTS_FILE.name} from {ORG_LIST_FILE.name}")
            jsonl_file = prepare.create_jsonl_file(ORG_LIST_FILE, 1, 1)

            print(f"Getting AI results via {REQUESTS_FILE.name}, saving them to {RESULTS_FILE.name}")
            file_id = openai_batch.upload_batch_input_file(REQUESTS_FILE)
            batch_id = openai_batch.submit_batch_request(file_id)

    if REQUESTS_FILE.exists():
            batch = openai.batches.list()
            output_file_id = openai_batch.monitor_batch_status(batch.data[0].id)
            if output_file_id:
                print(f"Downloading {output_file_id} results to {RESULTS_FILE}.")
                success = openai_batch.download_results_to_file(output_file_id, RESULTS_FILE)

    if RESULTS_FILE.exists():
            print(f"Processing results in {RESULTS_FILE.name}, filling company data in in {COMPANIES_DIR.name}")
            postprocess.process_downloaded_results(RESULTS_FILE, COMPANIES_DIR)

            openai_batch.clean_up_openai_files()
            postprocess.clean_up_local_files()
