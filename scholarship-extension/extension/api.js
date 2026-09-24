// Talks to the LLM backend. Must match docs/api-contract.md.

const MOCK_RESPONSE = {
  scholarship_name: "Example STEM Scholarship",
  deadline: "2026-12-01",
  criteria: {
    min_gpa: 3.0,
    majors: ["Computer Science", "Engineering"],
    states: ["VA"],
    enrollment: "full-time",
    other: ["Essay on leadership experience"]
  }
};

async function getCriteria(url, pageText) {
  if (CONFIG.USE_MOCK) {
    await new Promise((r) => setTimeout(r, 600)); // pretend network delay
    return MOCK_RESPONSE;
  }

  const res = await fetch(CONFIG.API_URL, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      url: url,
      page_text: pageText.slice(0, CONFIG.MAX_PAGE_CHARS)
    })
  });

  if (!res.ok) {
    throw new Error("The eligibility service returned an error (" + res.status + ").");
  }
  return res.json();
}
