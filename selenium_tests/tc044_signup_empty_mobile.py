from helpers import *


def test(driver):
    fill_signup_form(driver, "Kuril Food Corner", "kuril.food@gmail.com", "", "donor", "Kuril", "Road 3", "kuril123", "kuril123")
    validation = get_validation_message(driver, "phone")
    still_on_page = "signup.html" in driver.current_url
    return validation != "" and still_on_page, "Browser message: " + validation


TEST_CASE = ("TC44", "Verify signup with empty Mobile number field",
             "Mobile: (blank), other fields valid", test)


def run():
    return run_test_module("Contact & Location", [TEST_CASE], logout_before_each=True)


if __name__ == "__main__":
    run()
