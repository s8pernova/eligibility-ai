// Compares the student's profile against extracted criteria.
// Plain code, not AI, so results are consistent and explainable.
// Each result: { label, status: "met" | "not_met" | "check", detail }

function norm(s) {
  return String(s || "").trim().toLowerCase();
}

function compareEligibility(profile, data) {
  const c = data.criteria || {};
  const results = [];

  // GPA
  if (c.min_gpa != null) {
    if (profile.gpa == null || profile.gpa === "") {
      results.push({ label: "GPA", status: "check",
        detail: "Requires " + c.min_gpa + ". Add your GPA in settings." });
    } else if (Number(profile.gpa) >= Number(c.min_gpa)) {
      results.push({ label: "GPA", status: "met",
        detail: "Your " + profile.gpa + " meets the " + c.min_gpa + " minimum." });
    } else {
      results.push({ label: "GPA", status: "not_met",
        detail: "Requires " + c.min_gpa + "; yours is " + profile.gpa + "." });
    }
  }

  // Major (fuzzy on purpose: "STEM" vs "Computer Science" needs a human)
  if (Array.isArray(c.majors) && c.majors.length) {
    const mine = norm(profile.major);
    const match = c.majors.some((m) => norm(m) === mine);
    results.push({
      label: "Major",
      status: match ? "met" : "check",
      detail: match
        ? "Your major is on the list."
        : "Accepts " + c.majors.join(", ") + ". Check whether " + (profile.major || "your major") + " counts."
    });
  }

  // State of residence
  if (Array.isArray(c.states) && c.states.length) {
    const ok = c.states.some((s) => norm(s) === norm(profile.state));
    results.push({
      label: "State",
      status: ok ? "met" : "not_met",
      detail: ok ? "You live in an eligible state." : "Open to " + c.states.join(", ") + " residents."
    });
  }

  // Enrollment status
  if (c.enrollment) {
    const ok = norm(c.enrollment) === norm(profile.enrollment);
    results.push({
      label: "Enrollment",
      status: ok ? "met" : "not_met",
      detail: ok ? "You're " + profile.enrollment + "." : "Requires " + c.enrollment + " enrollment."
    });
  }

  // Deadline
  if (data.deadline) {
    const today = new Date().toISOString().slice(0, 10);
    const open = data.deadline >= today;
    results.push({
      label: "Deadline",
      status: open ? "met" : "not_met",
      detail: open ? "Apply by " + data.deadline + "." : "Closed on " + data.deadline + "."
    });
  }

  // Anything the AI couldn't turn into a rule
  (c.other || []).forEach((item) => {
    results.push({ label: "Also required", status: "check", detail: item });
  });

  return results;
}

function overallVerdict(results) {
  if (results.some((r) => r.status === "not_met")) {
    return { status: "not_met", text: "Likely not eligible" };
  }
  if (results.some((r) => r.status === "check")) {
    return { status: "check", text: "Possibly eligible" };
  }
  return { status: "met", text: "Likely eligible" };
}
