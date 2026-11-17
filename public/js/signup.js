const signupForm = document.getElementById("signupForm");

fillAreaSelect("area", "Select your area");

signupForm.addEventListener("submit", async function (event) {
  event.preventDefault();
  clearMessage("message");

  const name = document.getElementById("name").value.trim();
  const email = document.getElementById("email").value.trim();
  const phone = document.getElementById("phone").value.trim();
  const role = document.getElementById("role").value;
  const area = document.getElementById("area").value;
  const address = document.getElementById("address").value.trim();
  const password = document.getElementById("password").value;
  const confirmPassword = document.getElementById("confirmPassword").value;

  if (name === "" || address === "") {
    showMessage("message", "Name and address cannot be only spaces.", "error");
    return;
  }
  if (!/^01[3-9][0-9]{8}$/.test(phone)) {
    showMessage("message", "Mobile number must be exactly 11 digits starting with 01, e.g. 01711223344.", "error");
    return;
  }
  if (password.length < 6) {
    showMessage("message", "Password must be at least 6 characters long.", "error");
    return;
  }
  if (password !== confirmPassword) {
    showMessage("message", "Passwords do not match.", "error");
    return;
  }

  const button = document.getElementById("signupBtn");
  button.disabled = true;

  const result = await apiRequest("/api/signup", "POST", {
    name, email, phone, role, area, address, password, confirmPassword
  });

  button.disabled = false;

  if (result.ok) {
    showMessage("message", result.message, "success");
    signupForm.reset();
    setTimeout(function () {
      window.location.href = "login.html";
    }, 2000);
  } else {
    showMessage("message", result.message, "error");
  }
});
