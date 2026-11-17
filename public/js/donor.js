let myFoods = [];
let currentUser = null;

const STATUS_LABELS = {
  available: "Available",
  expired: "Expired",
  claimed: "Fully claimed",
  collected: "Collected"
};

async function loadFoods() {
  const result = await apiRequest("/api/donor/foods");
  if (!result.ok) {
    showMessage("message", result.message, "error");
    return;
  }

  myFoods = result.foods;

  document.getElementById("statTotal").textContent = result.stats.total;
  document.getElementById("statAvailable").textContent = result.stats.servingsLeft;
  document.getElementById("statClaimed").textContent = result.stats.waiting;
  document.getElementById("statCollected").textContent = result.stats.servingsCollected;

  showConfirmations(result.confirmations);
  showFoodTable();
}

function showConfirmations(confirmations) {
  const panel = document.getElementById("confirmPanel");
  const list = document.getElementById("confirmList");
  document.getElementById("confirmCount").textContent = confirmations.length;

  if (confirmations.length === 0) {
    panel.classList.add("hidden");
    list.innerHTML = "";
    return;
  }

  let cards = "";
  for (const claim of confirmations) {
    cards +=
      '<div class="confirm-item" id="confirm-item-' + claim.id + '">' +
        '<div class="confirm-food">' +
          '<span class="confirm-emoji">' + foodEmoji(claim.foodType) + "</span>" +
          "<div>" +
            '<div class="food-name">' + escapeHtml(claim.title) + "</div>" +
            '<div class="small"><strong>' + claim.quantity + " servings</strong>, pickup at " + escapeHtml(claim.area) + "</div>" +
          "</div>" +
        "</div>" +
        '<div class="confirm-who">' +
          '<div class="small">Claimed ' + timeAgo(claim.claimedAt) + " by</div>" +
          '<div class="collector-name">' + escapeHtml(claim.collectorName) + "</div>" +
          '<div class="small">📞 ' + escapeHtml(claim.collectorPhone) + "</div>" +
          '<div class="small collector-location">📍 ' + escapeHtml(claim.collectorArea) + ", " +
            escapeHtml(claim.collectorAddress) + " " + mapsLink(claim.collectorArea, claim.collectorAddress) + "</div>" +
        "</div>" +
        '<button class="btn btn-primary" id="confirm-' + claim.id + '" onclick="confirmPickup(' + claim.id + ')">Confirm pickup</button>' +
      "</div>";
  }
  list.innerHTML = cards;
  panel.classList.remove("hidden");
}

function showFoodTable() {
  const tableBody = document.getElementById("foodTableBody");

  if (myFoods.length === 0) {
    tableBody.innerHTML = '<tr class="empty-row"><td colspan="6">No food posted yet. Use the form to post your first one.</td></tr>';
    return;
  }

  let rows = "";
  for (const food of myFoods) {
    rows += makeRow(food);
  }
  tableBody.innerHTML = rows;
}

function servingsBar(food) {
  const collected = food.collectedServings;
  const free = food.remaining;
  const claimed = food.quantity - free - collected;
  const pct = (n) => (n / food.quantity) * 100 + "%";

  return (
    '<div class="serv-bar" title="' + free + " free, " + claimed + " claimed, " + collected + ' collected">' +
      '<span class="seg free" style="width:' + pct(free) + '"></span>' +
      '<span class="seg claimed" style="width:' + pct(claimed) + '"></span>' +
      '<span class="seg collected" style="width:' + pct(collected) + '"></span>' +
    "</div>" +
    '<div class="small food-left">' + free + " left of " + food.quantity + "</div>"
  );
}

function makeRow(food) {
  const statusLabel = STATUS_LABELS[food.status];

  let buttons = "";
  if (food.claimCount === 0) {
    buttons += '<button class="btn btn-outline btn-sm" id="edit-' + food.id + '" onclick="startEdit(' + food.id + ')">Edit</button>';
  }
  if (food.waitingCount === 0) {
    buttons += '<button class="btn btn-danger btn-sm" id="delete-' + food.id + '" onclick="deleteFood(' + food.id + ')">Delete</button>';
  } else {
    buttons += '<span class="small">Confirm pickups above</span>';
  }

  const expires = food.status === "available" ? timeLeft(food.expiresAt) : "-";

  return (
    '<tr id="food-' + food.id + '">' +
      "<td>" +
        '<div class="food-name">' + foodEmoji(food.foodType) + " " + escapeHtml(food.title) + "</div>" +
        '<div class="small">' + escapeHtml(food.foodType) + "</div>" +
        '<div class="small">📍 ' + escapeHtml(food.area) + ", " + escapeHtml(food.location) + "</div>" +
      "</td>" +
      '<td class="food-qty">' + food.quantity + "</td>" +
      "<td>" + servingsBar(food) + "</td>" +
      '<td class="small">' + expires + "</td>" +
      '<td><span class="status status-' + food.status + '">' + statusLabel + "</span></td>" +
      '<td><div class="actions">' + buttons + "</div></td>" +
    "</tr>"
  );
}

const foodForm = document.getElementById("foodForm");

foodForm.addEventListener("submit", async function (event) {
  event.preventDefault();
  clearMessage("message");

  const foodData = {
    title: document.getElementById("foodTitle").value.trim(),
    foodType: document.getElementById("foodType").value,
    quantity: Number(document.getElementById("quantity").value),
    expiryHours: Number(document.getElementById("expiryHours").value),
    area: document.getElementById("foodArea").value,
    location: document.getElementById("location").value.trim(),
    notes: document.getElementById("notes").value.trim()
  };

  const editId = document.getElementById("editId").value;
  let result;

  if (editId) {
    result = await apiRequest("/api/donor/foods/" + editId, "PUT", foodData);
  } else {
    result = await apiRequest("/api/donor/foods", "POST", foodData);
  }

  if (result.ok) {
    resetForm();
    await loadFoods();
    showMessage("message", result.message, "success");
  } else {
    showMessage("message", result.message, "error");
  }
});

function startEdit(id) {
  const food = myFoods.find((f) => f.id === id);
  if (!food) return;

  document.getElementById("editId").value = food.id;
  document.getElementById("foodTitle").value = food.title;
  document.getElementById("foodType").value = food.foodType;
  document.getElementById("quantity").value = food.quantity;
  document.getElementById("expiryHours").value = food.expiryHours;
  document.getElementById("foodArea").value = food.area;
  document.getElementById("location").value = food.location;
  document.getElementById("notes").value = food.notes;

  document.getElementById("formTitle").textContent = "Edit food post";
  document.getElementById("formSub").textContent = "Saving restarts the freshness timer from now.";
  document.getElementById("saveFoodBtn").textContent = "Save changes";
  document.getElementById("cancelEditBtn").classList.remove("hidden");
  clearMessage("message");
  window.scrollTo({ top: 0, behavior: "smooth" });
}

function resetForm() {
  foodForm.reset();
  document.getElementById("editId").value = "";
  document.getElementById("foodArea").value = currentUser.area;
  document.getElementById("location").value = currentUser.address;
  document.getElementById("formTitle").textContent = "Post surplus food";
  document.getElementById("formSub").textContent = "Collectors will see it right away. Area and address start as your profile address.";
  document.getElementById("saveFoodBtn").textContent = "Post food";
  document.getElementById("cancelEditBtn").classList.add("hidden");
}

document.getElementById("cancelEditBtn").addEventListener("click", resetForm);

async function deleteFood(id) {
  const sure = confirm("Delete this food post? This cannot be undone.");
  if (!sure) return;

  const result = await apiRequest("/api/donor/foods/" + id, "DELETE");
  if (result.ok) {
    if (document.getElementById("editId").value === String(id)) resetForm();
    await loadFoods();
    showMessage("message", result.message, "success");
  } else {
    showMessage("message", result.message, "error");
  }
}

async function confirmPickup(claimId) {
  const result = await apiRequest("/api/donor/claims/" + claimId + "/confirm", "PUT");
  if (result.ok) {
    await loadFoods();
    showMessage("message", result.message, "success");
  } else {
    showMessage("message", result.message, "error");
  }
}

async function startPage() {
  const user = await protectPage("donor");
  if (!user) return;
  currentUser = user;
  document.getElementById("welcomeTitle").textContent = "Welcome, " + user.name;
  await fillAreaSelect("foodArea", "Select area", user.area);
  document.getElementById("location").value = user.address;
  setupLogout();
  setupRoleSwitch(user);
  await loadFoods();
}

startPage();
