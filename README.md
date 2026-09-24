# Eligiblity AI

Browser extension to look at scholarships as you search hubs, understanding every card through an LLM, and put it into a popup for the ones you'd be eligible for. The goal is no more wasted time on scholarships. Idea is a WIP.

## LLM backend

The backend compares supplied scholarship text against a student profile.
The extension is responsible for collecting that text; the endpoint does not
fetch URLs. Send one scholarship per request.

From the repository root in WSL:

```bash
python -m pip install -e .
python -m uvicorn backend.app:app --reload
```

Use the existing virtual environment or create and activate one first.
Set `OPENAI_API_KEY` in a root `.env` file or the process environment.
`LLM_MODEL` defaults to `gpt-4o-mini`. `ENV_FILE` overrides the dotenv path;
automatic root dotenv loading is limited to local/dev/development environments.
Keep the API key on the backend, never in the extension.

Open [interactive API docs](http://127.0.0.1:8000/docs) to try `POST /llm`:

```json
{
  "scholarship_text": "Full eligibility: Applicants must have a GPA of at least 3.0.",
  "student_profile": "My GPA is 3.5."
}
```

The response contains `status` (eligible, ineligible, or unknown),
`requirements` (each with a requirement, evidence quotes, status, and explanation),
`missing_information`, and `requirements_complete`.
Missing student evidence forces that requirement to unknown. A confirmed failed
requirement makes the overall result ineligible; otherwise missing facts,
incomplete rules, or no extracted requirements produce unknown.
The server checks that evidence quotes occur in the submitted inputs.
Exact quotes and structured output do not prove the model's interpretation is
correct. Assessments are preliminary and should be checked against official rules.

Invalid inputs return 422; unusable provider output returns 502, provider rate
limits return 503, and provider timeouts return 504.

Run offline checks from the repository root:

```bash
python -m unittest discover -s tests -v
```

These tests exercise mocked provider responses, not live model accuracy.
Before relying on filtering, evaluate real scholarship/profile examples,
including OR conditions, exceptions, incomplete cards, and hostile page text.
