const params = new URLSearchParams(window.location.search);
const emailBox = document.getElementById("resetEmail");
emailBox.value = params.get("email") || "";

const STATUS_TEXT = {
  pending: ["waiting", "⏳ Your request is waiting for the admin. Keep your phone nearby."],
  code_given: ["ready", "📞 The admin has given you a code. Enter it below."],
  rejected: ["rejected", "The admin rejected your request. Check your email and mobile number and send a new request."],
  replaced: ["rejected", "This request was replaced by a newer one."],
  verified: ["ready", "Code already verified. Choose your new password."],
  done: ["ready", "Your password was already reset. You can log in."]
};

async function checkStatus() {
  const email = emailBox.value.trim();
  const box = document.getElementById("requestStatus");
  if (!email) {
    box.classList.add("hidden");
    return;
  }

  const result = await apiRequest("/api/forgot-password/status?email=" + encodeURIComponent(email));
  const info = result.ok ? STATUS_TEXT[result.status] : null;
  if (!info) {
    box.classList.add("hidden");
    return;
  }
  box.className = "request-status " + info[0];
  box.textContent = info[1];
}

checkStatus();
setInterval(checkStatus, 8000);
emailBox.addEventListener("change", checkStatus);

document.getElementById("codeForm").addEventListener("submit", async function (event) {
  event.preventDefault();
  clearMessage("message");

  const email = emailBox.value.trim();
  const code = document.getElementById("code").value.trim();
  const result = await apiRequest("/api/verify-reset-code", "POST", { email: email, code: code });

  if (!result.ok) {
    showMessage("message", result.message, "error");
    return;
  }

  document.getElementById("codeStep").classList.add("hidden");
  document.getElementById("passwordStep").classList.remove("hidden");
  document.getElementById("sideStepCode").className = "done";
  document.getElementById("sideStepPassword").className = "current";
  showMessage("passwordMessage", result.message, "success");
  document.getElementById("newPassword").focus();
});

document.getElementById("newPasswordForm").addEventListener("submit", async function (event) {
  event.preventDefault();
  clearMessage("passwordMessage");

  const newPassword = document.getElementById("newPassword").value;
  const confirmPassword = document.getElementById("confirmPassword").value;

  if (newPassword.length < 6) {
    showMessage("passwordMessage", "New password must be at least 6 characters long.", "error");
    return;
  }
  if (newPassword !== confirmPassword) {
    showMessage("passwordMessage", "Passwords do not match.", "error");
    return;
  }

  const result = await apiRequest("/api/reset-password", "POST", { newPassword, confirmPassword });

  if (result.ok) {
    document.getElementById("newPasswordForm").reset();
    showMessage("passwordMessage", result.message, "success");
    setTimeout(function () {
      window.location.href = "login.html";
    }, 2500);
  } else {
    showMessage("passwordMessage", result.message, "error");
  }
});
