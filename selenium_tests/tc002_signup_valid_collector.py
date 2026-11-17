from helpers import *


def test(driver):
    fill_signup_form(driver, "Rahim Uddin", "rahim.collector@gmail.com", "01811223344", "collector", "Mohammadpur", "Block B, Road 4", "rahim123", "rahim123")
    message = wait_for_message(driver)
    return "successfully" in message, message


TEST_CASE = ("TC02", "Verify signup with valid information as Collector",
             "Name: Rahim Uddin, Email: rahim.collector@gmail.com, Mobile: 01811223344, Role: Collector, Area: Mohammadpur, Address: Block B, Road 4, Password: rahim123", test)


def run():
    return run_test_module("Sign Up", [TEST_CASE], logout_before_each=True)


if __name__ == "__main__":
    run()
