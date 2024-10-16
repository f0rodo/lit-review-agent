import os
import logging
from paperscraper.pubmed import get_and_dump_pubmed_papers
from paperscraper.arxiv import get_and_dump_arxiv_papers
from paperscraper.xrxiv.xrxiv_query import XRXivQuery
from paperscraper.scholar import get_and_dump_scholar_papers
from paperscraper.pdf import save_pdf_from_dump

# Configurations for paths
PDFS_DIR = "./literature/pdfs"
DUMPS_DIR = "./literature/dumps"

def scrape_papers_from_sources(keyword_query, sources=['pubmed', 'arxiv', 'biorxiv', 'medrxiv', 'chemrxiv', 'scholar']):
    """
    Scrape papers from various sources based on the given keyword query.

    Args:
        keyword_query (list): List of keywords or keyword lists to use for searching papers.
        sources (list): List of sources to scrape from. Options include 'pubmed', 'arxiv', 'biorxiv', 'medrxiv', 'chemrxiv', 'scholar'.
    """
    logging.info("Starting paper scraping from various sources.")

    for source in sources:
        output_dir = os.path.join(DUMPS_DIR, source)
        os.makedirs(output_dir, exist_ok=True)
        
        if source == 'arxiv':
            output_file = os.path.join(output_dir, 'arxiv_papers.jsonl')
            logging.info(f"Scraping papers from arXiv with query: {keyword_query}")
            get_and_dump_arxiv_papers(keyword_query, output_filepath=output_file)

        # elif source in ['biorxiv', 'medrxiv', 'chemrxiv']:
        #     querier = XRXivQuery()
        #     output_file = os.path.join(output_dir, f"{source}_papers.jsonl")
        #     logging.info(f"Scraping papers from {source} with query: {keyword_query}")
        #     querier.search_keywords(keyword_query, output_filepath=output_file)

        # elif source == 'scholar':
        #     output_file = os.path.join(output_dir, 'scholar_papers.jsonl')
        #     logging.info(f"Scraping papers from Google Scholar with topic: {keyword_query}")
        #     get_and_dump_scholar_papers(keyword_query, output_filepath=output_file)

    logging.info("Paper scraping completed from all specified sources.")

def download_pdfs_from_metadata(metadata_file):
    """
    Download PDFs for the given metadata dump.

    Args:
        metadata_file (str): Path to the metadata JSONL file.
    """
    logging.info(f"Downloading PDFs from metadata file: {metadata_file}")
    os.makedirs(PDFS_DIR, exist_ok=True)
    save_pdf_from_dump(metadata_file, pdf_path=PDFS_DIR, key_to_save='doi')
    logging.info(f"PDF download completed. Saved to {PDFS_DIR}")

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Scrape papers and download PDFs based on keywords.")
    parser.add_argument('--query', type=str, nargs='+', required=True, help="Keywords for paper search.")
    parser.add_argument('--sources', type=str, nargs='+', default=['pubmed', 'arxiv', 'biorxiv', 'medrxiv', 'chemrxiv', 'scholar'], help="Sources to scrape from.")
    parser.add_argument('--download_pdfs', action='store_true', help="Flag to download PDFs after scraping metadata.")
    args = parser.parse_args()

    #scrape_papers_from_sources(args.query, args.sources)

    if args.download_pdfs:
        for source in args.sources:
            metadata_file = os.path.join(DUMPS_DIR, source, f"{source}_papers.jsonl")
            if os.path.exists(metadata_file):
                download_pdfs_from_metadata(metadata_file)