function makeHeroTicket(food, extraClass) {
  return (
    '<div class="ticket ' + extraClass + '">' +
      '<div class="ticket-top">' +
        '<div class="ticket-head">' +
          '<span class="ticket-emoji">' + foodEmoji(food.foodType) + "</span>" +
          '<span class="type-pill">' + escapeHtml(food.foodType) + "</span>" +
        "</div>" +
        "<h3>" + escapeHtml(food.title) + "</h3>" +
        '<div class="ticket-info">📍 ' + escapeHtml(food.area) + "</div>" +
        '<div class="ticket-info">🏪 ' + escapeHtml(food.donorName) + "</div>" +
      "</div>" +
      '<div class="ticket-bottom">' +
        '<span class="qty">' + food.remaining + " <small>servings left</small></span>" +
        '<span class="time-left">' + timeLeft(food.expiresAt) + "</span>" +
      "</div>" +
    "</div>"
  );
}

async function loadHomePage() {
  const stats = await apiRequest("/api/public/stats");
  if (stats.ok) {
    const liveText = document.getElementById("liveText");
    if (stats.availableFood === 0) {
      liveText.textContent = "Nothing is waiting right now. Donors post new food every day.";
    } else {
      const word = stats.availableFood === 1 ? "donation" : "donations";
      liveText.textContent = stats.availableFood + " " + word + " (" + stats.servingsWaiting +
        " servings) waiting for a collector right now.";
    }

    if (stats.servingsShared > 0) {
      document.getElementById("sharedLine").textContent =
        stats.servingsShared + " servings have already reached people through FoodBridge.";
    }
    document.getElementById("donorCount").textContent =
      stats.donors + (stats.donors === 1 ? " donor is" : " donors are") + " already sharing food";
    document.getElementById("collectorCount").textContent =
      stats.collectors + (stats.collectors === 1 ? " collector is" : " collectors are") + " already picking up";
  } else {
    document.getElementById("liveLine").classList.add("hidden");
  }

  const result = await apiRequest("/api/public/foods");
  if (result.ok && result.foods.length > 0) {
    let html = makeHeroTicket(result.foods[0], "");
    if (result.foods[1]) html += makeHeroTicket(result.foods[1], "second");
    document.getElementById("heroTickets").innerHTML = html;
  }
}

async function setupTopButtons() {
  const result = await apiRequest("/api/me");
  if (!result.ok) return;

  const firstButton = document.getElementById("navLoginBtn");
  const secondButton = document.getElementById("navSignupBtn");

  secondButton.textContent = "Go to dashboard";
  secondButton.href = dashboardFor(result.user.role);

  firstButton.textContent = "Log out";
  firstButton.href = "#";
  firstButton.addEventListener("click", async function (event) {
    event.preventDefault();
    await apiRequest("/api/logout", "POST");
    window.location.reload();
  });
}

loadHomePage();
setupTopButtons();
