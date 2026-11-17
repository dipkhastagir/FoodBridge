let allUsers = [];
let allFoods = [];

const REQUEST_STATUS = {
  pending: ["Waiting", "status-claimed"],
  code_given: ["Code given", "status-available"],
  verified: ["Code verified", "status-available"],
  done: ["Password reset", "status-collected"],
  rejected: ["Rejected", "status-expired"],
  replaced: ["Replaced", "status-collected"]
};

const FOOD_STATUS = {
  available: "Available",
  expired: "Expired",
  claimed: "Fully claimed",
  collected: "Collected"
};

function shortDate(dateText) {
  if (!dateText) return "-";
  return new Date(dateText).toLocaleString([], { day: "numeric", month: "short", hour: "2-digit", minute: "2-digit" });
}

function rolePill(role) {
  return '<span class="role-pill ' + role + '">' + escapeHtml(role) + "</span>";
}

function openTab(tabId) {
  document.querySelectorAll(".tab").forEach((tab) => tab.classList.remove("active"));
  document.querySelectorAll(".tab-section").forEach((section) => section.classList.add("hidden"));
  const tab = document.getElementById(tabId);
  tab.classList.add("active");
  document.getElementById(tab.dataset.section).classList.remove("hidden");
}

document.querySelectorAll(".tab").forEach((tab) => {
  tab.addEventListener("click", () => openTab(tab.id));
});

function openModal(id) {
  document.getElementById(id).classList.remove("hidden");
}

function closeModal(id) {
  document.getElementById(id).classList.add("hidden");
}

async function loadOverview() {
  const result = await apiRequest("/api/admin/overview");
  if (!result.ok) return;
  document.getElementById("statDonors").textContent = result.donors;
  document.getElementById("statCollectors").textContent = result.collectors;
  document.getElementById("statFoods").textContent = result.foodPosts;
  document.getElementById("statWaiting").textContent = result.pickupsWaiting;
  document.getElementById("statShared").textContent = result.servingsShared;
  document.getElementById("statRequests").textContent = result.openRequests;
  document.getElementById("requestBadge").textContent = result.openRequests;
  document.getElementById("requestBadge").classList.toggle("hidden", result.openRequests === 0);
}

async function loadRequests() {
  const result = await apiRequest("/api/admin/requests");
  const body = document.getElementById("requestsBody");
  if (!result.ok) {
    showMessage("message", result.message, "error");
    return;
  }
  if (result.requests.length === 0) {
    body.innerHTML = '<tr class="empty-row"><td colspan="6">No password reset requests yet.</td></tr>';
    return;
  }

  const typing = document.activeElement && document.activeElement.classList.contains("code-input-small");
  if (typing) return;

  let rows = "";
  for (const r of result.requests) {
    let account = '<div class="warn-text">No account uses this email</div><div class="small">' + escapeHtml(r.email) + "</div>";
    if (r.accountFound) {
      account = '<div class="food-name">' + escapeHtml(r.userName) + " " + rolePill(r.userRole) + "</div>" +
                '<div class="small">' + escapeHtml(r.email) + "</div>";
    }

    let phone = '<div><a href="tel:' + escapeHtml(r.phoneGiven) + '">' + escapeHtml(r.phoneGiven) + "</a></div>";
    if (r.accountFound) {
      phone += r.phoneMatches
        ? '<div class="match-ok">✓ Matches the account</div>'
        : '<div class="warn-text">✗ Account has ' + escapeHtml(r.registeredPhone) + "</div>";
    }

    const status = REQUEST_STATUS[r.status] || [r.status, "status-collected"];
    const open = r.status === "pending" || r.status === "code_given";

    let action = '<span class="small">Closed ' + shortDate(r.handledAt) + "</span>";
    if (open) {
      action = "";
      if (r.status === "code_given") {
        action += '<div class="small code-note" id="code-note-' + r.id + '">Code given, works until ' + shortDate(r.codeExpiresAt) + "</div>";
      }
      if (r.accountFound) {
        action +=
          '<div class="code-entry">' +
            '<input type="text" class="form-control code-input-small" id="code-input-' + r.id + '" ' +
              'maxlength="6" inputmode="numeric" placeholder="6 digits" aria-label="Code for ' + escapeHtml(r.email) + '">' +
            '<button class="btn btn-primary btn-sm" id="save-code-' + r.id + '" onclick="saveCode(' + r.id + ')">' +
              (r.status === "code_given" ? "Change code" : "Save code") + "</button>" +
          "</div>";
      }
      action += '<button class="btn btn-danger btn-sm" id="reject-' + r.id + '" onclick="rejectRequest(' + r.id + ')">Reject</button>';
    }

    rows +=
      '<tr id="request-' + r.id + '">' +
        '<td class="small">' + shortDate(r.createdAt) + "</td>" +
        "<td>" + account + "</td>" +
        "<td>" + phone + "</td>" +
        '<td class="request-message">' + (r.message ? escapeHtml(r.message) : '<span class="small">-</span>') + "</td>" +
        '<td><span class="status ' + status[1] + '">' + status[0] + "</span></td>" +
        "<td>" + action + "</td>" +
      "</tr>";
  }
  body.innerHTML = rows;
}

async function saveCode(requestId) {
  clearMessage("message");
  const code = document.getElementById("code-input-" + requestId).value.trim();
  if (!/^\d{6}$/.test(code)) {
    showMessage("message", "Please type exactly 6 digits for the code.", "error");
    return;
  }
  const result = await apiRequest("/api/admin/requests/" + requestId + "/code", "POST", { code: code });
  showMessage("message", result.message, result.ok ? "success" : "error");
  document.activeElement.blur();
  await refreshAll();
}

async function rejectRequest(requestId) {
  if (!confirm("Reject this password reset request?")) return;
  clearMessage("message");
  const result = await apiRequest("/api/admin/requests/" + requestId + "/reject", "POST");
  showMessage("message", result.message, result.ok ? "success" : "error");
  await refreshAll();
}

async function loadUsers() {
  const result = await apiRequest("/api/admin/users");
  if (!result.ok) return;
  allUsers = result.users;
  showUsers();
  fillActivityUserList();
}

function showUsers() {
  const search = document.getElementById("userSearch").value.trim().toLowerCase();
  const role = document.getElementById("userRoleFilter").value;
  const body = document.getElementById("usersBody");

  const users = allUsers.filter((u) => {
    const text = (u.name + " " + u.email + " " + u.phone + " " + u.area).toLowerCase();
    return (!role || u.role === role) && (!search || text.includes(search));
  });

  if (users.length === 0) {
    body.innerHTML = '<tr class="empty-row"><td colspan="9">No users match.</td></tr>';
    return;
  }

  let rows = "";
  for (const u of users) {
    const status = u.blocked
      ? '<span class="status status-expired">Blocked</span>'
      : '<span class="status status-available">Active</span>';

    rows +=
      '<tr id="user-' + u.id + '">' +
        '<td><div class="food-name">' + escapeHtml(u.name) + '</div><div class="small">' + escapeHtml(u.email) + "</div></td>" +
        "<td>" + rolePill(u.role) + "</td>" +
        '<td><a href="tel:' + escapeHtml(u.phone) + '">' + escapeHtml(u.phone) + "</a></td>" +
        "<td>" + escapeHtml(u.area) + '<div class="small">' + escapeHtml(u.address) + "</div></td>" +
        "<td>" + u.posts + "</td>" +
        "<td>" + u.claims + "</td>" +
        '<td class="small">' + shortDate(u.lastActive) + "</td>" +
        '<td class="user-status">' + status + "</td>" +
        '<td><div class="actions">' +
          '<button class="btn btn-primary btn-sm" id="edit-user-' + u.id + '" onclick="startEditUser(' + u.id + ')">Edit</button>' +
          '<button class="btn btn-outline btn-sm" id="block-' + u.id + '" onclick="toggleBlock(' + u.id + ')">' + (u.blocked ? "Unblock" : "Block") + "</button>" +
          '<button class="btn btn-outline btn-sm" id="history-' + u.id + '" onclick="showUserActivity(' + u.id + ')">Activity</button>' +
          '<button class="btn btn-danger btn-sm" id="delete-user-' + u.id + '" onclick="deleteUser(' + u.id + ')">Delete</button>' +
        "</div></td>" +
      "</tr>";
  }
  body.innerHTML = rows;
}

document.getElementById("userSearch").addEventListener("input", showUsers);
document.getElementById("userRoleFilter").addEventListener("change", showUsers);

function setUserModalMode(adding) {
  document.getElementById("userModalTitle").textContent = adding ? "Add user" : "Edit user";
  document.getElementById("saveUserBtn").textContent = adding ? "Add user" : "Save user";
  document.getElementById("editUserStatusGroup").classList.toggle("hidden", adding);
  document.getElementById("editUserPassword").required = adding;
  document.getElementById("editUserPasswordLabel").innerHTML = adding
    ? "Password"
    : 'New password <span class="optional">(leave empty to keep it)</span>';
}

function startAddUser() {
  clearMessage("userModalMessage");
  document.getElementById("userForm").reset();
  document.getElementById("editUserId").value = "";
  setUserModalMode(true);
  openModal("userModal");
}

document.getElementById("addUserBtn").addEventListener("click", startAddUser);

function startEditUser(userId) {
  const user = allUsers.find((u) => u.id === userId);
  clearMessage("userModalMessage");
  setUserModalMode(false);
  document.getElementById("editUserId").value = user.id;
  document.getElementById("editUserName").value = user.name;
  document.getElementById("editUserEmail").value = user.email;
  document.getElementById("editUserPhone").value = user.phone;
  document.getElementById("editUserArea").value = user.area;
  document.getElementById("editUserAddress").value = user.address;
  document.getElementById("editUserRole").value = user.role;
  document.getElementById("editUserStatus").value = user.blocked ? "blocked" : "active";
  document.getElementById("editUserPassword").value = "";
  openModal("userModal");
}

document.getElementById("userForm").addEventListener("submit", async function (event) {
  event.preventDefault();
  const userId = document.getElementById("editUserId").value;
  const details = {
    name: document.getElementById("editUserName").value.trim(),
    email: document.getElementById("editUserEmail").value.trim(),
    phone: document.getElementById("editUserPhone").value.trim(),
    area: document.getElementById("editUserArea").value,
    address: document.getElementById("editUserAddress").value.trim(),
    role: document.getElementById("editUserRole").value
  };

  let result;
  if (userId) {
    details.blocked = document.getElementById("editUserStatus").value === "blocked";
    details.newPassword = document.getElementById("editUserPassword").value;
    result = await apiRequest("/api/admin/users/" + userId, "PUT", details);
  } else {
    details.password = document.getElementById("editUserPassword").value;
    result = await apiRequest("/api/admin/users", "POST", details);
  }

  if (!result.ok) {
    showMessage("userModalMessage", result.message, "error");
    return;
  }
  closeModal("userModal");
  showMessage("message", result.message, "success");
  await refreshAll();
});

async function toggleBlock(userId) {
  const user = allUsers.find((u) => u.id === userId);
  const question = user.blocked ? "Unblock " + user.name + "?" : "Block " + user.name + "? They won't be able to log in.";
  if (!confirm(question)) return;
  const result = await apiRequest("/api/admin/users/" + userId + "/block", "PUT");
  showMessage("message", result.message, result.ok ? "success" : "error");
  await refreshAll();
}

async function deleteUser(userId) {
  const user = allUsers.find((u) => u.id === userId);
  if (!confirm("Delete " + user.name + "? Their food posts and waiting claims are removed. This cannot be undone.")) return;
  const result = await apiRequest("/api/admin/users/" + userId, "DELETE");
  showMessage("message", result.message, result.ok ? "success" : "error");
  await refreshAll();
}

async function loadFoods() {
  const result = await apiRequest("/api/admin/foods");
  const body = document.getElementById("foodsBody");
  if (!result.ok) return;
  allFoods = result.foods;
  if (allFoods.length === 0) {
    body.innerHTML = '<tr class="empty-row"><td colspan="7">No food posts.</td></tr>';
    return;
  }

  let rows = "";
  for (const f of allFoods) {
    rows +=
      '<tr id="admin-food-' + f.id + '">' +
        '<td><div class="food-name">' + foodEmoji(f.foodType) + " " + escapeHtml(f.title) + '</div><div class="small">' + escapeHtml(f.foodType) + "</div></td>" +
        "<td>" + escapeHtml(f.donorName) + "</td>" +
        "<td>" + escapeHtml(f.area) + '<div class="small">' + escapeHtml(f.location) + "</div></td>" +
        '<td class="admin-servings">' + f.remaining + " left of " + f.quantity +
          (f.waitingClaims ? '<div class="small">' + f.waitingClaims + " pickup(s) waiting</div>" : "") + "</td>" +
        '<td><span class="status status-' + f.status + '">' + FOOD_STATUS[f.status] + "</span></td>" +
        '<td class="small">' + shortDate(f.createdAt) + "</td>" +
        '<td><div class="actions">' +
          '<button class="btn btn-primary btn-sm" id="edit-food-' + f.id + '" onclick="startEditFood(' + f.id + ')">Edit</button>' +
          '<button class="btn btn-danger btn-sm" id="delete-food-' + f.id + '" onclick="deleteFoodPost(' + f.id + ')">Delete</button>' +
        "</div></td>" +
      "</tr>";
  }
  body.innerHTML = rows;
}

function setFoodModalMode(adding) {
  document.getElementById("foodModalTitle").textContent = adding ? "Add food post" : "Edit food post";
  document.getElementById("saveFoodEditBtn").textContent = adding ? "Add food post" : "Save food post";
  document.getElementById("editFoodDonorGroup").classList.toggle("hidden", !adding);
  document.getElementById("editFoodDonor").required = adding;
}

function startAddFood() {
  const donors = allUsers.filter((u) => u.role === "donor");
  let options = '<option value="">Select a donor</option>';
  for (const d of donors) {
    options += '<option value="' + d.id + '">' + escapeHtml(d.name) + " (" + escapeHtml(d.area) + ")</option>";
  }

  clearMessage("foodModalMessage");
  document.getElementById("foodEditForm").reset();
  document.getElementById("editFoodId").value = "";
  document.getElementById("editFoodDonor").innerHTML = options;
  document.getElementById("editFoodQuantity").min = 1;
  document.getElementById("editFoodClaimed").textContent = "";
  document.getElementById("editFoodHours").value = 6;
  setFoodModalMode(true);
  openModal("foodModal");
}

document.getElementById("addFoodBtn").addEventListener("click", startAddFood);

document.getElementById("editFoodDonor").addEventListener("change", function () {
  const donor = allUsers.find((u) => u.id === Number(this.value));
  if (!donor) return;
  document.getElementById("editFoodArea").value = donor.area;
  document.getElementById("editFoodLocation").value = donor.address;
});

function startEditFood(foodId) {
  const food = allFoods.find((f) => f.id === foodId);
  setFoodModalMode(false);
  const claimed = food.quantity - food.remaining;
  const hoursLeft = Math.ceil((new Date(food.expiresAt).getTime() - Date.now()) / 3600000);

  clearMessage("foodModalMessage");
  document.getElementById("editFoodId").value = food.id;
  document.getElementById("editFoodTitle").value = food.title;
  document.getElementById("editFoodType").value = food.foodType;
  document.getElementById("editFoodQuantity").value = food.quantity;
  document.getElementById("editFoodQuantity").min = Math.max(claimed, 1);
  document.getElementById("editFoodClaimed").textContent =
    claimed > 0 ? "Collectors already took " + claimed + " servings, so the total can't go below " + claimed + "." : "Nobody has claimed this food yet.";
  document.getElementById("editFoodArea").value = food.area;
  document.getElementById("editFoodLocation").value = food.location;
  document.getElementById("editFoodHours").value = Math.min(Math.max(hoursLeft, 1), 48);
  document.getElementById("editFoodNotes").value = food.notes || "";
  openModal("foodModal");
}

document.getElementById("foodEditForm").addEventListener("submit", async function (event) {
  event.preventDefault();
  const foodId = document.getElementById("editFoodId").value;
  const details = {
    title: document.getElementById("editFoodTitle").value.trim(),
    foodType: document.getElementById("editFoodType").value,
    quantity: Number(document.getElementById("editFoodQuantity").value),
    area: document.getElementById("editFoodArea").value,
    location: document.getElementById("editFoodLocation").value.trim(),
    expiryHours: Number(document.getElementById("editFoodHours").value),
    notes: document.getElementById("editFoodNotes").value.trim()
  };

  let result;
  if (foodId) {
    result = await apiRequest("/api/admin/foods/" + foodId, "PUT", details);
  } else {
    details.donorId = Number(document.getElementById("editFoodDonor").value);
    result = await apiRequest("/api/admin/foods", "POST", details);
  }

  if (!result.ok) {
    showMessage("foodModalMessage", result.message, "error");
    return;
  }
  closeModal("foodModal");
  showMessage("message", result.message, "success");
  await refreshAll();
});

async function deleteFoodPost(foodId) {
  if (!confirm("Delete this food post? Waiting claims on it are cancelled.")) return;
  const result = await apiRequest("/api/admin/foods/" + foodId, "DELETE");
  showMessage("message", result.message, result.ok ? "success" : "error");
  await refreshAll();
}

async function loadClaims() {
  const result = await apiRequest("/api/admin/claims");
  const body = document.getElementById("claimsBody");
  if (!result.ok) return;
  if (result.claims.length === 0) {
    body.innerHTML = '<tr class="empty-row"><td colspan="7">No claims yet.</td></tr>';
    return;
  }

  let rows = "";
  for (const c of result.claims) {
    const waiting = c.status === "claimed";
    const status = waiting
      ? '<span class="status status-claimed">Waiting for pickup</span>'
      : '<span class="status status-collected">Collected</span>';

    let buttons = "";
    if (waiting) {
      buttons += '<button class="btn btn-primary btn-sm" id="confirm-claim-' + c.id + '" onclick="confirmClaim(' + c.id + ')">Confirm pickup</button>';
    }
    buttons += '<button class="btn btn-danger btn-sm" id="cancel-claim-' + c.id + '" onclick="cancelClaim(' + c.id + ')">Cancel claim</button>';

    rows +=
      '<tr id="admin-claim-' + c.id + '">' +
        '<td><div class="food-name">' + foodEmoji(c.foodType) + " " + escapeHtml(c.title) + '</div><div class="small">' + escapeHtml(c.area) + "</div></td>" +
        "<td>" + c.quantity + "</td>" +
        "<td>" + escapeHtml(c.collectorName) + "</td>" +
        "<td>" + escapeHtml(c.donorName) + "</td>" +
        '<td class="small">' + shortDate(c.claimedAt) + "</td>" +
        '<td class="claim-status">' + status + "</td>" +
        '<td><div class="actions">' + buttons + "</div></td>" +
      "</tr>";
  }
  body.innerHTML = rows;
}

function startAddClaim() {
  const foods = allFoods.filter((f) => f.remaining > 0);
  const collectors = allUsers.filter((u) => u.role === "collector");

  let foodOptions = '<option value="">Select a food post</option>';
  for (const f of foods) {
    foodOptions += '<option value="' + f.id + '">' + escapeHtml(f.title) + " (" + f.remaining + " left, " + escapeHtml(f.donorName) + ")</option>";
  }
  let collectorOptions = '<option value="">Select a collector</option>';
  for (const c of collectors) {
    collectorOptions += '<option value="' + c.id + '">' + escapeHtml(c.name) + " (" + escapeHtml(c.area) + ")</option>";
  }

  clearMessage("claimModalMessage");
  document.getElementById("claimForm").reset();
  document.getElementById("newClaimFood").innerHTML = foodOptions;
  document.getElementById("newClaimCollector").innerHTML = collectorOptions;
  document.getElementById("newClaimQuantity").removeAttribute("max");
  openModal("claimModal");
}

document.getElementById("addClaimBtn").addEventListener("click", startAddClaim);

document.getElementById("newClaimFood").addEventListener("change", function () {
  const food = allFoods.find((f) => f.id === Number(this.value));
  const box = document.getElementById("newClaimQuantity");
  if (food) {
    box.max = food.remaining;
  } else {
    box.removeAttribute("max");
  }
});

document.getElementById("claimForm").addEventListener("submit", async function (event) {
  event.preventDefault();
  const result = await apiRequest("/api/admin/claims", "POST", {
    foodId: Number(document.getElementById("newClaimFood").value),
    collectorId: Number(document.getElementById("newClaimCollector").value),
    quantity: Number(document.getElementById("newClaimQuantity").value)
  });

  if (!result.ok) {
    showMessage("claimModalMessage", result.message, "error");
    return;
  }
  closeModal("claimModal");
  showMessage("message", result.message, "success");
  await refreshAll();
});

async function confirmClaim(claimId) {
  const result = await apiRequest("/api/admin/claims/" + claimId + "/confirm", "PUT");
  showMessage("message", result.message, result.ok ? "success" : "error");
  await refreshAll();
}

async function cancelClaim(claimId) {
  if (!confirm("Cancel this claim? Waiting servings go back to the food post.")) return;
  const result = await apiRequest("/api/admin/claims/" + claimId, "DELETE");
  showMessage("message", result.message, result.ok ? "success" : "error");
  await refreshAll();
}

function fillActivityUserList() {
  const select = document.getElementById("activityUser");
  const selected = select.value;
  let options = '<option value="">Everyone</option>';
  for (const u of allUsers) {
    options += '<option value="' + u.id + '">' + escapeHtml(u.name) + " (" + u.role + ")</option>";
  }
  select.innerHTML = options;
  select.value = selected;
}

async function loadActivity() {
  const userId = document.getElementById("activityUser").value;
  const search = document.getElementById("activitySearch").value.trim();
  const params = new URLSearchParams();
  if (userId) params.append("userId", userId);
  if (search) params.append("search", search);

  const result = await apiRequest("/api/admin/activity?" + params.toString());
  const body = document.getElementById("activityBody");
  if (!result.ok) return;
  if (result.activity.length === 0) {
    body.innerHTML = '<tr class="empty-row"><td colspan="4">Nothing found.</td></tr>';
    return;
  }

  let rows = "";
  for (const a of result.activity) {
    rows +=
      '<tr class="activity-row">' +
        '<td class="small">' + shortDate(a.at) + "</td>" +
        "<td>" + escapeHtml(a.userName) + " " + rolePill(a.role) + "</td>" +
        '<td class="activity-action">' + escapeHtml(a.action) + "</td>" +
        '<td class="small">' + escapeHtml(a.details) + "</td>" +
      "</tr>";
  }
  body.innerHTML = rows;
}

function showUserActivity(userId) {
  document.getElementById("activityUser").value = String(userId);
  document.getElementById("activitySearch").value = "";
  openTab("tab-activity");
  loadActivity();
}

document.getElementById("activityFilterBtn").addEventListener("click", loadActivity);
document.getElementById("activitySearch").addEventListener("keydown", (event) => {
  if (event.key === "Enter") loadActivity();
});

async function refreshAll() {
  await loadOverview();
  await loadRequests();
  await loadUsers();
  await loadFoods();
  await loadClaims();
  await loadActivity();
}

async function startPage() {
  const user = await protectPage("admin");
  if (!user) return;
  setupLogout();
  await fillAreaSelect("editUserArea", "Select area");
  await fillAreaSelect("editFoodArea", "Select area");
  await refreshAll();
  setInterval(async () => {
    await loadOverview();
    await loadRequests();
  }, 15000);
}

startPage();
