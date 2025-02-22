import time
from pathlib import Path

import openai


def upload_batch_input_file(jsonl_file):
    """
    Uploads a batch input file to OpenAI.
    """
    response = openai.files.create(
        file=open(jsonl_file, "rb"),
        purpose="batch"
    )
    print(f"File uploaded. ID: {response.id}")
    print(f"    {response}")
    return response.id


def submit_batch_request(jsonl_file_id):
    """
    Submits a batch request to OpenAI.
    """
    response = openai.batches.create(
        input_file_id=jsonl_file_id,
        endpoint="/v1/chat/completions",
        completion_window="24h"
    )

    print(f"Batch job started. ID: {response.id}")
    print(f"    {response}")
    return response.id


def monitor_batch_status(batch_id):
    """
    Monitors the batch request and waits for completion.
    """
    while True:
        response = openai.batches.retrieve(batch_id)
        status = response.status

        if status in ["completed", "failed"]:
            print(f"Batch job {batch_id} finished with status: {status}; results are in {response.output_file_id}")
            print(f"    {response}")
            return response.output_file_id or response.error_file_id

        print(f"Batch job {batch_id} is still {status}... Checking again in 60 seconds.")
        time.sleep(60)

def get_error_results(error_file_id):
    error_filename = "batch_errors.jsonl"

    response = openai.files.content(error_file_id)
    print(response)

    with open(error_filename, "w", encoding="utf-8") as file:
        file.write(response.text)
    print(f"Batch errors saved as {error_filename}")


def download_results_to_file(output_file_id, results_file: Path):
    """
    Downloads the results from OpenAI's Batch API and saves them to a local file.
    """
    if results_file.exists():
        results_file.unlink()
        print(f"Deleted previous results file: {results_file}")

    response = openai.files.content(output_file_id)
    print(f"Download started of output file. ID: {output_file_id}")
    print(f"    {response}")

    with open(results_file, "w", encoding="utf-8") as file:
        file.write(response.text)

    if results_file.exists() and results_file.stat().st_size > 0:
        print(f"Batch results successfully saved in {results_file}")
        return True
    else:
        print(f"Download failed: File {results_file} is empty or missing.")
        return False

def clean_up_openai_files():
    files = openai.files.list()
    print(files)

    for file in files.data:
        openai.files.delete(file.id)
        print(f"Deleted file: {file.id} ({file.filename})")

    print(openai.files.list())
