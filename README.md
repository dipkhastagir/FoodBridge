# FoodBridge – Surplus Food Sharing Platform (SQAT Project)

FoodBridge connects people who have leftover food with people who can deliver it to those in need.

- **Donor** (restaurant, bakery, household): posts surplus food, confirms pickups, edits/deletes posts.
- **Collector** (NGO, volunteer group): searches food, claims **only the servings they need**, releases claims.
- **Admin**: answers forgot-password requests and has full control over donors, collectors, food posts and the activity log.

### Main rules
| Feature | How it works |
|---|---|
| **Partial claim** | A collector types how many servings they need. The rest stays available for other collectors. |
| **Pickup confirmation** | Claims show on the donor's dashboard under *Waiting for your confirmation*. |
| **Release (re-donate)** | Before the donor confirms, a collector can release a claim. The servings go back to the post. |
| **Lock** | After the donor clicks **Confirm pickup**, the claim is locked and can't be released. |
| **Role switch** | *Switch to Collector* / *Switch to Donor* button on each dashboard. Posts and claims are kept. You can never claim your own food. |
| **Mobile number** | Exactly 11 digits starting with 01 (Bangladesh), e.g. 01711223344. The box accepts digits only and stops at 11; the server checks it again. |
| **Location** | Mobile number, area and address are required at sign up. Collectors filter food by area and see *Near you* badges; donors see the collector's area and address. Both get **Open in Maps** links. |
| **Forgot password** | The user sends a request (email + mobile number + message) to the **admin**. The admin checks the number, calls the user, **types a 6-digit code** and tells it to the user. The code works for **2 hours** with 5 tries. The user enters it at *Forgot password? → Already have a code? Enter it here* and sets a new password. No email is needed. |
| **Admin control** | Full access: reset requests, **add users** (donor, collector or admin), **add food posts** for any donor, **add claims** for any collector, **edit any user** (name, email, mobile, area, address, role, status, new password), block/unblock, delete users, **edit any food post** (including quantity), delete posts, **confirm or cancel any claim**, and a full **activity log**. |
| **Back buttons** | On the log in, sign up, forgot password and code pages. |

Tech: HTML + CSS + JavaScript (frontend), Node.js + Express (backend), JSON file database (`data/db.json`), Python Selenium (testing).

---

## 1. Install these first (one time)

1. **Node.js (LTS)** – https://nodejs.org (Windows Installer .msi)
2. **Python 3** – https://www.python.org (tick "Add Python to PATH")
3. **Google Chrome**
4. **VS Code**

## 2. Run the website (Terminal 1)

Open the folder that contains `package.json` in VS Code (**File → Open Folder**), open a terminal and run:

```
npm install
npm run reset
npm start
```

Open **http://localhost:3000** in Chrome or Edge (type it in the **top address bar**).
**Keep this terminal open** – the website stops if you close it.

> Never open the HTML files by double-clicking them (address bar shows `File C:/...`). That can't reach the server.

### Demo accounts

The demo accounts (admin, donor, collectors) are listed in **`demo.txt`**. They are not shown on the website.

### "Change your password – found in a data breach" popup in Chrome
That popup comes from **Chrome**, not from FoodBridge. Chrome shows it whenever you type a password that is on public
leak lists (like `donor123` or `12345678`). The demo passwords above are unique, so they don't trigger it.
If you type a simple password while trying the site and want the popup gone:
Chrome → **Settings → Autofill and passwords → Google Password Manager → Settings** → turn off
**"Warn you if passwords are exposed in a data breach"**. The Selenium tests already turn it off automatically.

## 3. Forgot password (handled by the admin)

1. User: **Log in → Forgot password?** Enter email, mobile number and an optional message → **Send request to admin**.
2. Admin: log in as admin → **Reset requests** tab. The row shows whose account it is and whether the
   mobile number **matches the account**. Call the user, type a **6-digit code** in the box, click **Save code**
   and tell the user the code. It works for **2 hours**.
3. User: **Forgot password? → Already have a code? Enter it here**. Type the email and the code → choose a new password.

The admin can also **Reject** a request. Requests for emails with no account are shown in red and can't get a code.

## 4. Run the Selenium tests (Terminal 2)

Every test case has its **own file**: `tc001_signup_valid_donor.py` to `tc140_profile_dashboard_link.py` (**140 test cases**).
TC01 to TC60 test every feature. TC61 to TC140 add the missing features and **boundary tests**
(the values just inside and just outside every limit, such as quantity 1 / 1000 / 1001, fresh time 1 / 48 / 0 / 49 hours,
passwords of 5 and 6 characters, mobile prefixes 012 / 013 / 019, claims of 0 / 1 / all / one more than left,
4 and 5 wrong reset codes).

First time only:
```
cd selenium_tests
python -m venv venv
venv\Scripts\Activate.ps1
pip install selenium
```
(Command Prompt: `venv\Scripts\activate`. If `python` is not found, use `py`.)

**Run one test case:**
```
python tc001_signup_valid_donor.py
python tc083_donor_quantity_1000.py
```

**Run all 140 in order:**
```
python run_all_tests.py
```
It ends with `TOTAL: 140 test cases PASSED: 140 FAILED: 0` and saves `test_results.csv`.
A browser screenshot of each test is saved in `screenshots/TC01.png ... TC140.png`. The full run takes about 15 to 20 minutes.

Each file resets the demo data before it runs, so every test can be run alone, in any order, as many times as you like.

| Section | Feature tests | Extra and boundary tests |
|---|---|---|
| Sign Up | TC01 to TC07 | TC61 to TC72 |
| Login | TC08 to TC13 | TC73 to TC74 |
| Donor Dashboard | TC14 to TC20 | TC82 to TC94 |
| Collector Dashboard | TC21 to TC26 | TC95 to TC103 |
| Profile & Security | TC27 to TC30 | TC75 to TC81 |
| Pickup Confirmation & Home Page | TC31 to TC34 | TC104, TC136 to TC137 |
| Partial Claim | TC35 to TC36 |  |
| Role Switch | TC37 to TC38 | TC105 to TC106 |
| Forgot Password | TC39 to TC41 | TC107 to TC118 |
| Navigation | TC42 to TC43 | TC138 to TC140 |
| Contact & Location | TC44 to TC47 |  |
| Admin | TC48 to TC60 | TC119 to TC135 |

Change `STEP_DELAY` in `helpers.py` (e.g. `1.5`) to watch the browser more slowly.

## 5. Project structure

```
FoodBridge/
├── server.js          ← backend: all API routes
├── database.js        ← reads/writes data/db.json + demo data
├── reset-db.js        ← "npm run reset"
├── demo.txt           ← demo accounts (admin, donor, collectors)
├── public/
│   ├── index.html                 home page
│   ├── signup.html, login.html
│   ├── forgot-password.html       step 1: request to admin
│   ├── reset-password.html        step 2-3: admin's code + new password
│   ├── admin-dashboard.html       admin control room
│   ├── donor-dashboard.html, collector-dashboard.html, profile.html
│   ├── css/style.css
│   └── js/  api.js home.js signup.js login.js forgot.js reset.js donor.js collector.js profile.js admin.js
└── selenium_tests/    helpers.py + 140 test files (tc001_... to tc140_...) + run_all_tests.py
```

## 6. API list

| Method | URL | Who |
|---|---|---|
| POST | /api/signup, /api/login, /api/logout | anyone |
| POST | /api/forgot-password, /api/verify-reset-code, /api/reset-password | anyone |
| GET | /api/forgot-password/status?email= | anyone (code page status) |
| GET | /api/me | logged in |
| PUT | /api/profile, /api/change-password, /api/switch-role | logged in |
| GET/POST | /api/donor/foods | donor |
| PUT/DELETE | /api/donor/foods/:id | donor (edit only if nobody claimed it) |
| PUT | /api/donor/claims/:id/confirm | donor (locks the claim) |
| GET | /api/foods?search=&type=&area= | collector |
| POST | /api/foods/:id/claim `{quantity}` | collector |
| GET | /api/collector/claims | collector |
| PUT | /api/collector/claims/:id/release | collector (only before donor confirms) |
| GET | /api/public/stats, /api/public/foods | anyone (home page) |
| GET | /api/areas | anyone (area list) |
| GET | /api/admin/overview, /requests, /users, /foods, /claims, /activity | admin |
| POST | /api/admin/requests/:id/code `{code}`, /api/admin/requests/:id/reject | admin |
| POST | /api/admin/users, /api/admin/foods, /api/admin/claims (add new) | admin |
| PUT | /api/admin/users/:id, /api/admin/users/:id/block, /api/admin/users/:id/role | admin |
| PUT | /api/admin/foods/:id, /api/admin/claims/:id/confirm | admin |
| DELETE | /api/admin/users/:id, /api/admin/foods/:id, /api/admin/claims/:id | admin |
| POST | /api/test/reset | testing only |

## 7. Common problems

| Problem | Fix |
|---|---|
| "Cannot connect to the server" | Open `http://localhost:3000`, not the HTML file (`File C:/...`) |
| Edge searches Bing instead of opening the site | Type `http://localhost:3000` in the **top address bar** (Ctrl + L) |
| `npm.ps1 cannot be loaded because running scripts is disabled` | Run once: `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` (or use `npm.cmd install`) |
| `npm` not recognized right after installing Node.js | Restart the PC |
| `EADDRINUSE :3000` | Server already running. Stop it: `Stop-Process -Id (Get-NetTCPConnection -LocalPort 3000).OwningProcess -Force` |
| Demo logins fail after updating the project | Run `npm run reset` (old `db.json` has a different format) |
| Login page shows an email you didn't type | Fixed: the fields stay empty until you click them. If Chrome still offers a saved login, that is Chrome's suggestion list; you can remove saved logins in Chrome → Settings → Passwords |
| "The admin has not given you a code yet" | The admin must type a code and click **Save code** on your request first |
| "Your account is blocked" | The admin blocked the account; the admin can unblock it in Donors & collectors |
| Project inside OneDrive is slow | Move it to e.g. `C:\Projects\FoodBridge` |
