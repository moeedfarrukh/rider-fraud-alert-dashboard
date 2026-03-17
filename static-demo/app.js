const defaultAlerts = [
  { alert_id: 101, rider_id: 12, city: "Karachi", fraud_type: "promo_abuse", risk_score: 91, estimated_loss: 12800, priority_score: 11648, status: "open", created_ts: "2026-03-17T10:00:00Z" },
  { alert_id: 102, rider_id: 33, city: "Lahore", fraud_type: "payment_fraud", risk_score: 87, estimated_loss: 14400, priority_score: 12528, status: "open", created_ts: "2026-03-17T10:10:00Z" },
  { alert_id: 103, rider_id: 47, city: "Islamabad", fraud_type: "refund_abuse", risk_score: 74, estimated_loss: 8600, priority_score: 6364, status: "monitor", created_ts: "2026-03-17T10:20:00Z" },
  { alert_id: 104, rider_id: 58, city: "Rawalpindi", fraud_type: "account_takeover", risk_score: 82, estimated_loss: 9900, priority_score: 8118, status: "open", created_ts: "2026-03-17T10:40:00Z" },
  { alert_id: 105, rider_id: 71, city: "Karachi", fraud_type: "location_spoofing", risk_score: 63, estimated_loss: 5200, priority_score: 3276, status: "monitor", created_ts: "2026-03-17T11:05:00Z" },
  { alert_id: 106, rider_id: 85, city: "Lahore", fraud_type: "payment_fraud", risk_score: 95, estimated_loss: 17000, priority_score: 16150, status: "open", created_ts: "2026-03-17T11:20:00Z" }
];

const riderProfiles = {
  12: {
    created_at: "2025-12-01",
    city: "Karachi",
    signup_channel: "referral",
    status: "active",
    devices: [{ id: "D-992", rooted: 1, first_seen: "2025-12-01", last_seen: "2026-03-17" }, { id: "D-314", rooted: 0, first_seen: "2026-01-21", last_seen: "2026-03-16" }],
    trips: [{ id: 88911, fare: 620, promo: 410, distance: 9.2, status: "completed" }, { id: 88701, fare: 500, promo: 280, distance: 7.1, status: "completed" }],
    payments: [{ id: 78121, amount: 210, method: "card", success: 0, chargeback: 1 }, { id: 78021, amount: 220, method: "card", success: 1, chargeback: 0 }],
    refunds: [{ id: 4112, amount: 380, reason: "trip_not_taken", ts: "2026-03-16T07:20:00Z" }],
  },
  33: {
    created_at: "2025-11-19",
    city: "Lahore",
    signup_channel: "paid_social",
    status: "active",
    devices: [{ id: "D-771", rooted: 1, first_seen: "2025-11-19", last_seen: "2026-03-17" }],
    trips: [{ id: 77891, fare: 720, promo: 150, distance: 12.7, status: "completed" }],
    payments: [{ id: 66191, amount: 570, method: "card", success: 0, chargeback: 1 }],
    refunds: [],
  },
  47: {
    created_at: "2025-10-03",
    city: "Islamabad",
    signup_channel: "organic",
    status: "active",
    devices: [{ id: "D-188", rooted: 0, first_seen: "2025-10-03", last_seen: "2026-03-16" }],
    trips: [{ id: 66444, fare: 410, promo: 90, distance: 6.1, status: "completed" }],
    payments: [{ id: 55431, amount: 320, method: "wallet", success: 1, chargeback: 0 }],
    refunds: [{ id: 3001, amount: 310, reason: "service_issue", ts: "2026-03-15T10:00:00Z" }],
  },
  58: {
    created_at: "2026-01-14",
    city: "Rawalpindi",
    signup_channel: "seo",
    status: "active",
    devices: [{ id: "D-450", rooted: 0, first_seen: "2026-01-14", last_seen: "2026-03-17" }, { id: "D-451", rooted: 0, first_seen: "2026-03-01", last_seen: "2026-03-17" }],
    trips: [{ id: 45512, fare: 540, promo: 0, distance: 10.5, status: "completed" }],
    payments: [{ id: 40012, amount: 540, method: "wallet", success: 1, chargeback: 0 }],
    refunds: [],
  },
  71: {
    created_at: "2025-09-08",
    city: "Karachi",
    signup_channel: "referral",
    status: "active",
    devices: [{ id: "D-650", rooted: 0, first_seen: "2025-09-08", last_seen: "2026-03-15" }],
    trips: [{ id: 33290, fare: 350, promo: 50, distance: 4.4, status: "completed" }],
    payments: [{ id: 30111, amount: 300, method: "cash", success: 1, chargeback: 0 }],
    refunds: [],
  },
  85: {
    created_at: "2025-12-22",
    city: "Lahore",
    signup_channel: "referral",
    status: "active",
    devices: [{ id: "D-777", rooted: 1, first_seen: "2025-12-22", last_seen: "2026-03-17" }, { id: "D-778", rooted: 1, first_seen: "2026-02-10", last_seen: "2026-03-17" }],
    trips: [{ id: 99210, fare: 810, promo: 420, distance: 14.1, status: "completed" }, { id: 99211, fare: 760, promo: 320, distance: 13.4, status: "completed" }],
    payments: [{ id: 88111, amount: 390, method: "card", success: 0, chargeback: 1 }, { id: 88112, amount: 440, method: "card", success: 0, chargeback: 1 }],
    refunds: [{ id: 5002, amount: 390, reason: "duplicate_charge", ts: "2026-03-17T06:10:00Z" }],
  },
};

function getAlerts() {
  const saved = localStorage.getItem("rfad_alerts");
  if (!saved) {
    localStorage.setItem("rfad_alerts", JSON.stringify(defaultAlerts));
    return [...defaultAlerts];
  }
  return JSON.parse(saved);
}

function saveAlerts(alerts) {
  localStorage.setItem("rfad_alerts", JSON.stringify(alerts));
}

function getActions() {
  return JSON.parse(localStorage.getItem("rfad_actions") || "[]");
}

function saveAction(action) {
  const actions = getActions();
  actions.unshift(action);
  localStorage.setItem("rfad_actions", JSON.stringify(actions));
}

function renderQueuePage() {
  const tbody = document.getElementById("alerts-tbody");
  if (!tbody) return;

  let alerts = getAlerts().sort((a, b) => b.priority_score - a.priority_score);
  const minRisk = Number(document.getElementById("minRisk").value || 0);
  const fraudType = document.getElementById("fraudType").value;
  const city = document.getElementById("city").value;
  const status = document.getElementById("status").value;

  alerts = alerts.filter((a) => a.risk_score >= minRisk);
  if (fraudType) alerts = alerts.filter((a) => a.fraud_type === fraudType);
  if (city) alerts = alerts.filter((a) => a.city === city);
  if (status) alerts = alerts.filter((a) => a.status === status);

  // KPI metrics
  const totalAlerts = alerts.length;
  const estLoss = alerts.reduce((sum, a) => sum + a.estimated_loss, 0);
  const highRiskCount = alerts.filter((a) => a.risk_score >= 80).length;
  const blockedCount = alerts.filter((a) => a.status === "blocked").length;

  document.getElementById("totalAlerts").textContent = totalAlerts.toLocaleString("en-US");
  document.getElementById("highRiskCount").textContent = highRiskCount.toLocaleString("en-US");
  document.getElementById("estLoss").textContent = estLoss.toLocaleString("en-US", {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  });
  document.getElementById("blockedCount").textContent = blockedCount.toLocaleString("en-US");

  // Severity distribution
  const high = alerts.filter((a) => a.risk_score >= 80).length;
  const med = alerts.filter((a) => a.risk_score >= 60 && a.risk_score < 80).length;
  const low = alerts.filter((a) => a.risk_score < 60).length;
  const totalSev = high + med + low || 1;

  const sevHighPct = (high * 100) / totalSev;
  const sevMedPct = (med * 100) / totalSev;
  const sevLowPct = (low * 100) / totalSev;

  const sevHigh = document.getElementById("sevHigh");
  const sevMed = document.getElementById("sevMed");
  const sevLow = document.getElementById("sevLow");
  const sevLegend = document.getElementById("sevLegend");
  if (sevHigh && sevMed && sevLow && sevLegend) {
    sevHigh.style.width = `${sevHighPct}%`;
    sevMed.style.width = `${sevMedPct}%`;
    sevLow.style.width = `${sevLowPct}%`;
    sevLegend.innerHTML = `
      <span class="pill pill-high">High · ${high}</span>
      <span class="pill pill-medium">Medium · ${med}</span>
      <span class="pill pill-low">Low · ${low}</span>
    `;
  }

  // Fraud type distribution
  const fraudCounts = {};
  alerts.forEach((a) => {
    fraudCounts[a.fraud_type] = (fraudCounts[a.fraud_type] || 0) + 1;
  });
  const fraudEntries = Object.entries(fraudCounts).sort((a, b) => b[1] - a[1]).slice(0, 5);
  const totalFraud = fraudEntries.reduce((sum, [, cnt]) => sum + cnt, 0) || 1;
  const fraudTypeList = document.getElementById("fraudTypeList");
  if (fraudTypeList) {
    fraudTypeList.innerHTML = "";
    fraudEntries.forEach(([type, cnt]) => {
      const pct = (cnt * 100) / totalFraud;
      const li = document.createElement("li");
      li.innerHTML = `
        <span class="fraud-label">${type}</span>
        <div class="fraud-bar-wrap">
          <div class="fraud-bar" style="width:${pct}%"></div>
        </div>
        <span class="fraud-count">${cnt}</span>
      `;
      fraudTypeList.appendChild(li);
    });
  }

  tbody.innerHTML = "";
  if (!alerts.length) {
    tbody.innerHTML = '<tr><td colspan="9">No alerts match current filters.</td></tr>';
    return;
  }

  alerts.forEach((a) => {
    const tr = document.createElement("tr");
    tr.innerHTML = `
      <td>#${a.alert_id}</td>
      <td><a href="rider.html?rider_id=${a.rider_id}">R${a.rider_id}</a></td>
      <td>${a.city}</td>
      <td>${
        a.risk_score >= 80
          ? '<span class="pill pill-high">High</span>'
          : a.risk_score >= 60
          ? '<span class="pill pill-medium">Medium</span>'
          : '<span class="pill pill-low">Low</span>'
      }</td>
      <td>${a.fraud_type}</td>
      <td>${a.risk_score.toFixed(1)}%</td>
      <td>${a.estimated_loss.toLocaleString("en-US", { minimumFractionDigits: 2 })}</td>
      <td><span class="status ${a.status}">${a.status}</span></td>
      <td>
        <form class="action-form" data-alert="${a.alert_id}">
          <input name="notes" type="text" placeholder="Notes" />
          <div class="action-inline">
            <select name="action">
              <option value="monitor">monitor</option>
              <option value="temporary_block">temporary_block</option>
              <option value="escalate">escalate</option>
              <option value="allow">allow</option>
            </select>
            <select name="outcome">
              <option value="pending_review">pending_review</option>
              <option value="confirmed_fraud">confirmed_fraud</option>
              <option value="false_positive">false_positive</option>
            </select>
            <input name="analyst" type="text" placeholder="Analyst" required />
            <button type="submit">Save</button>
          </div>
        </form>
      </td>
    `;
    tbody.appendChild(tr);
  });

  document.querySelectorAll(".action-form").forEach((form) => {
    form.addEventListener("submit", (e) => {
      e.preventDefault();
      const alertId = Number(form.dataset.alert);
      const data = new FormData(form);
      const analyst = data.get("analyst");
      const action = data.get("action");
      const outcome = data.get("outcome");
      const notes = data.get("notes");

      const statusMap = { allow: "closed", monitor: "monitor", temporary_block: "blocked", escalate: "open" };
      const alertsData = getAlerts();
      const index = alertsData.findIndex((x) => x.alert_id === alertId);
      if (index !== -1) {
        alertsData[index].status = statusMap[action] || "monitor";
        saveAlerts(alertsData);
      }

      saveAction({
        action_id: Date.now(),
        alert_id: alertId,
        rider_id: alertsData[index]?.rider_id || null,
        fraud_type: alertsData[index]?.fraud_type || null,
        analyst_id: analyst,
        action,
        outcome_label: outcome,
        notes,
        action_ts: new Date().toISOString(),
      });

      renderQueuePage();
    });
  });
}

function renderRiderPage() {
  const riderName = document.getElementById("riderName");
  if (!riderName) return;

  const params = new URLSearchParams(window.location.search);
  const riderId = Number(params.get("rider_id"));
  const profile = riderProfiles[riderId];
  const alert = getAlerts().find((a) => a.rider_id === riderId);

  if (!profile) {
    riderName.textContent = `Rider R${riderId} not found`;
    return;
  }

  riderName.textContent = `Rider R${riderId}`;
  document.getElementById("riderMeta").textContent = `City: ${profile.city} | Signup: ${profile.signup_channel} | Status: ${profile.status}`;
  document.getElementById("riderCreated").textContent = `Created: ${profile.created_at}`;
  document.getElementById("riskLine").textContent = alert
    ? `Current Fraud Type: ${alert.fraud_type} | Risk: ${alert.risk_score} | Priority: ${alert.priority_score} | Est. Loss: ${alert.estimated_loss}`
    : "No current alert snapshot for this rider.";

  fillTable("devicesBody", profile.devices, (d) => `<td>${d.id}</td><td>${d.rooted}</td><td>${d.first_seen}</td><td>${d.last_seen}</td>`, 4);
  fillTable("tripsBody", profile.trips, (t) => `<td>${t.id}</td><td>${t.fare}</td><td>${t.promo}</td><td>${t.distance}</td><td>${t.status}</td>`, 5);
  fillTable("paymentsBody", profile.payments, (p) => `<td>${p.id}</td><td>${p.amount}</td><td>${p.method}</td><td>${p.success}</td><td>${p.chargeback}</td>`, 5);
  fillTable("refundsBody", profile.refunds, (r) => `<td>${r.id}</td><td>${r.amount}</td><td>${r.reason}</td><td>${r.ts}</td>`, 4);

  const riderActions = getActions().filter((a) => Number(a.rider_id) === riderId);
  fillTable(
    "actionsBody",
    riderActions,
    (a) => `<td>${a.action_id}</td><td>${a.alert_id}</td><td>${a.analyst_id}</td><td>${a.action}</td><td>${a.outcome_label}</td><td>${a.notes || ""}</td><td>${a.action_ts}</td>`,
    7
  );
}

function renderActionsPage() {
  const tbody = document.getElementById("actionsLogBody");
  if (!tbody) return;
  const actions = getActions();
  fillTable(
    "actionsLogBody",
    actions,
    (a) => `
      <td>${a.action_id}</td>
      <td>${a.alert_id}</td>
      <td>${a.rider_id ? `<a href="rider.html?rider_id=${a.rider_id}">R${a.rider_id}</a>` : "-"}</td>
      <td>${a.fraud_type || "-"}</td>
      <td>${a.analyst_id}</td>
      <td>${a.action}</td>
      <td>${a.outcome_label}</td>
      <td>${a.notes || ""}</td>
      <td>${a.action_ts}</td>
    `,
    9
  );
}

function fillTable(targetId, rows, rowHtml, colSpan) {
  const tbody = document.getElementById(targetId);
  if (!tbody) return;
  tbody.innerHTML = "";
  if (!rows.length) {
    tbody.innerHTML = `<tr><td colspan="${colSpan}">No records</td></tr>`;
    return;
  }
  rows.forEach((row) => {
    const tr = document.createElement("tr");
    tr.innerHTML = rowHtml(row);
    tbody.appendChild(tr);
  });
}

window.addEventListener("DOMContentLoaded", () => {
  if (document.getElementById("alerts-tbody")) {
    document.getElementById("applyFilters").addEventListener("click", renderQueuePage);
    document.getElementById("resetDemo").addEventListener("click", () => {
      localStorage.removeItem("rfad_alerts");
      localStorage.removeItem("rfad_actions");
      renderQueuePage();
    });
    renderQueuePage();
  }
  renderRiderPage();
  renderActionsPage();
});
