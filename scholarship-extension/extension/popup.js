const checkBtn = document.getElementById("check");
const messageEl = document.getElementById("message");
const outputEl = document.getElementById("output");

document.getElementById("edit-profile").addEventListener("click", (e) => {
  e.preventDefault();
  chrome.runtime.openOptionsPage();
});

function showMessage(text, isError) {
  messageEl.textContent = text;
  messageEl.className = "message" + (isError ? " error" : "");
}

const ICONS = { met: "✓", not_met: "✕", check: "?" };

// Uses textContent everywhere (never innerHTML) because the data
// originally comes from arbitrary web pages.
function render(data, results) {
  outputEl.replaceChildren();

  const verdict = overallVerdict(results);
  const box = document.createElement("div");
  box.className = "verdict " + verdict.status;
  box.textContent = verdict.text;
  const name = document.createElement("small");
  name.textContent = data.scholarship_name || "Unnamed scholarship";
  box.appendChild(name);
  outputEl.appendChild(box);

  if (!results.length) {
    showMessage("No specific requirements were found on this page. Read it directly to confirm.");
    return;
  }

  const list = document.createElement("ul");
  list.className = "results";
  results.forEach((r) => {
    const li = document.createElement("li");
    const icon = document.createElement("span");
    icon.className = "icon " + r.status;
    icon.textContent = ICONS[r.status];
    const body = document.createElement("div");
    const label = document.createElement("strong");
    label.textContent = r.label;
    body.appendChild(label);
    body.appendChild(document.createTextNode(r.detail));
    li.append(icon, body);
    list.appendChild(li);
  });
  outputEl.appendChild(list);
}

async function getPageText(tab) {
  const [{ result }] = await chrome.scripting.executeScript({
    target: { tabId: tab.id },
    func: () => document.body.innerText
  });
  return result || "";
}

checkBtn.addEventListener("click", async () => {
  outputEl.replaceChildren();
  checkBtn.disabled = true;
  showMessage("Reading the page…");

  try {
    const { profile } = await chrome.storage.local.get("profile");
    if (!profile) {
      showMessage("Set up your profile first, then check again.", true);
      chrome.runtime.openOptionsPage();
      return;
    }

    const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
    let pageText;
    try {
      pageText = await getPageText(tab);
    } catch {
      showMessage("This page can't be read. Open a scholarship website and try again.", true);
      return;
    }

    showMessage("Finding the requirements…");
    const data = await getCriteria(tab.url, pageText);
    const results = compareEligibility(profile, data);
    showMessage("");
    render(data, results);
  } catch (err) {
    showMessage(err.message || "Something went wrong. Try again.", true);
  } finally {
    checkBtn.disabled = false;
  }
});
