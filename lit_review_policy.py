import os
import argparse
import logging
import hashlib
import json
from datetime import datetime
from tqdm import tqdm
from openai import OpenAI
from src.paper_processing import extract_text_from_pdf
from src.policy_engine import CustomPolicyEngine
from src.models import PaperSummary, Demographics
from src.utils import ensure_folders_exist, clear_folder, load_rules
from src.report_generation import generate_report
from src.full_pipeline import run_full_pipeline

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Folder paths
folder_path = "./literature/pdfs"
parsed_folder_path = "./literature/parsed"
conditions_folder_path = "./literature/conditions"
reports_folder_path = "./literature/reports"

# OpenAI client setup
client = OpenAI()

# Ensure parsed, conditions, and reports folders exist
ensure_folders_exist([parsed_folder_path, conditions_folder_path, reports_folder_path])

# Load custom rules from policy.json
rules = load_rules('./literature/policy.json')

# Create context information for policy engine
context = {
    "quality_criteria": "Quality is determined based on the type of evidence, such as systematic reviews, RCTs, and expert opinions. Additional factors include methodological rigor and sample size."
}

# Initialize custom policy engine
policy_engine = CustomPolicyEngine(rules, context, conditions_folder_path=conditions_folder_path)

# Main function
def main():
    parser = argparse.ArgumentParser(description="Literature Review Policy Engine", add_help=True)
    parser.add_argument("--clear", choices=['conditions', 'parsed'], help="Clear cached conditions or parsed summaries")
    parser.add_argument("--list", action="store_true", help="List all processed papers and their categories")
    parser.add_argument("--report", action="store_true", help="Generate a summary report of all processed papers in tabular format")
    parser.add_argument("--full_pipeline", action="store_true", help="Run the full pipeline to process PDFs and evaluate them")
    args = parser.parse_args()

    # Clear specified folder if --clear is used
    if args.clear:
        folder_to_clear = conditions_folder_path if args.clear == 'conditions' else parsed_folder_path
        clear_folder(folder_to_clear)
        logging.info(f"Cleared all files in {folder_to_clear}")

    if args.list:
        # List all processed papers and their results
        for filename in os.listdir(parsed_folder_path):
            if filename.endswith(".json"):
                with open(os.path.join(parsed_folder_path, filename), "r") as f:
                    summary_data = json.load(f)
                    paper = PaperSummary(**summary_data)
                    category = policy_engine.evaluate(paper)
                    logging.info(f"Paper: {paper.title}\nCategory: {category}\n")
    elif args.report:
        # Generate a summary report of all processed papers in tabular format
        generate_report(parsed_folder_path, folder_path, rules, policy_engine, reports_folder_path)
    elif args.full_pipeline:
        # Run the full pipeline to process PDFs and evaluate them
        run_full_pipeline(folder_path, parsed_folder_path, context, rules, policy_engine, client)

if __name__ == "__main__":
    main()