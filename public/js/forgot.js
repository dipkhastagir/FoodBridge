document.getElementById("forgotForm").addEventListener("submit", async function (event) {
  event.preventDefault();
  clearMessage("message");

  const email = document.getElementById("email").value.trim();
  const phone = document.getElementById("phone").value.trim();
  const message = document.getElementById("requestMessage").value.trim();

  const button = document.getElementById("sendRequestBtn");
  button.disabled = true;
  button.textContent = "Sending...";

  const result = await apiRequest("/api/forgot-password", "POST", { email, phone, message });

  button.disabled = false;
  button.textContent = "Send request to admin";

  if (!result.ok) {
    showMessage("message", result.message, "error");
    return;
  }

  showMessage("message", result.message, "success");

  setTimeout(function () {
    window.location.href = "reset-password.html?email=" + encodeURIComponent(email);
  }, 2000);
});
