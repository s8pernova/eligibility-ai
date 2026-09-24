# API contract: extension <-> LLM backend

Both sides must match this. Talk before changing it.

## Request

`POST /api/extract`

```json
{ "url": "https://example.org/scholarship", "page_text": "full visible text of the page" }
```

`page_text` is trimmed to 20,000 characters by the extension.

## Response (200)

```json
{
  "scholarship_name": "Example STEM Scholarship",
  "deadline": "2026-12-01",
  "criteria": {
    "min_gpa": 3.0,
    "majors": ["Computer Science", "Engineering"],
    "states": ["VA"],
    "enrollment": "full-time",
    "other": ["Essay on leadership experience"]
  }
}
```

Rules:
- Use `null` for anything the page doesn't mention (not 0, not "").
- `deadline` is `YYYY-MM-DD` or `null`.
- `states` uses two-letter codes.
- `enrollment` is `"full-time"`, `"part-time"`, or `null`.
- `other` is always a list (empty if nothing), for requirements that can't be checked automatically.

## Errors

Return a non-200 status; the extension shows a generic error message.

## Local dev

The backend runs at `http://localhost:8000`. It needs CORS enabled for the extension
(e.g. in FastAPI, `CORSMiddleware` with `allow_origins=["*"]` during development).
If the backend moves, update `API_URL` in `extension/config.js` and
`host_permissions` in `extension/manifest.json`.
