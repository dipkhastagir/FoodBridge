from helpers import *


def test(driver):
    open_donor_dashboard(driver)
    click(driver, "edit-2")
    title_while_editing = find(driver, "formTitle").text
    click(driver, "cancelEditBtn")
    title_after = find(driver, "formTitle").text
    edit_id = find(driver, "editId").get_attribute("value")
    passed = title_while_editing == "Edit food post" and title_after == "Post surplus food" and edit_id == ""
    return passed, "While editing: " + title_while_editing + " | After cancel: " + title_after


TEST_CASE = ("TC94", "Verify Cancel edit puts the form back to posting new food",
             "Click Edit on Fresh Bread Loaves, then Cancel edit", test)


def run():
    return run_test_module("Donor Dashboard", [TEST_CASE], login_as=(DONOR_EMAIL, DONOR_PASSWORD))


if __name__ == "__main__":
    run()
