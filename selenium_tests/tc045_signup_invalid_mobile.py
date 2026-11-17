from helpers import *


def test(driver):
    fill_signup_form(driver, "Kuril Food Corner", "kuril.food@gmail.com", "0181145129", "donor", "Kuril", "Road 3", "kuril123", "kuril123")
    validation = get_validation_message(driver, "phone")
    return validation != "", "Browser message: " + validation


TEST_CASE = ("TC45", "Verify signup with an invalid mobile number",
             "Mobile: 0181145129 (10 digits)", test)


def run():
    return run_test_module("Contact & Location", [TEST_CASE], logout_before_each=True)


if __name__ == "__main__":
    run()
