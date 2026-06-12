const API_BASE = "http://127.0.0.1:8000";

const navToggle = document.querySelector(".nav-toggle");
const navLinks = document.querySelector("[data-nav-links]");

let samplePayloads = new Map();
let selectedPayload = null;

if (navToggle && navLinks) {
  navToggle.addEventListener("click", () => {
    const isOpen = navLinks.classList.toggle("open");
    navToggle.setAttribute("aria-expanded", String(isOpen));
  });

  navLinks.querySelectorAll("a").forEach((link) => {
    link.addEventListener("click", () => {
      navLinks.classList.remove("open");
      navToggle.setAttribute("aria-expanded", "false");
    });
  });
}

document.addEventListener("DOMContentLoaded", () => {
  const datasetSelect = document.querySelector("[data-dataset-select]");
  if (!datasetSelect) {
    return;
  }

  initialiseDashboard(datasetSelect);
});

async function initialiseDashboard(datasetSelect) {
  await checkHealth({ retries: 6, delayMs: 1000 });
  await loadSamples(datasetSelect);

  document.querySelector("[data-run-allocation]")?.addEventListener("click", runAllocation);
  document.querySelector("[data-run-comparison]")?.addEventListener("click", runFairnessComparison);
  datasetSelect.addEventListener("change", () => {
    selectedPayload = samplePayloads.get(datasetSelect.value) || null;
    updateScenarioStats(selectedPayload);
  });
}

async function checkHealth({ retries = 1, delayMs = 0 } = {}) {
  for (let attempt = 1; attempt <= retries; attempt += 1) {
    try {
      const health = await requestJson("/health");
      setText("[data-api-status]", health.status === "ok" ? "Connected" : "Offline");
      return true;
    } catch (error) {
      if (attempt < retries) {
        setText("[data-api-status]", "Connecting");
        showMessage(`Waiting for API startup... attempt ${attempt + 1}/${retries}`, "info");
        await sleep(delayMs);
        continue;
      }

      setText("[data-api-status]", "Offline");
      showMessage("API Offline. Start the backend with: uvicorn api.main:app --reload", "error");
      return false;
    }
  }
}

async function loadSamples(datasetSelect) {
  try {
    const response = await requestJson("/samples");
    const samples = Array.isArray(response.samples) ? response.samples : [];

    if (!samples.length) {
      datasetSelect.innerHTML = '<option value="">No datasets available</option>';
      showMessage("No sample datasets were returned by the API.", "error");
      return;
    }

    samplePayloads = new Map(samples.map((sample) => [sample.id, sample.payload]));
    datasetSelect.innerHTML = samples
      .map((sample) => `<option value="${escapeHtml(sample.id)}">${escapeHtml(sample.id)}</option>`)
      .join("");

    selectedPayload = samplePayloads.get(datasetSelect.value) || null;
    updateScenarioStats(selectedPayload);
    showMessage("API Connected. Select a dataset and run allocation.", "success");
  } catch (error) {
    datasetSelect.innerHTML = '<option value="">API unavailable</option>';
    showMessage(error.message || "Unable to load datasets from the API.", "error");
  }
}

async function runAllocation() {
  if (!selectedPayload) {
    showMessage("No dataset selected. Load samples from the API first.", "error");
    return;
  }

  try {
    showMessage("Running allocation with the FairMatch backend...", "info");
    const result = await postJson("/allocate", selectedPayload);
    renderAllocationResult(result);
    showMessage("Allocation completed with real backend data.", "success");
  } catch (error) {
    showMessage(error.message || "Allocation failed.", "error");
  }
}

async function runFairnessComparison() {
  if (!selectedPayload) {
    showMessage("No dataset selected. Load samples from the API first.", "error");
    return;
  }

  try {
    showMessage("Running counterfactual fairness comparison...", "info");
    const result = await postJson("/compare-fairness?fairness_weight=3", selectedPayload);
    renderComparisonResult(result);
    showMessage("Fairness comparison completed with real backend data.", "success");
  } catch (error) {
    showMessage(error.message || "Fairness comparison failed.", "error");
  }
}

async function requestJson(path) {
  const response = await fetch(`${API_BASE}${path}`);
  return parseResponse(response);
}

async function postJson(path, payload) {
  const response = await fetch(`${API_BASE}${path}`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  });
  return parseResponse(response);
}

async function parseResponse(response) {
  let data;
  try {
    data = await response.json();
  } catch (error) {
    throw new Error("Invalid API response.");
  }

  if (!response.ok) {
    throw new Error(data.detail || "API request failed.");
  }

  return data;
}

function renderAllocationResult(result) {
  if (!result || !Array.isArray(result.assignments)) {
    throw new Error("Invalid allocation response.");
  }

  setText("[data-data-source-label]", "Live backend data");
  setText("[data-overview-status]", result.status);
  setText("[data-overview-total]", result.total_satisfaction);
  setText("[data-overview-gap]", result.fairness_gap);
  setText("[data-overview-gini]", formatDecimal(result.gini_coefficient, 3));
  setText("[data-summary-status]", result.status === "OPTIMAL" ? "Completed" : result.status);
  setText("[data-summary-assigned]", result.assignments.length);
  setText("[data-summary-projects]", selectedPayload?.items?.length ?? "N/A");
  setText("[data-summary-result]", "Fairness-Aware");

  setText("[data-metric-total]", result.total_satisfaction);
  setText("[data-metric-average]", formatDecimal(result.average_satisfaction, 2));
  setText("[data-metric-gap]", result.fairness_gap);
  setText("[data-metric-max-min]", result.max_min_value);
  setText("[data-metric-gini]", formatDecimal(result.gini_coefficient, 3));
  setText("[data-metric-workload]", result.workload_gap);

  renderAllocationRows(result.assignments);
  renderExplanation(result.assignments[0]);
}

function renderAllocationRows(assignments) {
  const container = document.querySelector("[data-allocation-rows]");
  if (!container) {
    return;
  }

  container.innerHTML = assignments
    .map((assignment) => {
      const rank = assignment.preference_rank ?? "Unranked";
      const skillText = assignment.skill_match ? "Matched" : "Not matched";
      const skillClass = assignment.skill_match ? "positive-text" : "";
      return `
        <div class="product-table-row" role="row">
          <span>${escapeHtml(assignment.person_name)}</span>
          <span>${escapeHtml(assignment.item_name)}</span>
          <span>${escapeHtml(String(rank))}</span>
          <span>${escapeHtml(String(assignment.satisfaction))}</span>
          <span class="${skillClass}">${skillText}</span>
          <span>${assignment.explanation ? "Explained" : "Pending"}</span>
        </div>
      `;
    })
    .join("");
}

function renderExplanation(assignment) {
  if (!assignment || !assignment.explanation) {
    return;
  }

  const explanation = assignment.explanation;
  setText("[data-explanation-person]", assignment.person_name);
  setText("[data-explanation-project]", assignment.item_name);

  const notes = [
    explanation.summary,
    explanation.first_choice_note,
    explanation.capacity_note,
    explanation.skill_note,
    explanation.supervisor_note,
    explanation.fairness_note,
    explanation.workload_note,
  ].filter(Boolean);

  const list = document.querySelector("[data-explanation-list]");
  if (list) {
    list.innerHTML = notes.map((note) => `<li>${escapeHtml(note)}</li>`).join("");
  }
}

function renderComparisonResult(result) {
  if (!result || !result.counterfactual_comparison) {
    throw new Error("Invalid comparison response.");
  }

  const comparison = result.counterfactual_comparison;
  setText("[data-baseline-total]", comparison.baseline_total_satisfaction);
  setText("[data-baseline-gap]", comparison.baseline_fairness_gap);
  setText("[data-baseline-gini]", formatDecimal(comparison.baseline_gini_coefficient, 3));
  setText("[data-fairness-total]", comparison.fairness_total_satisfaction);
  setText("[data-fairness-gap]", comparison.fairness_fairness_gap);
  setText("[data-fairness-gini]", formatDecimal(comparison.fairness_gini_coefficient, 3));

  const changedAssignments = comparison.changed_assignments || {};
  const changedSatisfaction = comparison.changed_satisfaction || {};
  const changedCount = Object.keys(changedAssignments).length;
  setText("[data-changed-count]", changedCount);
  setText(
    "[data-comparison-note]",
    result.warning ||
      "Real backend comparison loaded. Changed assignments and satisfaction changes are listed below."
  );

  const changes = [
    ...Object.entries(changedAssignments).map(([personId, items]) => {
      const [before, after] = items;
      return `${personId}: assignment ${before} -> ${after}`;
    }),
    ...Object.entries(changedSatisfaction).map(([personId, scores]) => {
      const [before, after] = scores;
      return `${personId}: satisfaction ${before} -> ${after}`;
    }),
  ];

  const list = document.querySelector("[data-change-list]");
  if (list) {
    list.innerHTML = changes.length
      ? changes.map((change) => `<li>${escapeHtml(change)}</li>`).join("")
      : "<li>No assignment or satisfaction changes detected.</li>";
  }
}

function updateScenarioStats(payload) {
  if (!payload) {
    return;
  }

  const supervisors = new Set(
    (payload.items || [])
      .map((item) => item.supervisor_id)
      .filter((supervisorId) => supervisorId !== undefined && supervisorId !== null)
  );

  setText("[data-scenario-students]", (payload.people || []).length);
  setText("[data-scenario-projects]", (payload.items || []).length);
  setText("[data-scenario-supervisors]", supervisors.size || "N/A");
}

function showMessage(message, type = "info") {
  const panel = document.querySelector("[data-message-panel]");
  if (!panel) {
    return;
  }

  panel.textContent = message;
  panel.className = `message-panel visible ${type}`;
}

function setText(selector, value) {
  const element = document.querySelector(selector);
  if (element) {
    element.textContent = value;
  }
}

function formatDecimal(value, digits) {
  const number = Number(value);
  return Number.isFinite(number) ? number.toFixed(digits) : "N/A";
}

function escapeHtml(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

function sleep(ms) {
  return new Promise((resolve) => {
    window.setTimeout(resolve, ms);
  });
}
