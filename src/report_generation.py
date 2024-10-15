import os
import json
import logging
import pandas as pd
from datetime import datetime
from src.models import PaperSummary

# Utility function to generate a report from processed papers
def generate_report(parsed_folder_path, folder_path, rules, policy_engine, reports_folder_path):
    """
    Generate a summary report of all processed papers in tabular format.

    Args:
        parsed_folder_path (str): Path to the folder containing parsed summaries.
        folder_path (str): Path to the folder containing original PDFs.
        rules (list): List of rules for evaluating papers.
        policy_engine (CustomPolicyEngine): Policy engine instance.
        reports_folder_path (str): Path to save the report.
    """
    report_data = []
    for filename in os.listdir(parsed_folder_path):
        if filename.endswith(".json"):
            with open(os.path.join(parsed_folder_path, filename), "r") as f:
                summary_data = json.load(f)
                paper = PaperSummary(**summary_data)
                paper_data = {
                    "paper_title": paper.title,
                    "paper_path": os.path.join(folder_path, filename.replace(".json", ".pdf")),
                    "summary": paper.summary,
                    "publication_date": paper.publication_date,
                    "authors": ", ".join(paper.authors),
                    "quality": paper.quality,
                    "populations": paper.populations,
                    "disorder_subtype": ", ".join(paper.disorder_subtype),
                    "treatment_type": ", ".join(paper.treatment_type),
                    "evidence_level": ", ".join(paper.evidence_level),
                    "date": datetime.now().strftime('%Y-%m-%d')
                }
                # Evaluate each condition for the paper
                for rule in rules:
                    condition_result = policy_engine.check_condition(paper, rule)
                    condition_key = rule['condition'].replace(" ", "_").replace("'", "").lower()
                    paper_data[condition_key] = "pass" if condition_result.condition_passes else "not pass"
                report_data.append(paper_data)
    
    # Create a DataFrame and print it
    df = pd.DataFrame(report_data)
    logging.info(df)

    # Save the report to a CSV file with the current date
    report_filename = f"report_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.csv"
    report_file_path = os.path.join(reports_folder_path, report_filename)
    df.to_csv(report_file_path, index=False)
    logging.info(f"Report saved to {report_file_path}")

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')