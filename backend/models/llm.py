"""Scholarship eligibility request and response schemas."""

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

EligibilityStatus = Literal["eligible", "ineligible", "unknown"]


class LLMRequest(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    scholarship_text: str = Field(min_length=1, max_length=50000)
    student_profile: str = Field(min_length=1, max_length=20000)


class RequirementAssessment(BaseModel):
    requirement: str
    scholarship_evidence: str
    student_evidence: str | None
    status: EligibilityStatus
    explanation: str


class EligibilityAnalysis(BaseModel):
    requirements: list[RequirementAssessment]
    missing_information: list[str]
    requirements_complete: bool = Field(
        description="Whether the supplied text contains the full eligibility rules, "
        "rather than a card, summary, or reference to rules elsewhere."
    )


class LLMResponse(EligibilityAnalysis):
    status: EligibilityStatus
