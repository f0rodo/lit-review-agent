import os
import hashlib
import json
import logging
from tqdm import tqdm
from openai import OpenAI
from src.paper_processing import extract_text_from_pdf
from src.models import PaperSummary, Demographics

# Function to run the full pipeline of processing PDFs and evaluating them
def run_full_pipeline(folder_path, parsed_folder_path, context, rules, policy_engine, client):
    """
    Run the full pipeline to process PDFs and evaluate them.

    Args:
        folder_path (str): Path to the folder containing original PDFs.
        parsed_folder_path (str): Path to the folder to store parsed summaries.
        context (dict): Contextual information for quality criteria.
        rules (list): List of rules for evaluating papers.
        policy_engine (CustomPolicyEngine): Policy engine instance.
        client (OpenAI): OpenAI client instance.
    """
    papers = []
    for filename in tqdm(os.listdir(folder_path), desc="Processing PDFs"):
        if filename.endswith(".pdf"):
            file_path = os.path.join(folder_path, filename)
            text = extract_text_from_pdf(file_path)

            # Generate MD5 hash of the context and text
            md5_hash = hashlib.md5((text + json.dumps(context)).encode('utf-8')).hexdigest()
            parsed_file_path = os.path.join(parsed_folder_path, f"{md5_hash}.json")

            # Check if the summary already exists
            if os.path.exists(parsed_file_path):
                with open(parsed_file_path, "r") as f:
                    summary_data = json.load(f)
                    summary_data['populations'] = list(map(lambda p: Demographics(**p), summary_data.get('populations', [])))
                summary = PaperSummary(**summary_data)
            else:
                # Inject agent context from rules into OpenAI prompt
                agent_context = "\n".join([rule['agent_context'] for rule in rules])
                completion = client.beta.chat.completions.parse(
                    model="gpt-4o-2024-08-06",
                    messages=[
                        {"role": "system", "content": f"You are an AI summarizing research papers. Use the following context to guide your summary:\n{agent_context}"},
                        {"role": "user", "content": text}
                    ],
                    response_format=PaperSummary,
                )

                summary = completion.choices[0].message.parsed

                # Save the summary to a JSON file
                with open(parsed_file_path, "w") as f:
                    json.dump(summary.dict(), f)

            papers.append(summary)

    # Evaluate each paper against the custom policy engine
    for paper in tqdm(papers, desc="Evaluating Papers"):
        logging.info(f"Evaluating paper: {paper.title}")
        logging.info(f"Input data: {paper}")
        category = policy_engine.evaluate(paper)
        logging.info(f"Evaluation result: {category}")
        logging.info(f"Paper: {paper.title}\nCategory: {category}\n")