from helpers import *


def test(driver):
    fill_signup_form(driver, "Arpita Saha Arpa", "arpita.donor@gmail.com", "01711223344", "donor", "Kuril", "House 5, Road 2", "arpita123", "arpita123")
    message = wait_for_message(driver)
    return "successfully" in message, message


TEST_CASE = ("TC01", "Verify signup with valid information as Donor",
             "Name: Arpita Saha Arpa, Email: arpita.donor@gmail.com, Mobile: 01711223344, Role: Donor, Area: Kuril, Address: House 5, Road 2, Password: arpita123", test)


def run():
    return run_test_module("Sign Up", [TEST_CASE], logout_before_each=True)


if __name__ == "__main__":
    run()
