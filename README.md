# Literature Review Policy Engine

This README provides an overview of how to use the Literature Review Policy Engine to evaluate research papers based on custom policies, generate summaries, and create reports.

![Showing an image of a spreadsheet and how you can filter based on policy conditions.](./docs/ExampleReport.png "Lit Review Report")

## Requirements

- Python 3.12+
- Virtual environment (optional but recommended)

### Python Packages

To install the required packages, run:

```bash
poetry install
```

To manage dependencies, this project uses Poetry. Run `poetry install` to create the virtual environment and install all dependencies.
## Folder Structure

- `./literature/pdfs` - Folder where all PDF documents are stored.
- `./literature/parsed` - Folder to store parsed summaries of the papers.
- `./literature/conditions` - Folder to store condition evaluations for papers.
- `./literature/reports` - Folder to store generated summary reports.
- `./literature/policy.json` - Policy file where categorization rules are defined.

## Running the Script

The main script (`lit_review_policy.py`) can be used to parse research papers, evaluate them based on defined policies, and generate reports. Below are the different command line options available:

### Arguments

- `--full_pipeline`
  - Runs the full pipeline to parse papers, evaluate conditions, and generate summaries.

- `--clear [conditions|parsed]`
  - Clears the cached conditions or parsed summaries from the respective folders.

- `--list`
  - Lists all processed papers and their evaluated categories.

- `--report`
  - Generates a summary report of all processed papers in tabular format.

### Example Commands

- **Clear Parsed Summaries**:
  ```bash
  python lit_review_policy.py --clear parsed
  ```

- **List Processed Papers**:
  ```bash
  python lit_review_policy.py --list
  ```

- **Generate a Report**:
  ```bash
  python lit_review_policy.py --report
  ```

## Policy Setup

The categorization logic for the literature review is defined in the `policy.json` file. This file contains an array of rules, where each rule includes:

- `condition`: A natural language description of what condition the paper must satisfy (e.g., "The evidence level is 'RCT'").
- `category`: The category assigned if the condition passes (e.g., "Moderate Quality Study").
- `agent_context`: Context to guide the AI in evaluating the condition.

### Example Policy Entry

```json
{
  "condition": "The evidence level is either 'systematic review' or 'meta-analysis'.",
  "category": "High Quality Study",
  "agent_context": "Determine if the paper evidence is systematic review or meta analysis. Add this to evidence_level."
}
```

## How to Add or Modify Policies

1. Open the `policy.json` file in a text editor.
2. Add new rules following the format mentioned above.
3. Save the file.

The script will use the updated policies to categorize papers accordingly.

## Example Workflow

1. **Add PDFs**: Place the research papers in the `./literature/pdfs` folder.
2. **Run Script**: Use `python lit_review_policy.py --full_pipeline` with the appropriate arguments to parse the papers and generate summaries.
3. **Generate Report**: After processing the papers, generate a report using `--report` to get an overview of the categorization.

## Customization

- **Custom Policy Engine**: The categorization logic can be extended by adding more detailed policies or modifying the existing ones.
- **Demographics and Details**: You can add or modify demographic information by editing the `Demographics` and `Details` models to fit the data you want to capture.

## Troubleshooting

- **Validation Errors**: Ensure that the JSON structure in `policy.json` matches the format expected by the script.
- **API Errors**: Make sure your OpenAI API key is correctly set up and has access to the required models.


# Paper Scraper Module

This module provides functionality to scrape research papers from multiple sources based on a keyword search and optionally download the corresponding PDFs. It supports sources like PubMed, arXiv, bioRxiv, medRxiv, chemRxiv, and Google Scholar.


## Usage
The script can be used to scrape papers and optionally download PDFs.

### Command Line Arguments
- `--query` (required): Keywords for the paper search. Accepts multiple keywords.
- `--sources` (optional): Specify sources to scrape from. Options include `pubmed`, `arxiv`, `biorxiv`, `medrxiv`, `chemrxiv`, and `scholar`. Default is all sources. **NOTE** There is a bug with every source but arxiv
- `--download_pdfs` (optional): Use this flag to download PDFs after scraping the metadata.

### Example
To scrape papers related to "COVID-19" and "Artificial Intelligence" from arXiv, and download their PDFs:

```sh
python fetch_papers.py --query "COVID-19" "Artificial Intelligence" --sources arxiv --download_pdfs
```

This command will:
1. Scrape metadata from arXiv using the specified keywords.
2. Save the metadata dumps in `literature/dumps/arxiv`.
3. Download the PDFs for the retrieved papers and store them in `literature/pdfs`.

## Logging
The script uses Python's logging module to provide information during the scraping and downloading process.
- Logs are displayed on the console, showing the progress of the scraping and PDF downloads.

## Troubleshooting
- **ModuleNotFoundError: No module named 'pkg_resources'**: This error indicates that `setuptools` is not installed. Install it using:
  ```sh
  pip install setuptools
  ```



## License

This project is licensed under the MIT License.

