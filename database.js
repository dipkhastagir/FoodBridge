const fs = require("fs");
const path = require("path");
const bcrypt = require("bcryptjs");

const DATA_FOLDER = path.join(__dirname, "data");
const DB_FILE = path.join(DATA_FOLDER, "db.json");

const DEMO_PASSWORDS = {
  admin: "Admin@FoodBridge26",
  donor: "Donor@FoodBridge26",
  collector: "Collector@FoodBridge26",
  collector2: "Smile@FoodBridge26"
};

const AREAS = [
  "Badda", "Banani", "Baridhara", "Bashundhara", "Dhanmondi", "Farmgate", "Gulshan",
  "Jatrabari", "Khilgaon", "Kuril", "Lalbagh", "Malibagh", "Mirpur", "Mohakhali",
  "Mohammadpur", "Motijheel", "Old Dhaka", "Rampura", "Shyamoli", "Tejgaon", "Uttara", "Wari",
  "Outside Dhaka"
];

function hoursFromNow(hours) {
  return new Date(Date.now() + hours * 60 * 60 * 1000).toISOString();
}

function makeFood(id, title, foodType, quantity, remaining, area, location, hours, notes) {
  return {
    id: id,
    donorId: 1,
    title: title,
    foodType: foodType,
    quantity: quantity,
    remaining: remaining,
    area: area,
    location: location,
    expiryHours: hours,
    expiresAt: hoursFromNow(hours),
    notes: notes,
    createdAt: new Date().toISOString()
  };
}

function createSeedData() {
  const now = new Date().toISOString();

  return {
    nextUserId: 5,
    nextFoodId: 6,
    nextClaimId: 3,
    nextRequestId: 1,
    nextActivityId: 4,
    users: [
      {
        id: 1,
        name: "Dhaka Food Corner",
        email: "donor@foodbridge.com",
        phone: "01711000001",
        area: "Banani",
        address: "House 12, Road 11, Banani",
        role: "donor",
        blocked: false,
        password: bcrypt.hashSync(DEMO_PASSWORDS.donor, 10),
        createdAt: now
      },
      {
        id: 2,
        name: "Hope Volunteers",
        email: "collector@foodbridge.com",
        phone: "01811000002",
        area: "Mirpur",
        address: "Section 10, Block C, Mirpur",
        role: "collector",
        blocked: false,
        password: bcrypt.hashSync(DEMO_PASSWORDS.collector, 10),
        createdAt: now
      },
      {
        id: 3,
        name: "Smile Foundation",
        email: "smile@foodbridge.com",
        phone: "01911000003",
        area: "Uttara",
        address: "Sector 7, Road 3, Uttara",
        role: "collector",
        blocked: false,
        password: bcrypt.hashSync(DEMO_PASSWORDS.collector2, 10),
        createdAt: now
      },
      {
        id: 4,
        name: "FoodBridge Admin",
        email: "admin@foodbridge.com",
        phone: "01511000004",
        area: "Tejgaon",
        address: "FoodBridge Office, Tejgaon",
        role: "admin",
        blocked: false,
        password: bcrypt.hashSync(DEMO_PASSWORDS.admin, 10),
        createdAt: now
      }
    ],
    foods: [
      makeFood(1, "Chicken Biryani", "Cooked Meal", 20, 20, "Banani", "House 12, Road 11", 5, "Packed in food boxes, still warm."),
      makeFood(2, "Fresh Bread Loaves", "Bakery", 15, 15, "Gulshan", "Gulshan 1 Circle, shop 4", 12, "Baked this morning."),
      makeFood(3, "Mixed Fruits Basket", "Fruits & Vegetables", 10, 10, "Dhanmondi", "Road 27, House 5", 24, "Bananas, apples and oranges."),
      makeFood(4, "Vegetable Khichuri", "Cooked Meal", 25, 0, "Mirpur", "Section 10 bus stand", 4, "Vegetarian."),
      makeFood(5, "Egg Fried Rice", "Cooked Meal", 12, 0, "Banani", "House 12, Road 11", 3, "")
    ],
    claims: [
      { id: 1, foodId: 4, collectorId: 2, quantity: 25, status: "claimed",
        title: "Vegetable Khichuri", foodType: "Cooked Meal", area: "Mirpur", location: "Section 10 bus stand",
        claimedAt: now, collectedAt: null },
      { id: 2, foodId: 5, collectorId: 2, quantity: 12, status: "collected",
        title: "Egg Fried Rice", foodType: "Cooked Meal", area: "Banani", location: "House 12, Road 11",
        claimedAt: now, collectedAt: now }
    ],
    resetRequests: [],
    activity: [
      { id: 1, at: now, userId: 1, userName: "Dhaka Food Corner", role: "donor",
        action: "Posted food", details: "Vegetable Khichuri (25 servings, Mirpur)" },
      { id: 2, at: now, userId: 2, userName: "Hope Volunteers", role: "collector",
        action: "Claimed food", details: "25 servings of Vegetable Khichuri" },
      { id: 3, at: now, userId: 1, userName: "Dhaka Food Corner", role: "donor",
        action: "Confirmed pickup", details: "12 servings of Egg Fried Rice by Hope Volunteers" }
    ]
  };
}

function saveData(data) {
  if (!fs.existsSync(DATA_FOLDER)) {
    fs.mkdirSync(DATA_FOLDER, { recursive: true });
  }
  fs.writeFileSync(DB_FILE, JSON.stringify(data, null, 2));
}

function readData() {
  if (!fs.existsSync(DB_FILE)) {
    const seed = createSeedData();
    saveData(seed);
    return seed;
  }

  try {
    const data = JSON.parse(fs.readFileSync(DB_FILE, "utf-8"));
    if (!Array.isArray(data.activity) || !Array.isArray(data.resetRequests)) {
      console.log("db.json was from an older version, so it was reset with demo data.");
      return resetData();
    }
    return data;
  } catch (error) {
    console.log("db.json was broken, so it was reset with demo data.");
    return resetData();
  }
}

function resetData() {
  const seed = createSeedData();
  saveData(seed);
  return seed;
}

module.exports = { readData, saveData, resetData, hoursFromNow, DEMO_PASSWORDS, AREAS };
