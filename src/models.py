from typing import List
from pydantic import BaseModel

class Details(BaseModel):
    detail: str
    value: str
    description: str

class Demographics(BaseModel):
    population_size: int = None
    min_age: int = None
    max_age: int = None
    gender: int = None
    inclusion_criteria: List[Details]
    exclusion_criteria: List[Details]
    other_details: List[Details]

class PaperSummary(BaseModel):
    title: str
    summary: str
    publication_date: str
    authors: list[str]
    quality: str  # Generalized quality measure (determined by agent context)
    populations: List[Demographics]
    disorder_subtype: list[str]
    treatment_type: list[str]
    evidence_level: list[str]

class ConditionResult(BaseModel):
    condition_passes: bool
    relevant_snippets: list[str]