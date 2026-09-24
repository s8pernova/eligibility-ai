"""Offline tests for eligibility decisions and provider failure handling."""

import unittest
from types import SimpleNamespace
from unittest.mock import Mock

from fastapi.testclient import TestClient

from backend.app import app
from backend.clients import get_openai_client
from backend.models.llm import EligibilityAnalysis, LLMRequest, RequirementAssessment
from backend.services.llm import LLMOutputError, prompt


class EligibilityTests(unittest.TestCase):
    def setUp(self):
        self.request = LLMRequest(
            scholarship_text="Full eligibility: Applicants must have a GPA of at least 3.0.",
            student_profile="My GPA is 3.5.",
        )
        self.analysis = EligibilityAnalysis(
            requirements=[
                RequirementAssessment(
                    requirement="GPA of at least 3.0",
                    scholarship_evidence="Applicants must have a GPA of at least 3.0.",
                    student_evidence="My GPA is 3.5.",
                    status="eligible",
                    explanation="3.5 exceeds 3.0.",
                )
            ],
            missing_information=[],
            requirements_complete=True,
        )
        self.client = Mock()
        self.message = SimpleNamespace(parsed=self.analysis, refusal=None)
        self.client.chat.completions.parse.return_value = SimpleNamespace(
            choices=[SimpleNamespace(message=self.message)]
        )

    def assess(self):
        return prompt(self.client, self.request, "gpt-4o-mini")

    def test_complete_satisfied_rules_are_eligible(self):
        self.assertEqual(self.assess().status, "eligible")
        arguments = self.client.chat.completions.parse.call_args.kwargs
        self.assertEqual(arguments["response_format"], EligibilityAnalysis)
        self.assertEqual(
            arguments["messages"][1]["content"], self.request.model_dump_json()
        )

    def test_missing_student_evidence_cannot_prove_eligibility(self):
        self.analysis.requirements[0].student_evidence = None
        result = self.assess()
        self.assertEqual(result.status, "unknown")
        self.assertEqual(result.requirements[0].status, "unknown")

    def test_missing_student_evidence_cannot_prove_ineligibility(self):
        self.analysis.requirements[0].student_evidence = None
        self.analysis.requirements[0].status = "ineligible"
        self.assertEqual(self.assess().status, "unknown")

    def test_incomplete_card_is_unknown(self):
        self.analysis.requirements_complete = False
        self.assertEqual(self.assess().status, "unknown")

    def test_no_requirements_is_unknown(self):
        self.analysis.requirements = []
        self.assertEqual(self.assess().status, "unknown")

    def test_missing_information_is_unknown(self):
        self.analysis.missing_information = ["Enrollment status"]
        self.assertEqual(self.assess().status, "unknown")

    def test_explicit_failure_takes_precedence(self):
        self.request.student_profile = "My GPA is 2.5."
        item = self.analysis.requirements[0]
        item.student_evidence = "My GPA is 2.5."
        item.status = "ineligible"
        item.explanation = "2.5 is below 3.0."
        self.analysis.requirements_complete = False
        self.assertEqual(self.assess().status, "ineligible")

    def test_fabricated_quotes_are_rejected(self):
        for field in ("scholarship_evidence", "student_evidence"):
            with self.subTest(field=field):
                item = self.analysis.requirements[0]
                original = getattr(item, field)
                setattr(item, field, "Invented evidence")
                with self.assertRaises(LLMOutputError):
                    self.assess()
                setattr(item, field, original)

    def test_unusable_provider_outputs_are_rejected(self):
        for parsed, refusal in ((None, None), (None, "Refused")):
            with self.subTest(refusal=refusal):
                self.message.parsed = parsed
                self.message.refusal = refusal
                with self.assertRaises(LLMOutputError):
                    self.assess()
        self.client.chat.completions.parse.return_value.choices = []
        with self.assertRaises(LLMOutputError):
            self.assess()

    def test_http_contract(self):
        app.dependency_overrides[get_openai_client] = lambda: self.client
        self.addCleanup(app.dependency_overrides.clear)
        with TestClient(app) as http:
            response = http.post("/llm", json=self.request.model_dump())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json()["status"], "eligible")
            for bad in (
                {"scholarship_text": " ", "student_profile": "profile"},
                {"scholarship_text": "rules"},
                {"response": "old input"},
            ):
                self.assertEqual(http.post("/llm", json=bad).status_code, 422)
            self.message.parsed = None
            self.assertEqual(
                http.post("/llm", json=self.request.model_dump()).status_code, 502
            )


if __name__ == "__main__":
    unittest.main()
