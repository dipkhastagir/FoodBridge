async function loadAvailableFood() {
  const search = document.getElementById("searchInput").value.trim();
  const type = document.getElementById("typeFilter").value;
  const area = document.getElementById("areaFilter").value;

  const params = new URLSearchParams();
  if (search) params.append("search", search);
  if (type) params.append("type", type);
  if (area) params.append("area", area);

  const result = await apiRequest("/api/foods?" + params.toString());
  if (!result.ok) {
    showMessage("message", result.message, "error");
    return;
  }

  const grid = document.getElementById("foodGrid");
  const emptyState = document.getElementById("emptyState");

  document.getElementById("statAvailableFood").textContent = result.foods.length;

  if (result.foods.length === 0) {
    grid.innerHTML = "";
    emptyState.classList.remove("hidden");
    return;
  }

  emptyState.classList.add("hidden");
  let cards = "";
  for (const food of result.foods) {
    cards += makeTicket(food);
  }
  grid.innerHTML = cards;
}

function makeTicket(food) {
  let notes = "";
  if (food.notes) {
    notes = '<div class="ticket-notes">' + escapeHtml(food.notes) + "</div>";
  }

  let leftText = "servings";
  if (food.remaining < food.quantity) {
    leftText = "of " + food.quantity + " left";
  }

  return (
    '<article class="ticket food-card" id="food-card-' + food.id + '">' +
      '<div class="ticket-top">' +
        '<div class="ticket-head">' +
          '<span class="ticket-emoji">' + foodEmoji(food.foodType) + "</span>" +
          '<span class="type-pill food-type">' + escapeHtml(food.foodType) + "</span>" +
        "</div>" +
        '<h3 class="food-title">' + escapeHtml(food.title) + "</h3>" +
        (food.nearYou ? '<span class="near-badge">Near you</span>' : "") +
        '<div class="ticket-info food-area">📍 <strong>' + escapeHtml(food.area) + "</strong>, " + escapeHtml(food.location) +
          " " + mapsLink(food.area, food.location) + "</div>" +
        '<div class="ticket-info">🏪 ' + escapeHtml(food.donorName) + ", " + escapeHtml(food.donorPhone) + "</div>" +
        notes +
      "</div>" +
      '<div class="ticket-bottom">' +
        '<div class="ticket-line">' +
          '<div class="qty"><span id="remaining-' + food.id + '">' + food.remaining + "</span> <small>" + leftText + "</small></div>" +
          '<div class="time-left">' + timeLeft(food.expiresAt) + "</div>" +
        "</div>" +
        '<form class="claim-form" onsubmit="claimFood(event, ' + food.id + ')">' +
          '<input type="number" class="form-control claim-qty" id="claim-qty-' + food.id + '" ' +
            'min="1" max="' + food.remaining + '" placeholder="Qty" aria-label="Servings to claim" required>' +
          '<button type="submit" class="btn btn-primary btn-sm" id="claim-' + food.id + '">Claim</button>' +
        "</form>" +
      "</div>" +
    "</article>"
  );
}

async function loadMyClaims() {
  const result = await apiRequest("/api/collector/claims");
  if (!result.ok) {
    showMessage("message", result.message, "error");
    return;
  }

  const claims = result.claims;
  const waiting = claims.filter((c) => c.status === "claimed").length;
  const collectedServings = claims.filter((c) => c.status === "collected").reduce((s, c) => s + c.quantity, 0);
  document.getElementById("statMyClaims").textContent = waiting;
  document.getElementById("statCollected").textContent = collectedServings;

  const tableBody = document.getElementById("claimsTableBody");

  if (claims.length === 0) {
    tableBody.innerHTML = '<tr class="empty-row"><td colspan="6">You have not claimed any food yet.</td></tr>';
    return;
  }

  let rows = "";
  for (const claim of claims) {
    let statusPill = "";
    let action = "";

    if (claim.status === "claimed") {
      statusPill = '<span class="status status-claimed">Waiting for donor</span>';
      action = '<button class="btn btn-danger btn-sm" id="release-' + claim.id + '" onclick="releaseClaim(' + claim.id + ')">Release food</button>';
    } else {
      statusPill = '<span class="status status-collected">Confirmed by donor</span>';
      action = '<span class="locked" id="locked-' + claim.id + '">🔒 Locked</span>';
    }

    rows +=
      '<tr id="claim-row-' + claim.id + '">' +
        '<td><div class="food-name">' + foodEmoji(claim.foodType) + " " + escapeHtml(claim.title) + "</div>" +
          '<div class="small">Claimed ' + timeAgo(claim.claimedAt) + "</div></td>" +
        '<td class="claim-qty-cell">' + claim.quantity + "</td>" +
        "<td>" + escapeHtml(claim.donorName) + '<div class="small">' + escapeHtml(claim.donorPhone) + "</div></td>" +
        "<td><strong>" + escapeHtml(claim.area) + "</strong>" + '<div class="small">' + escapeHtml(claim.location) + "</div>" +
          mapsLink(claim.area, claim.location) + "</td>" +
        "<td>" + statusPill + "</td>" +
        "<td>" + action + "</td>" +
      "</tr>";
  }
  tableBody.innerHTML = rows;
}

async function claimFood(event, foodId) {
  event.preventDefault();
  clearMessage("message");

  const quantity = Number(document.getElementById("claim-qty-" + foodId).value);
  const result = await apiRequest("/api/foods/" + foodId + "/claim", "POST", { quantity: quantity });

  await loadAvailableFood();
  await loadMyClaims();
  showMessage("message", result.message, result.ok ? "success" : "error");
}

async function releaseClaim(claimId) {
  const sure = confirm("Release this food? Only do this if you have NOT picked it up. The servings go back to the donor's post for other collectors.");
  if (!sure) return;

  clearMessage("message");
  const result = await apiRequest("/api/collector/claims/" + claimId + "/release", "PUT");
  await loadAvailableFood();
  await loadMyClaims();
  showMessage("message", result.message, result.ok ? "success" : "error");
}

document.getElementById("searchBtn").addEventListener("click", loadAvailableFood);

document.getElementById("clearSearchBtn").addEventListener("click", function () {
  document.getElementById("searchInput").value = "";
  document.getElementById("typeFilter").value = "";
  document.getElementById("areaFilter").value = "";
  loadAvailableFood();
});

document.getElementById("searchInput").addEventListener("keydown", function (event) {
  if (event.key === "Enter") loadAvailableFood();
});

async function startPage() {
  const user = await protectPage("collector");
  if (!user) return;
  document.getElementById("welcomeTitle").textContent = "Welcome, " + user.name;
  document.getElementById("myAreaLine").innerHTML =
    "📍 You are in <strong>" + escapeHtml(user.area) + "</strong>. Food marked <em>Near you</em> is in your area.";
  setupLogout();
  setupRoleSwitch(user);
  await fillAreaSelect("areaFilter", "All areas");
  await loadAvailableFood();
  await loadMyClaims();
}

startPage();
