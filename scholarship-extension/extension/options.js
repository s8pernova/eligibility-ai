const fields = ["gpa", "major", "state", "enrollment"];

async function load() {
  const { profile } = await chrome.storage.local.get("profile");
  if (!profile) return;
  fields.forEach((f) => {
    if (profile[f] != null) document.getElementById(f).value = profile[f];
  });
}

document.getElementById("save").addEventListener("click", async () => {
  const profile = {};
  fields.forEach((f) => (profile[f] = document.getElementById(f).value.trim()));
  profile.state = profile.state.toUpperCase();
  profile.gpa = profile.gpa === "" ? null : Number(profile.gpa);

  await chrome.storage.local.set({ profile });
  const saved = document.getElementById("saved");
  saved.textContent = "Profile saved";
  setTimeout(() => (saved.textContent = ""), 2000);
});

load();
