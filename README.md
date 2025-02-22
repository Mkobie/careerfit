# careerfit

This is a command-line tool that you can use to find some companies that could be a good fit for you, depending on your needs and priorities.

The data that the tool looks through was collected as follows:
* Company names were scraped from [the Dutch IND website that lists companies that can sponsor highly skilled migrants](https://ind.nl/en/public-register-recognised-sponsors/public-register-regular-labour-and-highly-skilled-migrants) (see careerfit/scraping)
* [OpenAi](https://platform.openai.com/) tried its best to provide some info about each company - it's industry, values, typical jobs etc (see careerfit/batch_population; note: you need a OpenAI key for this.)

At the moment the tool is targeted towards my own preferences (embedded, c++, python, randstad), but feel free to extend it to suit your needs!

## Features

- Search for companies using various filters (e.g., industry, job types).
- Maintain a personal list of interesting companies.

## Installation

Make sure you have Python 3.8+ installed, then clone the repository, install dependencies, and run the setup script to unpack the company data files:
```bash
git clone https://github.com/Mkobie/careerfit.git
cd careerfit
pip install -r requirements.txt
./setup.sh
```

Install careerfit in a virtual environment, and try it out!

```bash
python -m venv .venv       # Make your virtual environment
source .venv/bin/activate  # On Linux/macOS/WSL2
.venv\Scripts\activate     # On Windows (cmd or PowerShell)

pip install -e .           # Install the CLI tool
careerfit --help
```
## Usage: search and save

Search through the 11000+ companies using boolean flags like so:

```bash
careerfit --randstad    # To filter companies that (probably) have a location in the Randstad area of the Netherlands
careerfit --python      # To filter companies that (probably) hire people to code using python
careerfit --c           # To filter companies that (probably) hire people to code using c or c++
careerfit --software    # To filter companies that (probably) have software jobs
careerfit --embedded    # To filter companies that (probably) have embedded jobs
careerfit --english     # To filter companies that (probably) have english-only jobs
careerfit --englishish  # Fuzzier version of the previous search - includes places where certainty is even lower
careerfit --global      # To filter companies that (probably) have locations outside of the Netherlands as well
```

Or more interactive flags (although the data set isn't so robust that you're guaranteed to get any good results).
```bash
careerfit --industry marine 
careerfit --values innovation 
```

By default 5 results will be returned per page. You can change this to suit your preference:
```bash
careerfit --limit 10    # To show 10 results per page
careerfit --verbose     # To show alllll the results in one go
```

You can also change how results are shown (just a bit):
```bash
careerfit --show-links      # This will show the companies url at the end.
careerfit --show-industry   # This will show a list of the company's industry (probably) at the end 
```

Have I mentioned that the company name at the start of the description is a clickable link?
You can also use a flag to open the sites of all the results automatically for you (proceed with caution if you use the verbose flag here)
```bash
careerfit --open-links      # This will show the first 5 entries companies, and open links for them!
```

That's nice and all, but can I keep track of interesting companies somehow?
Of course, that's what paper and pencils are for!
Just kidding, this CLI has some small offerings in that area too.
If you like a company, save it to a list.
```bash
careerfit --save my_list_name company_of_interest_name    # Save a company for future reference
careerfit --unsave my_list_name company_of_interest_name  # You can unsave companies too
careerfit --show-saved my_list_name                       # And view the names you've saved
```

But if like me you get tired of typing out company names (and spelling them wrong), you can save companies by their position in the list returned by careerfit.
```bash
careerfit --save my_list_name 1   # To save the first company returned by careerfit on a given page
```

If all the companies on a page look good to you, you can add them all to your list:
```bash
careerfit --python              # If these 5 companies all look good to you, then...
careerfit --save my_list_name   # ...add them all to your list by leaving out the 2nd save argument!
```

If you get so into this that your list becomes long enough you want to search it instead of the full IND cornucopia, you can set your own list as a data source.
```bash
careerfit --source my_list_name --python  # To filter just the python companies from your personal list
```

Phew that's already a lot. But wait, there's more!

## Usage: admin

Admin functions are pretty much just
* Seeing what's stored in a company's json key
* Changing the stored value

To do this, use the `careerfit-admin` command, and specify the company, field, and (if editing) the new value:
```bash
careerfit-admin --company "Company to edit" --field website --value https://www.CorrectUrl.com
careerfit-admin --company 1 --field english --value no  # Referring to search results by number works here too
```
