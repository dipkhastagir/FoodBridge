const loginForm = document.getElementById("loginForm");
const loginInputs = [document.getElementById("email"), document.getElementById("password")];

for (const input of loginInputs) {
  input.value = "";
  input.addEventListener("focus", function () {
    input.removeAttribute("readonly");
  });
}

window.addEventListener("pageshow", function () {
  loginForm.reset();
});

document.getElementById("loginBtn").addEventListener("click", function () {
  for (const input of loginInputs) {
    input.removeAttribute("readonly");
  }
});

loginForm.addEventListener("submit", async function (event) {
  event.preventDefault();
  clearMessage("message");

  const email = document.getElementById("email").value.trim();
  const password = document.getElementById("password").value;

  const button = document.getElementById("loginBtn");
  button.disabled = true;

  const result = await apiRequest("/api/login", "POST", { email, password });

  button.disabled = false;

  if (result.ok) {
    showMessage("message", result.message, "success");
    window.location.href = dashboardFor(result.user.role);
  } else {
    showMessage("message", result.message, "error");
  }
});
