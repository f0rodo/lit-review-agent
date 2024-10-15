import os
import hashlib
import json
from tqdm import tqdm
from openai import OpenAI
from src.models import PaperSummary, ConditionResult

# OpenAI client setup
client = OpenAI()

# Custom rule-based categorization logic for literature review
class CustomPolicyEngine:
    def __init__(self, rules, context, conditions_folder_path):
        """
        Initialize the CustomPolicyEngine.

        Args:
            rules (list): List of rules for evaluating papers.
            context (dict): Contextual information for quality criteria.
            conditions_folder_path (str): Path to store condition evaluations.
        """
        self.rules = rules
        self.context = context
        self.conditions_folder_path = conditions_folder_path

    def evaluate(self, paper):
        """
        Evaluate a paper against the defined rules.

        Args:
            paper (PaperSummary): Summary of the paper to evaluate.

        Returns:
            str: Category assigned to the paper.
        """
        for rule in tqdm(self.rules, desc="Evaluating Conditions"):
            condition_result = self.check_condition(paper, rule)
            if condition_result.condition_passes:
                return rule['category']
        return "Uncategorized"

    def check_condition(self, paper, rule):
        """
        Check if a given condition passes for the paper.

        Args:
            paper (PaperSummary): Summary of the paper.
            rule (dict): Rule to evaluate.

        Returns:
            ConditionResult: Result of the condition evaluation.
        """
        # Generate MD5 hash for the condition
        condition_hash = hashlib.md5((json.dumps(rule) + paper.title).encode('utf-8')).hexdigest()
        condition_file_path = os.path.join(self.conditions_folder_path, f"{condition_hash}.json")

        # Check if the condition evaluation already exists
        if os.path.exists(condition_file_path):
            with open(condition_file_path, "r") as f:
                condition_result = json.load(f)
                return ConditionResult(**condition_result['condition_result'])
        else:
            # Use OpenAI to evaluate the condition
            completion = client.beta.chat.completions.parse(
                model="gpt-4o-2024-08-06",
                messages=[
                    {"role": "system", "content": f"You are an AI agent determining if the following condition passes: {rule['agent_context']}. Provide the result as a JSON with the key 'condition_passes' as a boolean."},
                    {"role": "user", "content": paper.summary}
                ],
                response_format=ConditionResult,
            )

            condition_result = completion.choices[0].message.parsed

            # Save the condition result to a JSON file
            condition_data = {
                "paper_title": paper.title,
                "condition_text": rule['condition'],
                "condition_result": condition_result.dict()
            }
            with open(condition_file_path, "w") as f:
                json.dump(condition_data, f)

            return condition_result