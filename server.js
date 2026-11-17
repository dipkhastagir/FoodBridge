const express = require("express");
const session = require("express-session");
const bcrypt = require("bcryptjs");
const crypto = require("crypto");
const path = require("path");
const db = require("./database");

const app = express();
const PORT = 3000;

const FOOD_TYPES = ["Cooked Meal", "Bakery", "Fruits & Vegetables", "Dry Food", "Drinks & Dairy"];

app.use(express.json());

app.use(
  session({
    secret: "foodbridge-secret-key",
    resave: false,
    saveUninitialized: false,
    cookie: { maxAge: 2 * 60 * 60 * 1000 }
  })
);

app.use(express.static(path.join(__dirname, "public")));

function isValidEmail(email) {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
}

function cleanPhone(phone) {
  return String(phone || "").replace(/[\s-]/g, "");
}
function isValidPhone(phone) {
  return /^01[3-9]\d{8}$/.test(cleanPhone(phone));
}

function isValidArea(area) {
  return db.AREAS.includes(area);
}

function safeUser(user) {
  return {
    id: user.id,
    name: user.name,
    email: user.email,
    phone: user.phone,
    area: user.area,
    address: user.address,
    role: user.role
  };
}

function findUser(data, id) {
  return data.users.find((u) => u.id === id);
}

function logActivity(data, user, action, details) {
  data.activity.push({
    id: data.nextActivityId,
    at: new Date().toISOString(),
    userId: user ? user.id : null,
    userName: user ? user.name : "Visitor",
    role: user ? user.role : "visitor",
    action: action,
    details: details || ""
  });
  data.nextActivityId++;
  if (data.activity.length > 2000) {
    data.activity.splice(0, data.activity.length - 2000);
  }
}

function isExpired(food) {
  return new Date(food.expiresAt).getTime() < Date.now();
}

function foodStatus(food, data) {
  if (food.remaining > 0) {
    return isExpired(food) ? "expired" : "available";
  }
  const waiting = data.claims.some((c) => c.foodId === food.id && c.status === "claimed");
  return waiting ? "claimed" : "collected";
}

function validateFood(body) {
  const title = (body.title || "").trim();
  const location = (body.location || "").trim();
  const quantity = Number(body.quantity);
  const expiryHours = Number(body.expiryHours);

  if (!title) return "Food title is required.";
  if (!FOOD_TYPES.includes(body.foodType)) return "Please select a valid food type.";
  if (!Number.isInteger(quantity) || quantity < 1 || quantity > 1000) {
    return "Quantity must be a whole number between 1 and 1000.";
  }
  if (!isValidArea(body.area)) return "Please select the pickup area.";
  if (!location) return "Pickup address is required.";
  if (!Number.isInteger(expiryHours) || expiryHours < 1 || expiryHours > 48) {
    return "Expiry time must be between 1 and 48 hours.";
  }
  return "";
}

function maskEmail(email) {
  const [name, domain] = email.split("@");
  return name.charAt(0) + "*".repeat(Math.max(name.length - 1, 3)) + "@" + domain;
}

function requireLogin(role) {
  return function (req, res, next) {
    if (!req.session.userId) {
      return res.status(401).json({ message: "Please login first." });
    }
    const data = db.readData();
    const user = findUser(data, req.session.userId);
    if (!user) {
      return res.status(401).json({ message: "Please login first." });
    }
    if (user.blocked) {
      req.session.destroy(() => {});
      return res.status(401).json({ message: "Your account is blocked. Please contact the admin." });
    }
    if (role && user.role !== role) {
      return res.status(403).json({ message: "You are not allowed to do this." });
    }
    req.user = user;
    next();
  };
}

app.post("/api/signup", (req, res) => {
  const name = (req.body.name || "").trim();
  const email = (req.body.email || "").trim().toLowerCase();
  const phone = cleanPhone(req.body.phone);
  const area = req.body.area;
  const address = (req.body.address || "").trim();
  const role = req.body.role;
  const password = req.body.password || "";
  const confirmPassword = req.body.confirmPassword || "";

  if (!name || !email || !phone || !area || !address || !password || !confirmPassword || !role) {
    return res.status(400).json({ message: "Please fill in all required fields." });
  }
  if (!isValidEmail(email)) {
    return res.status(400).json({ message: "Please enter a valid email address." });
  }
  if (!isValidPhone(phone)) {
    return res.status(400).json({ message: "Mobile number must be exactly 11 digits starting with 01, e.g. 01711223344." });
  }
  if (!isValidArea(area)) {
    return res.status(400).json({ message: "Please select your area." });
  }
  if (role !== "donor" && role !== "collector") {
    return res.status(400).json({ message: "Please select a valid role." });
  }
  if (password.length < 6) {
    return res.status(400).json({ message: "Password must be at least 6 characters long." });
  }
  if (password !== confirmPassword) {
    return res.status(400).json({ message: "Passwords do not match." });
  }

  const data = db.readData();
  if (data.users.some((u) => u.email === email)) {
    return res.status(400).json({ message: "This email is already registered." });
  }

  data.users.push({
    id: data.nextUserId,
    name,
    email,
    phone,
    area,
    address,
    role,
    blocked: false,
    password: bcrypt.hashSync(password, 10),
    createdAt: new Date().toISOString()
  });
  logActivity(data, data.users[data.users.length - 1], "Signed up", "as a " + role + " in " + area);
  data.nextUserId++;
  db.saveData(data);

  res.json({ message: "Account created successfully! Please login." });
});

app.post("/api/login", (req, res) => {
  const email = (req.body.email || "").trim().toLowerCase();
  const password = req.body.password || "";

  if (!email || !password) {
    return res.status(400).json({ message: "Email and password are required." });
  }

  const data = db.readData();
  const user = data.users.find((u) => u.email === email);

  if (!user || !bcrypt.compareSync(password, user.password)) {
    return res.status(401).json({ message: "Invalid email or password." });
  }
  if (user.blocked) {
    return res.status(403).json({ message: "Your account is blocked. Please contact the admin." });
  }

  req.session.userId = user.id;
  logActivity(data, user, "Logged in", "");
  db.saveData(data);
  res.json({ message: "Login successful!", user: safeUser(user) });
});

app.post("/api/logout", (req, res) => {
  const data = db.readData();
  const user = findUser(data, req.session.userId);
  if (user) {
    logActivity(data, user, "Logged out", "");
    db.saveData(data);
  }
  req.session.destroy(() => {
    res.json({ message: "Logged out successfully." });
  });
});

app.get("/api/me", requireLogin(), (req, res) => {
  res.json({ user: safeUser(req.user) });
});

app.put("/api/profile", requireLogin(), (req, res) => {
  const name = (req.body.name || "").trim();
  const phone = cleanPhone(req.body.phone);
  const area = req.body.area;
  const address = (req.body.address || "").trim();

  if (!name || !address) {
    return res.status(400).json({ message: "Name and address cannot be empty." });
  }
  if (!isValidPhone(phone)) {
    return res.status(400).json({ message: "Mobile number must be exactly 11 digits starting with 01, e.g. 01711223344." });
  }
  if (!isValidArea(area)) {
    return res.status(400).json({ message: "Please select your area." });
  }

  const data = db.readData();
  const user = findUser(data, req.user.id);
  user.name = name;
  user.phone = phone;
  user.area = area;
  user.address = address;
  logActivity(data, user, "Updated profile", "Phone " + phone + ", " + area);
  db.saveData(data);

  res.json({ message: "Profile updated successfully.", user: safeUser(user) });
});

app.put("/api/change-password", requireLogin(), (req, res) => {
  const currentPassword = req.body.currentPassword || "";
  const newPassword = req.body.newPassword || "";

  if (!currentPassword || !newPassword) {
    return res.status(400).json({ message: "Please fill in all password fields." });
  }

  const data = db.readData();
  const user = findUser(data, req.user.id);

  if (!bcrypt.compareSync(currentPassword, user.password)) {
    return res.status(400).json({ message: "Current password is incorrect." });
  }
  if (newPassword.length < 6) {
    return res.status(400).json({ message: "New password must be at least 6 characters long." });
  }

  user.password = bcrypt.hashSync(newPassword, 10);
  logActivity(data, user, "Changed password", "");
  db.saveData(data);
  res.json({ message: "Password changed successfully." });
});

app.put("/api/switch-role", requireLogin(), (req, res) => {
  const data = db.readData();
  const user = findUser(data, req.user.id);
  if (user.role === "admin") {
    return res.status(400).json({ message: "The admin role can't be switched." });
  }
  user.role = user.role === "donor" ? "collector" : "donor";
  logActivity(data, user, "Switched role", "now a " + user.role);
  db.saveData(data);

  const label = user.role === "donor" ? "Donor" : "Collector";
  res.json({ message: "You are now using FoodBridge as a " + label + ".", user: safeUser(user) });
});

const CODE_HOURS = 2;
const MAX_TRIES = 5;

function newestRequest(data, email) {
  const list = data.resetRequests.filter((r) => r.email === email);
  return list[list.length - 1];
}

app.post("/api/forgot-password", (req, res) => {
  const email = (req.body.email || "").trim().toLowerCase();
  const phone = cleanPhone(req.body.phone);
  const message = (req.body.message || "").trim().slice(0, 300);

  if (!isValidEmail(email)) {
    return res.status(400).json({ message: "Please enter a valid email address." });
  }
  if (!isValidPhone(phone)) {
    return res.status(400).json({ message: "Mobile number must be exactly 11 digits starting with 01, e.g. 01711223344." });
  }

  const data = db.readData();
  const user = data.users.find((u) => u.email === email);

  for (const old of data.resetRequests) {
    if (old.email === email && (old.status === "pending" || old.status === "code_given")) {
      old.status = "replaced";
    }
  }

  data.resetRequests.push({
    id: data.nextRequestId,
    email: email,
    userId: user ? user.id : null,
    phoneGiven: phone,
    message: message,
    status: "pending",
    codeHash: null,
    codeExpiresAt: null,
    tries: 0,
    createdAt: new Date().toISOString(),
    handledAt: null
  });
  data.nextRequestId++;
  logActivity(data, user, "Asked for password reset", email + ", mobile " + phone);
  db.saveData(data);

  res.json({ message: "Your request was sent to the admin. The admin will call your mobile number and give you a 6-digit code." });
});

app.get("/api/forgot-password/status", (req, res) => {
  const email = (req.query.email || "").trim().toLowerCase();
  const data = db.readData();
  const request = newestRequest(data, email);
  res.json({ status: request ? request.status : "none" });
});

app.post("/api/verify-reset-code", (req, res) => {
  const email = (req.body.email || "").trim().toLowerCase();
  const code = (req.body.code || "").trim();

  if (!/^\d{6}$/.test(code)) {
    return res.status(400).json({ message: "The code must be 6 digits." });
  }

  const data = db.readData();
  const request = newestRequest(data, email);

  if (!request || request.status === "pending") {
    return res.status(400).json({ message: "The admin has not given you a code yet. Please wait for their call." });
  }
  if (request.status === "rejected") {
    return res.status(400).json({ message: "The admin rejected this request. Please send a new request." });
  }
  if (request.status !== "code_given") {
    return res.status(400).json({ message: "This request is closed. Please send a new request." });
  }
  if (new Date(request.codeExpiresAt).getTime() < Date.now()) {
    return res.status(400).json({ message: "This code has expired. Please send a new request." });
  }
  if (request.tries >= MAX_TRIES) {
    return res.status(400).json({ message: "Too many wrong codes. Please send a new request." });
  }
  if (!bcrypt.compareSync(code, request.codeHash)) {
    request.tries++;
    db.saveData(data);
    const left = MAX_TRIES - request.tries;
    return res.status(400).json({ message: "Wrong code. You have " + left + " tries left." });
  }

  request.status = "verified";
  db.saveData(data);
  req.session.resetUserId = request.userId;
  req.session.resetRequestId = request.id;
  req.session.resetUntil = Date.now() + 10 * 60 * 1000;
  res.json({ message: "Code verified. Now choose a new password." });
});

app.post("/api/reset-password", (req, res) => {
  const newPassword = req.body.newPassword || "";
  const confirmPassword = req.body.confirmPassword || "";

  if (!req.session.resetUserId || Date.now() > req.session.resetUntil) {
    return res.status(400).json({ message: "Please verify the code from the admin first." });
  }
  if (newPassword.length < 6) {
    return res.status(400).json({ message: "New password must be at least 6 characters long." });
  }
  if (newPassword !== confirmPassword) {
    return res.status(400).json({ message: "Passwords do not match." });
  }

  const data = db.readData();
  const user = findUser(data, req.session.resetUserId);
  const request = data.resetRequests.find((r) => r.id === req.session.resetRequestId);
  if (!user) {
    return res.status(400).json({ message: "This account no longer exists." });
  }

  user.password = bcrypt.hashSync(newPassword, 10);
  if (request) request.status = "done";
  logActivity(data, user, "Reset password", "with a code from the admin");
  db.saveData(data);

  delete req.session.resetUserId;
  delete req.session.resetRequestId;
  delete req.session.resetUntil;
  res.json({ message: "Password reset successfully! You can log in with your new password." });
});

app.get("/api/donor/foods", requireLogin("donor"), (req, res) => {
  const data = db.readData();
  const myFoods = data.foods.filter((f) => f.donorId === req.user.id);
  const myFoodIds = myFoods.map((f) => f.id);

  const foods = myFoods
    .sort((a, b) => b.id - a.id)
    .map((f) => {
      const claims = data.claims.filter((c) => c.foodId === f.id);
      return {
        ...f,
        status: foodStatus(f, data),
        claimCount: claims.length,
        waitingCount: claims.filter((c) => c.status === "claimed").length,
        collectedServings: claims.filter((c) => c.status === "collected").reduce((s, c) => s + c.quantity, 0)
      };
    });

  const confirmations = data.claims
    .filter((c) => myFoodIds.includes(c.foodId) && c.status === "claimed")
    .map((c) => {
      const collector = findUser(data, c.collectorId);
      return {
        ...c,
        collectorName: collector ? collector.name : "Unknown",
        collectorPhone: collector ? collector.phone : "",
        collectorArea: collector ? collector.area : "",
        collectorAddress: collector ? collector.address : ""
      };
    });

  const myClaims = data.claims.filter((c) => myFoodIds.includes(c.foodId));
  const stats = {
    total: foods.length,
    servingsLeft: foods.filter((f) => f.status === "available").reduce((s, f) => s + f.remaining, 0),
    waiting: confirmations.length,
    servingsCollected: myClaims.filter((c) => c.status === "collected").reduce((s, c) => s + c.quantity, 0)
  };

  res.json({ foods, confirmations, stats });
});

app.post("/api/donor/foods", requireLogin("donor"), (req, res) => {
  const error = validateFood(req.body);
  if (error) return res.status(400).json({ message: error });

  const data = db.readData();
  const hours = Number(req.body.expiryHours);
  const quantity = Number(req.body.quantity);

  const newFood = {
    id: data.nextFoodId,
    donorId: req.user.id,
    title: req.body.title.trim(),
    foodType: req.body.foodType,
    quantity: quantity,
    remaining: quantity,
    area: req.body.area,
    location: req.body.location.trim(),
    expiryHours: hours,
    expiresAt: db.hoursFromNow(hours),
    notes: (req.body.notes || "").trim(),
    createdAt: new Date().toISOString()
  };
  data.foods.push(newFood);
  data.nextFoodId++;
  logActivity(data, req.user, "Posted food", newFood.title + " (" + quantity + " servings, " + newFood.area + ")");
  db.saveData(data);

  res.json({ message: "Food post added successfully!", food: newFood });
});

app.put("/api/donor/foods/:id", requireLogin("donor"), (req, res) => {
  const error = validateFood(req.body);
  if (error) return res.status(400).json({ message: error });

  const data = db.readData();
  const food = data.foods.find((f) => f.id === Number(req.params.id) && f.donorId === req.user.id);

  if (!food) return res.status(404).json({ message: "Food post not found." });
  if (data.claims.some((c) => c.foodId === food.id)) {
    return res.status(400).json({ message: "Collectors already claimed some of this food, so it can't be edited." });
  }

  const hours = Number(req.body.expiryHours);
  food.title = req.body.title.trim();
  food.foodType = req.body.foodType;
  food.quantity = Number(req.body.quantity);
  food.remaining = food.quantity;
  food.area = req.body.area;
  food.location = req.body.location.trim();
  food.expiryHours = hours;
  food.expiresAt = db.hoursFromNow(hours);
  food.notes = (req.body.notes || "").trim();
  logActivity(data, req.user, "Edited food", food.title + " (" + food.quantity + " servings)");
  db.saveData(data);

  res.json({ message: "Food post updated successfully!", food });
});

app.delete("/api/donor/foods/:id", requireLogin("donor"), (req, res) => {
  const data = db.readData();
  const index = data.foods.findIndex((f) => f.id === Number(req.params.id) && f.donorId === req.user.id);

  if (index === -1) return res.status(404).json({ message: "Food post not found." });
  const foodId = data.foods[index].id;
  if (data.claims.some((c) => c.foodId === foodId && c.status === "claimed")) {
    return res.status(400).json({ message: "Collectors are coming for this food. Confirm their pickups first." });
  }

  logActivity(data, req.user, "Deleted food", data.foods[index].title);
  data.foods.splice(index, 1);
  db.saveData(data);
  res.json({ message: "Food post deleted successfully!" });
});

app.put("/api/donor/claims/:id/confirm", requireLogin("donor"), (req, res) => {
  const data = db.readData();
  const claim = data.claims.find((c) => c.id === Number(req.params.id));
  const food = claim ? data.foods.find((f) => f.id === claim.foodId) : null;

  if (!claim || !food || food.donorId !== req.user.id) {
    return res.status(404).json({ message: "Claim not found." });
  }
  if (claim.status !== "claimed") {
    return res.status(400).json({ message: "This pickup was already confirmed." });
  }

  claim.status = "collected";
  claim.collectedAt = new Date().toISOString();
  const collector = findUser(data, claim.collectorId);
  logActivity(data, req.user, "Confirmed pickup",
    claim.quantity + " servings of " + claim.title + " by " + (collector ? collector.name : "a collector"));
  db.saveData(data);
  res.json({ message: "Pickup confirmed! " + claim.quantity + " servings are marked as collected. Thank you for sharing!" });
});

app.get("/api/foods", requireLogin("collector"), (req, res) => {
  const search = (req.query.search || "").trim().toLowerCase();
  const type = req.query.type || "";
  const area = req.query.area || "";
  const data = db.readData();

  let foods = data.foods.filter((f) => f.remaining > 0 && !isExpired(f) && f.donorId !== req.user.id);

  if (search) {
    foods = foods.filter(
      (f) => f.title.toLowerCase().includes(search) ||
             f.location.toLowerCase().includes(search) ||
             f.area.toLowerCase().includes(search)
    );
  }
  if (type) {
    foods = foods.filter((f) => f.foodType === type);
  }
  if (area) {
    foods = foods.filter((f) => f.area === area);
  }

  const result = foods
    .sort((a, b) => b.id - a.id)
    .map((f) => {
      const donor = findUser(data, f.donorId);
      return {
        ...f,
        donorName: donor ? donor.name : "Unknown",
        donorPhone: donor ? donor.phone : "",
        nearYou: f.area === req.user.area
      };
    });

  res.json({ foods: result, myArea: req.user.area });
});

app.post("/api/foods/:id/claim", requireLogin("collector"), (req, res) => {
  const data = db.readData();
  const food = data.foods.find((f) => f.id === Number(req.params.id));
  const amount = Number(req.body.quantity);

  if (!food) return res.status(404).json({ message: "Food post not found." });
  if (food.donorId === req.user.id) {
    return res.status(400).json({ message: "You can't claim your own food post." });
  }
  if (food.remaining < 1 || isExpired(food)) {
    return res.status(400).json({ message: "Sorry, this food is no longer available." });
  }
  if (!Number.isInteger(amount) || amount < 1) {
    return res.status(400).json({ message: "Please enter how many servings you need (at least 1)." });
  }
  if (amount > food.remaining) {
    return res.status(400).json({ message: "Only " + food.remaining + " servings are left." });
  }

  food.remaining -= amount;

  const existing = data.claims.find(
    (c) => c.foodId === food.id && c.collectorId === req.user.id && c.status === "claimed"
  );
  if (existing) {
    existing.quantity += amount;
  } else {
    data.claims.push({
      id: data.nextClaimId,
      foodId: food.id,
      collectorId: req.user.id,
      quantity: amount,
      status: "claimed",
      title: food.title,
      foodType: food.foodType,
      area: food.area,
      location: food.location,
      claimedAt: new Date().toISOString(),
      collectedAt: null
    });
    data.nextClaimId++;
  }
  logActivity(data, req.user, "Claimed food", amount + " servings of " + food.title);
  db.saveData(data);

  let message = "You claimed " + amount + " servings of " + food.title + ".";
  message += food.remaining > 0 ? " " + food.remaining + " servings are still available for others." : " That was the last of it!";
  res.json({ message: message });
});

app.get("/api/collector/claims", requireLogin("collector"), (req, res) => {
  const data = db.readData();

  const claims = data.claims
    .filter((c) => c.collectorId === req.user.id)
    .sort((a, b) => b.id - a.id)
    .map((c) => {
      const food = data.foods.find((f) => f.id === c.foodId);
      const donor = food ? findUser(data, food.donorId) : null;
      return { ...c, donorName: donor ? donor.name : "Donor", donorPhone: donor ? donor.phone : "" };
    });

  res.json({ claims });
});

app.put("/api/collector/claims/:id/release", requireLogin("collector"), (req, res) => {
  const data = db.readData();
  const index = data.claims.findIndex((c) => c.id === Number(req.params.id) && c.collectorId === req.user.id);

  if (index === -1) return res.status(404).json({ message: "Claim not found." });
  const claim = data.claims[index];
  if (claim.status === "collected") {
    return res.status(400).json({ message: "The donor already confirmed this pickup, so it cannot be released." });
  }

  const food = data.foods.find((f) => f.id === claim.foodId);
  if (food) food.remaining += claim.quantity;
  data.claims.splice(index, 1);
  logActivity(data, req.user, "Released claim", claim.quantity + " servings of " + claim.title);
  db.saveData(data);
  res.json({ message: "Food released. " + claim.quantity + " servings are available for other collectors again." });
});

app.get("/api/public/stats", (req, res) => {
  const data = db.readData();
  const available = data.foods.filter((f) => f.remaining > 0 && !isExpired(f));

  res.json({
    availableFood: available.length,
    servingsWaiting: available.reduce((sum, f) => sum + f.remaining, 0),
    servingsShared: data.claims.filter((c) => c.status === "collected").reduce((sum, c) => sum + c.quantity, 0),
    donors: data.users.filter((u) => u.role === "donor").length,
    collectors: data.users.filter((u) => u.role === "collector").length
  });
});

app.get("/api/public/foods", (req, res) => {
  const data = db.readData();
  const foods = data.foods
    .filter((f) => f.remaining > 0 && !isExpired(f))
    .sort((a, b) => b.id - a.id)
    .slice(0, 2)
    .map((f) => {
      const donor = findUser(data, f.donorId);
      return {
        title: f.title,
        foodType: f.foodType,
        remaining: f.remaining,
        area: f.area,
        location: f.location,
        expiresAt: f.expiresAt,
        donorName: donor ? donor.name : "A donor"
      };
    });
  res.json({ foods });
});

app.get("/api/areas", (req, res) => {
  res.json({ areas: db.AREAS });
});

app.get("/api/admin/overview", requireLogin("admin"), (req, res) => {
  const data = db.readData();
  const people = data.users.filter((u) => u.role !== "admin");
  res.json({
    donors: people.filter((u) => u.role === "donor").length,
    collectors: people.filter((u) => u.role === "collector").length,
    blocked: people.filter((u) => u.blocked).length,
    foodPosts: data.foods.length,
    pickupsWaiting: data.claims.filter((c) => c.status === "claimed").length,
    servingsShared: data.claims.filter((c) => c.status === "collected").reduce((s, c) => s + c.quantity, 0),
    openRequests: data.resetRequests.filter((r) => r.status === "pending").length
  });
});

app.get("/api/admin/requests", requireLogin("admin"), (req, res) => {
  const data = db.readData();
  const requests = data.resetRequests
    .slice()
    .reverse()
    .map((r) => {
      const user = r.userId ? findUser(data, r.userId) : null;
      return {
        id: r.id,
        email: r.email,
        phoneGiven: r.phoneGiven,
        message: r.message,
        status: r.status,
        createdAt: r.createdAt,
        handledAt: r.handledAt,
        codeExpiresAt: r.codeExpiresAt,
        accountFound: !!user,
        userName: user ? user.name : "",
        userRole: user ? user.role : "",
        registeredPhone: user ? user.phone : "",
        phoneMatches: !!user && cleanPhone(user.phone) === cleanPhone(r.phoneGiven)
      };
    });
  res.json({ requests });
});

app.post("/api/admin/requests/:id/code", requireLogin("admin"), (req, res) => {
  const data = db.readData();
  const request = data.resetRequests.find((r) => r.id === Number(req.params.id));
  const code = String(req.body.code || "").trim();

  if (!request) return res.status(404).json({ message: "Request not found." });
  if (!request.userId || !findUser(data, request.userId)) {
    return res.status(400).json({ message: "No account uses this email, so no code can be given." });
  }
  if (request.status !== "pending" && request.status !== "code_given") {
    return res.status(400).json({ message: "This request is already closed." });
  }
  if (!/^\d{6}$/.test(code)) {
    return res.status(400).json({ message: "The code must be exactly 6 digits." });
  }

  request.codeHash = bcrypt.hashSync(code, 10);
  request.codeExpiresAt = new Date(Date.now() + CODE_HOURS * 60 * 60 * 1000).toISOString();
  request.tries = 0;
  request.status = "code_given";
  request.handledAt = new Date().toISOString();
  logActivity(data, req.user, "Gave reset code", "to " + request.email);
  db.saveData(data);

  res.json({
    message: "Code " + code + " saved for " + request.email + ". Tell it to the user by phone. It works for 2 hours.",
    expiresAt: request.codeExpiresAt
  });
});

app.post("/api/admin/requests/:id/reject", requireLogin("admin"), (req, res) => {
  const data = db.readData();
  const request = data.resetRequests.find((r) => r.id === Number(req.params.id));

  if (!request) return res.status(404).json({ message: "Request not found." });
  if (request.status !== "pending" && request.status !== "code_given") {
    return res.status(400).json({ message: "This request is already closed." });
  }
  request.status = "rejected";
  request.codeHash = null;
  request.handledAt = new Date().toISOString();
  logActivity(data, req.user, "Rejected reset request", "for " + request.email);
  db.saveData(data);
  res.json({ message: "Request rejected." });
});

app.get("/api/admin/users", requireLogin("admin"), (req, res) => {
  const data = db.readData();
  const users = data.users
    .filter((u) => u.id !== req.user.id)
    .map((u) => ({
      ...safeUser(u),
      blocked: !!u.blocked,
      createdAt: u.createdAt,
      posts: data.foods.filter((f) => f.donorId === u.id).length,
      claims: data.claims.filter((c) => c.collectorId === u.id).length,
      lastActive: (data.activity.filter((a) => a.userId === u.id).pop() || {}).at || null
    }));
  res.json({ users });
});

function findManagedUser(data, id, admin) {
  const user = findUser(data, Number(id));
  return user && user.id !== admin.id ? user : null;
}

function checkNewUser(data, body) {
  const email = (body.email || "").trim().toLowerCase();
  if (!(body.name || "").trim() || !(body.address || "").trim()) return "Name and address cannot be empty.";
  if (!isValidEmail(email)) return "Please enter a valid email address.";
  if (data.users.some((u) => u.email === email)) return "This email is already registered.";
  if (!isValidPhone(body.phone)) return "Mobile number must be exactly 11 digits starting with 01, e.g. 01711223344.";
  if (!isValidArea(body.area)) return "Please select an area.";
  if (!["donor", "collector", "admin"].includes(body.role)) return "Please select a role.";
  if ((body.password || "").length < 6) return "Password must be at least 6 characters long.";
  return "";
}

app.post("/api/admin/users", requireLogin("admin"), (req, res) => {
  const data = db.readData();
  const error = checkNewUser(data, req.body);
  if (error) return res.status(400).json({ message: error });

  const user = {
    id: data.nextUserId,
    name: req.body.name.trim(),
    email: req.body.email.trim().toLowerCase(),
    phone: cleanPhone(req.body.phone),
    area: req.body.area,
    address: req.body.address.trim(),
    role: req.body.role,
    blocked: false,
    password: bcrypt.hashSync(req.body.password, 10),
    createdAt: new Date().toISOString()
  };
  data.users.push(user);
  data.nextUserId++;
  logActivity(data, req.user, "Added user", user.name + " (" + user.role + ", " + user.email + ")");
  db.saveData(data);
  res.json({ message: user.name + " was added as a " + user.role + "." });
});

app.put("/api/admin/users/:id", requireLogin("admin"), (req, res) => {
  const data = db.readData();
  const user = findManagedUser(data, req.params.id, req.user);
  if (!user) return res.status(404).json({ message: "User not found." });

  const name = (req.body.name || "").trim();
  const email = (req.body.email || "").trim().toLowerCase();
  const phone = cleanPhone(req.body.phone);
  const area = req.body.area;
  const address = (req.body.address || "").trim();
  const role = req.body.role;
  const newPassword = req.body.newPassword || "";

  if (!name || !address) {
    return res.status(400).json({ message: "Name and address cannot be empty." });
  }
  if (!isValidEmail(email)) {
    return res.status(400).json({ message: "Please enter a valid email address." });
  }
  if (data.users.some((u) => u.email === email && u.id !== user.id)) {
    return res.status(400).json({ message: "Another account already uses this email." });
  }
  if (!isValidPhone(phone)) {
    return res.status(400).json({ message: "Mobile number must be exactly 11 digits starting with 01, e.g. 01711223344." });
  }
  if (!isValidArea(area)) {
    return res.status(400).json({ message: "Please select an area." });
  }
  if (!["donor", "collector", "admin"].includes(role)) {
    return res.status(400).json({ message: "Please select a role." });
  }
  if (newPassword && newPassword.length < 6) {
    return res.status(400).json({ message: "New password must be at least 6 characters long." });
  }

  user.name = name;
  user.email = email;
  user.phone = phone;
  user.area = area;
  user.address = address;
  user.role = role;
  user.blocked = req.body.blocked === true;
  if (newPassword) {
    user.password = bcrypt.hashSync(newPassword, 10);
  }
  logActivity(data, req.user, "Edited user", name + " (" + email + ")" + (newPassword ? ", new password set" : ""));
  db.saveData(data);
  res.json({ message: name + " was updated." });
});

app.put("/api/admin/users/:id/block", requireLogin("admin"), (req, res) => {
  const data = db.readData();
  const user = findManagedUser(data, req.params.id, req.user);
  if (!user) return res.status(404).json({ message: "User not found." });

  user.blocked = !user.blocked;
  logActivity(data, req.user, user.blocked ? "Blocked user" : "Unblocked user", user.name + " (" + user.email + ")");
  db.saveData(data);
  res.json({ message: user.name + (user.blocked ? " is blocked and can't log in." : " is unblocked.") });
});

app.put("/api/admin/users/:id/role", requireLogin("admin"), (req, res) => {
  const data = db.readData();
  const user = findManagedUser(data, req.params.id, req.user);
  if (!user) return res.status(404).json({ message: "User not found." });

  if (user.role === "admin") {
    return res.status(400).json({ message: "Use Edit to change an admin's role." });
  }
  user.role = user.role === "donor" ? "collector" : "donor";
  logActivity(data, req.user, "Changed role", user.name + " is now a " + user.role);
  db.saveData(data);
  res.json({ message: user.name + " is now a " + user.role + "." });
});

app.delete("/api/admin/users/:id", requireLogin("admin"), (req, res) => {
  const data = db.readData();
  const user = findManagedUser(data, req.params.id, req.user);
  if (!user) return res.status(404).json({ message: "User not found." });

  for (const claim of data.claims.filter((c) => c.collectorId === user.id && c.status === "claimed")) {
    const food = data.foods.find((f) => f.id === claim.foodId);
    if (food) food.remaining += claim.quantity;
  }
  data.claims = data.claims.filter((c) => !(c.collectorId === user.id && c.status === "claimed"));

  const theirFoodIds = data.foods.filter((f) => f.donorId === user.id).map((f) => f.id);
  data.claims = data.claims.filter((c) => !(theirFoodIds.includes(c.foodId) && c.status === "claimed"));
  data.foods = data.foods.filter((f) => f.donorId !== user.id);

  data.users = data.users.filter((u) => u.id !== user.id);
  logActivity(data, req.user, "Deleted user", user.name + " (" + user.email + ")");
  db.saveData(data);
  res.json({ message: user.name + " was deleted." });
});

app.get("/api/admin/foods", requireLogin("admin"), (req, res) => {
  const data = db.readData();
  const foods = data.foods
    .slice()
    .sort((a, b) => b.id - a.id)
    .map((f) => {
      const donor = findUser(data, f.donorId);
      return {
        ...f,
        status: foodStatus(f, data),
        donorName: donor ? donor.name : "Deleted user",
        waitingClaims: data.claims.filter((c) => c.foodId === f.id && c.status === "claimed").length
      };
    });
  res.json({ foods });
});

app.post("/api/admin/foods", requireLogin("admin"), (req, res) => {
  const error = validateFood(req.body);
  if (error) return res.status(400).json({ message: error });

  const data = db.readData();
  const donor = findUser(data, Number(req.body.donorId));
  if (!donor || donor.role !== "donor") {
    return res.status(400).json({ message: "Please select a donor for this food post." });
  }

  const quantity = Number(req.body.quantity);
  const hours = Number(req.body.expiryHours);
  const food = {
    id: data.nextFoodId,
    donorId: donor.id,
    title: req.body.title.trim(),
    foodType: req.body.foodType,
    quantity: quantity,
    remaining: quantity,
    area: req.body.area,
    location: req.body.location.trim(),
    expiryHours: hours,
    expiresAt: db.hoursFromNow(hours),
    notes: (req.body.notes || "").trim(),
    createdAt: new Date().toISOString()
  };
  data.foods.push(food);
  data.nextFoodId++;
  logActivity(data, req.user, "Added food post", food.title + " (" + quantity + " servings) for " + donor.name);
  db.saveData(data);
  res.json({ message: "Food post \"" + food.title + "\" was added for " + donor.name + "." });
});

app.put("/api/admin/foods/:id", requireLogin("admin"), (req, res) => {
  const error = validateFood(req.body);
  if (error) return res.status(400).json({ message: error });

  const data = db.readData();
  const food = data.foods.find((f) => f.id === Number(req.params.id));
  if (!food) return res.status(404).json({ message: "Food post not found." });

  const quantity = Number(req.body.quantity);
  const claimed = data.claims.filter((c) => c.foodId === food.id).reduce((s, c) => s + c.quantity, 0);
  if (quantity < claimed) {
    return res.status(400).json({ message: "Collectors already took " + claimed + " servings, so the quantity can't be less than " + claimed + "." });
  }

  const hours = Number(req.body.expiryHours);
  food.title = req.body.title.trim();
  food.foodType = req.body.foodType;
  food.quantity = quantity;
  food.remaining = quantity - claimed;
  food.area = req.body.area;
  food.location = req.body.location.trim();
  food.expiryHours = hours;
  food.expiresAt = db.hoursFromNow(hours);
  food.notes = (req.body.notes || "").trim();
  for (const claim of data.claims.filter((c) => c.foodId === food.id)) {
    claim.title = food.title;
    claim.foodType = food.foodType;
    claim.area = food.area;
    claim.location = food.location;
  }
  logActivity(data, req.user, "Edited food post", food.title + " (" + quantity + " servings, " + food.remaining + " left)");
  db.saveData(data);
  res.json({ message: "Food post \"" + food.title + "\" was updated." });
});

app.delete("/api/admin/foods/:id", requireLogin("admin"), (req, res) => {
  const data = db.readData();
  const food = data.foods.find((f) => f.id === Number(req.params.id));
  if (!food) return res.status(404).json({ message: "Food post not found." });

  data.claims = data.claims.filter((c) => !(c.foodId === food.id && c.status === "claimed"));
  data.foods = data.foods.filter((f) => f.id !== food.id);
  logActivity(data, req.user, "Deleted food post", food.title);
  db.saveData(data);
  res.json({ message: "Food post \"" + food.title + "\" was deleted." });
});

app.get("/api/admin/claims", requireLogin("admin"), (req, res) => {
  const data = db.readData();
  const claims = data.claims
    .slice()
    .sort((a, b) => b.id - a.id)
    .map((c) => {
      const food = data.foods.find((f) => f.id === c.foodId);
      const donor = food ? findUser(data, food.donorId) : null;
      const collector = findUser(data, c.collectorId);
      return {
        ...c,
        donorName: donor ? donor.name : "Deleted",
        collectorName: collector ? collector.name : "Deleted user"
      };
    });
  res.json({ claims });
});

app.post("/api/admin/claims", requireLogin("admin"), (req, res) => {
  const data = db.readData();
  const food = data.foods.find((f) => f.id === Number(req.body.foodId));
  const collector = findUser(data, Number(req.body.collectorId));
  const amount = Number(req.body.quantity);

  if (!food) return res.status(400).json({ message: "Please select a food post." });
  if (!collector || collector.role !== "collector") {
    return res.status(400).json({ message: "Please select a collector." });
  }
  if (food.donorId === collector.id) {
    return res.status(400).json({ message: "A collector can't claim their own food post." });
  }
  if (!Number.isInteger(amount) || amount < 1) {
    return res.status(400).json({ message: "Quantity must be at least 1." });
  }
  if (amount > food.remaining) {
    return res.status(400).json({ message: "Only " + food.remaining + " servings are left." });
  }

  food.remaining -= amount;
  const existing = data.claims.find(
    (c) => c.foodId === food.id && c.collectorId === collector.id && c.status === "claimed"
  );
  if (existing) {
    existing.quantity += amount;
  } else {
    data.claims.push({
      id: data.nextClaimId,
      foodId: food.id,
      collectorId: collector.id,
      quantity: amount,
      status: "claimed",
      title: food.title,
      foodType: food.foodType,
      area: food.area,
      location: food.location,
      claimedAt: new Date().toISOString(),
      collectedAt: null
    });
    data.nextClaimId++;
  }
  logActivity(data, req.user, "Added claim", amount + " servings of " + food.title + " for " + collector.name);
  db.saveData(data);
  res.json({ message: amount + " servings of " + food.title + " were claimed for " + collector.name + "." });
});

app.put("/api/admin/claims/:id/confirm", requireLogin("admin"), (req, res) => {
  const data = db.readData();
  const claim = data.claims.find((c) => c.id === Number(req.params.id));
  if (!claim) return res.status(404).json({ message: "Claim not found." });
  if (claim.status !== "claimed") {
    return res.status(400).json({ message: "This pickup was already confirmed." });
  }

  claim.status = "collected";
  claim.collectedAt = new Date().toISOString();
  logActivity(data, req.user, "Confirmed pickup", claim.quantity + " servings of " + claim.title);
  db.saveData(data);
  res.json({ message: "Pickup confirmed: " + claim.quantity + " servings of " + claim.title + "." });
});

app.delete("/api/admin/claims/:id", requireLogin("admin"), (req, res) => {
  const data = db.readData();
  const claim = data.claims.find((c) => c.id === Number(req.params.id));
  if (!claim) return res.status(404).json({ message: "Claim not found." });

  const food = data.foods.find((f) => f.id === claim.foodId);
  if (claim.status === "claimed" && food) {
    food.remaining += claim.quantity;
  }
  data.claims = data.claims.filter((c) => c.id !== claim.id);
  logActivity(data, req.user, "Cancelled claim", claim.quantity + " servings of " + claim.title);
  db.saveData(data);
  res.json({ message: "Claim cancelled: " + claim.quantity + " servings of " + claim.title + "." });
});

app.get("/api/admin/activity", requireLogin("admin"), (req, res) => {
  const userId = Number(req.query.userId) || 0;
  const search = (req.query.search || "").trim().toLowerCase();
  const data = db.readData();

  let list = data.activity.slice().reverse();
  if (userId) list = list.filter((a) => a.userId === userId);
  if (search) {
    list = list.filter((a) =>
      (a.action + " " + a.details + " " + a.userName).toLowerCase().includes(search));
  }
  res.json({ activity: list.slice(0, 300) });
});

app.post("/api/test/reset", (req, res) => {
  db.resetData();
  req.session.destroy(() => {
    res.json({ message: "Database reset to demo data." });
  });
});

app.use("/api", (req, res) => {
  res.status(404).json({ message: "API route not found." });
});

app.use((err, req, res, next) => {
  console.error(err.message);
  res.status(err.status || 500).json({ message: "Something went wrong on the server." });
});

app.listen(PORT, () => {
  db.readData();
  const url = "http://localhost:" + PORT;
  console.log("=========================================");
  console.log(" FoodBridge server is running!");
  console.log(" Open: " + url);
  console.log(" (Ctrl + Click a link, or type it in Chrome/Edge)");
  console.log(" Keep this terminal open. Press Ctrl + C to stop.");
  console.log(" Admin login: admin@foodbridge.com");
  console.log("=========================================");
});
