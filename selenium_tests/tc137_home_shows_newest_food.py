from helpers import *


def test(driver):
    login(driver, DONOR_EMAIL, DONOR_PASSWORD)
    open_donor_dashboard(driver)
    fill_food_form(driver, "Mango Juice", "Drinks & Dairy", "8", "6", "Banani Road 11", "")
    wait_for_message(driver)
    logout(driver)
    open_page(driver, "index.html")
    wait_until(driver, lambda d: "Mango Juice" in d.find_element(By.ID, "heroTickets").text)
    return True, "Home page ticket shows: Mango Juice"


TEST_CASE = ("TC137", "Verify the home page shows the newest food post",
             "Donor posts Mango Juice, then open the home page", test)


def run():
    return run_test_module("Home Page", [TEST_CASE], logout_before_each=True)


if __name__ == "__main__":
    run()
