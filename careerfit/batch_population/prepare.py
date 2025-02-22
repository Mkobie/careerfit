import json
import re

from careerfit.batch_population.locals import REQUESTS_FILE


def create_jsonl_file(file_path, start_line, stop_line):
    """
    Reads a list of company names from a file and creates a JSONL file for batch processing.
    """
    with open(file_path, "r", encoding="utf-8") as file:
        companies = file.readlines()

    start_line = max(1, start_line)
    stop_line = min(len(companies), stop_line)
    if stop_line == start_line:
        stop_line += 1

    jsonl_data = []
    for i in range(start_line - 1, stop_line):
        company_name = companies[i].strip()

        if company_name:
            company_name = re.sub(r'[<>:"/\\|?*]', '', company_name).replace(" B.V.", "")
            request_data = {
                "custom_id": f"request-{i+1}",
                "method": "POST",
                "url": "/v1/chat/completions",
                "body": {"model": "gpt-4o-mini",
                         "messages": [{"role": "system",
                                       "content": "You are an assistant that formats company details into a structured JSON format. "
                                                    "Respond only with valid JSON, nothing else."},
                                      {"role": "user",
                                       "content": f"Fetch detailed company information for '{company_name}' in the Netherlands and return it as a valid JSON object "
                                                    "in the following structure:\n\n"
                                                    "{\n"
                                                    '  "name": "Company Name",\n'
                                                    '  "industry": ["Industry1", "Industry2"],\n'
                                                    '  "values": ["Value1", "Value2"],\n'
                                                    '  "description": "Brief company description",\n'
                                                    '  "website": "Link to company website",\n'
                                                    '  "linkedin job page": "Link to LinkedIn jobs page for the company",\n' 
                                                    '  "types of jobs": ["Job1", "Job2"],\n'
                                                    '  "has software or programming jobs": "yes/no/unsure",\n'
                                                    '  "has embedded programming jobs": "yes/no/unsure",\n'
                                                    '  "has python jobs": "yes/no/unsure",\n'
                                                    '  "has c or c++ jobs": "yes/no/unsure",\n'
                                                    '  "dutch is required": "yes/no/unsure",\n'
                                                    '  "has location in the randstad": "yes/no/unsure",\n'
                                                    '  "countries with offices": ["Netherlands", "Country2"],\n'
                                                    '  "size": 0,\n'
                                                    '  "IND sponsor": "yes"\n'
                                                    "}\n\n"
                                                    "If you are unsure about any information, leave the entry blank. "
                                                    "Start the description with the company name at the front."
                                       }],
                         "max_tokens": 5000,
                         "response_format": { "type": "json_object" }
                }
            }

            jsonl_data.append(json.dumps(request_data))

    with open(REQUESTS_FILE, "w", encoding="utf-8") as jsonl_file:
        jsonl_file.write("\n".join(jsonl_data))

    print(f"Created batch request file: {REQUESTS_FILE.name}")
    return REQUESTS_FILE
