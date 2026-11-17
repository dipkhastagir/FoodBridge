function fillProfile(user) {
  document.getElementById("profileEmail").textContent = user.email;
  document.getElementById("profileName").value = user.name;
  document.getElementById("profilePhone").value = user.phone || "";
  document.getElementById("profileArea").value = user.area || "";
  document.getElementById("profileAddress").value = user.address || "";
  document.getElementById("navUserName").textContent = user.name;
}

document.getElementById("profileForm").addEventListener("submit", async function (event) {
  event.preventDefault();
  clearMessage("profileMessage");

  const result = await apiRequest("/api/profile", "PUT", {
    name: document.getElementById("profileName").value.trim(),
    phone: document.getElementById("profilePhone").value.trim(),
    area: document.getElementById("profileArea").value,
    address: document.getElementById("profileAddress").value.trim()
  });

  if (result.ok) {
    fillProfile(result.user);
    showMessage("profileMessage", result.message, "success");
  } else {
    showMessage("profileMessage", result.message, "error");
  }
});

document.getElementById("passwordForm").addEventListener("submit", async function (event) {
  event.preventDefault();
  clearMessage("passwordMessage");

  const currentPassword = document.getElementById("currentPassword").value;
  const newPassword = document.getElementById("newPassword").value;
  const confirmNewPassword = document.getElementById("confirmNewPassword").value;

  if (newPassword.length < 6) {
    showMessage("passwordMessage", "New password must be at least 6 characters long.", "error");
    return;
  }
  if (newPassword !== confirmNewPassword) {
    showMessage("passwordMessage", "New passwords do not match.", "error");
    return;
  }

  const result = await apiRequest("/api/change-password", "PUT", { currentPassword, newPassword });

  if (result.ok) {
    document.getElementById("passwordForm").reset();
    showMessage("passwordMessage", result.message, "success");
  } else {
    showMessage("passwordMessage", result.message, "error");
  }
});

async function startPage() {
  const user = await protectPage();
  if (!user) return;

  document.getElementById("navDashboard").href = dashboardFor(user.role);
  await fillAreaSelect("profileArea", "Select your area", user.area);
  fillProfile(user);
  setupLogout();
}

startPage();
