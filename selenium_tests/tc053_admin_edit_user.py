from helpers import *


def test(driver):
    open_admin_tab(driver, "tab-users", "usersBody")
    click(driver, "edit-user-3")
    type_text(driver, "editUserPhone", "01999888777")
    choose_option(driver, "editUserArea", "Badda")
    type_text(driver, "editUserAddress", "Road 5, Badda")
    click(driver, "saveUserBtn")
    message = wait_for_message(driver)
    wait_until(driver, lambda d: "01999888777" in d.find_element(By.ID, "user-3").text)
    row = find(driver, "user-3").text
    passed = "was updated" in message and "01999888777" in row and "Badda" in row
    return passed, message + " | Row now shows: 01999888777, Badda: " + str("Badda" in row)


TEST_CASE = ("TC53", "Verify admin can edit a user's details",
             "User: Smile Foundation, Mobile: 01999888777, Area: Badda, Address: Road 5, Badda", test)


def run():
    return run_test_module("Admin", [TEST_CASE], logout_before_each=True)


if __name__ == "__main__":
    run()
