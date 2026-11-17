async function apiRequest(url, method = "GET", data = null) {
  const options = {
    method: method,
    headers: { "Content-Type": "application/json" }
  };
  if (data) {
    options.body = JSON.stringify(data);
  }

  try {
    const response = await fetch(url, options);
    const result = await response.json();
    result.ok = response.ok;
    return result;
  } catch (error) {
    return { ok: false, message: "Cannot connect to the server. Is it running (npm start)?" };
  }
}

function showMessage(elementId, text, type) {
  const box = document.getElementById(elementId);
  box.textContent = text;
  box.className = "msg " + type;
}

function clearMessage(elementId) {
  const box = document.getElementById(elementId);
  box.textContent = "";
  box.className = "msg";
}

function escapeHtml(text) {
  const div = document.createElement("div");
  div.textContent = text == null ? "" : String(text);
  return div.innerHTML;
}

function timeLeft(expiresAt) {
  const ms = new Date(expiresAt).getTime() - Date.now();
  if (ms <= 0) return "Expired";
  const totalMinutes = Math.floor(ms / 60000);
  const hours = Math.floor(totalMinutes / 60);
  const minutes = totalMinutes % 60;
  return hours + "h " + minutes + "m left";
}

function timeAgo(dateText) {
  if (!dateText) return "";
  const minutes = Math.floor((Date.now() - new Date(dateText).getTime()) / 60000);
  if (minutes < 1) return "just now";
  if (minutes < 60) return minutes + " min ago";
  const hours = Math.floor(minutes / 60);
  if (hours < 24) return hours + "h ago";
  return Math.floor(hours / 24) + "d ago";
}

function foodEmoji(foodType) {
  const emojis = {
    "Cooked Meal": "🍛",
    "Bakery": "🍞",
    "Fruits & Vegetables": "🍎",
    "Dry Food": "🌾",
    "Drinks & Dairy": "🥛"
  };
  return emojis[foodType] || "🍱";
}

async function fillAreaSelect(selectId, firstText, selectedArea) {
  const select = document.getElementById(selectId);
  const result = await apiRequest("/api/areas");
  if (!result.ok) return;

  let options = '<option value="">' + firstText + "</option>";
  for (const area of result.areas) {
    options += '<option value="' + escapeHtml(area) + '">' + escapeHtml(area) + "</option>";
  }
  select.innerHTML = options;
  if (selectedArea) select.value = selectedArea;
}

function mapsLink(area, address) {
  const place = area === "Outside Dhaka" ? address + ", Bangladesh" : address + ", " + area + ", Dhaka";
  const url = "https://www.google.com/maps/search/?api=1&query=" + encodeURIComponent(place);
  return '<a class="map-link" href="' + url + '" target="_blank" rel="noopener">Open in Maps</a>';
}

function dashboardFor(role) {
  if (role === "admin") return "admin-dashboard.html";
  return role === "donor" ? "donor-dashboard.html" : "collector-dashboard.html";
}

async function protectPage(requiredRole) {
  const result = await apiRequest("/api/me");

  if (!result.ok) {
    window.location.href = "login.html";
    return null;
  }

  const user = result.user;
  if (requiredRole && user.role !== requiredRole) {
    window.location.href = dashboardFor(user.role);
    return null;
  }

  const nameBox = document.getElementById("navUserName");
  const roleBox = document.getElementById("navUserRole");
  if (nameBox) nameBox.textContent = user.name;
  if (roleBox) roleBox.textContent = user.role.charAt(0).toUpperCase() + user.role.slice(1);

  document.body.classList.remove("hidden");
  return user;
}

function setupRoleSwitch(user) {
  const button = document.getElementById("switchRoleBtn");
  if (!button) return;

  const otherRole = user.role === "donor" ? "Collector" : "Donor";
  button.textContent = "Switch to " + otherRole;

  button.addEventListener("click", async function () {
    let question = "Switch to " + otherRole + "?\n\n";
    if (user.role === "donor") {
      question += "You will be able to claim food from other donors. Your food posts stay saved and come back when you switch to Donor again.";
    } else {
      question += "You will be able to post food you can't use. Your claims stay saved and come back when you switch to Collector again.";
    }
    if (!confirm(question)) return;

    const result = await apiRequest("/api/switch-role", "PUT");
    if (result.ok) {
      window.location.href = dashboardFor(result.user.role);
    } else {
      showMessage("message", result.message, "error");
    }
  });
}

function setupLogout() {
  const button = document.getElementById("logoutBtn");
  if (!button) return;
  button.addEventListener("click", async function () {
    await apiRequest("/api/logout", "POST");
    window.location.href = "login.html";
  });
}

document.querySelectorAll('input[type="tel"]').forEach(function (box) {
  box.addEventListener("input", function () {
    box.value = box.value.replace(/\D/g, "").slice(0, 11);
  });
});
