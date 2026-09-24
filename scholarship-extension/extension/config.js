// Flip USE_MOCK to false once the Python backend is running.
const CONFIG = {
  USE_MOCK: true,
  API_URL: "http://localhost:8000/api/extract",
  MAX_PAGE_CHARS: 20000 // keep requests small; long pages get trimmed
};
