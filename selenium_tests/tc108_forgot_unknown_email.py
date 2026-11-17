from helpers import *


def test(driver):
    answer = send_request(driver, "nobody@gmail.com", "01711999888", "")
    logout(driver)
    open_admin_dashboard(driver)
    row = find(driver, "request-1").text
    no_code_box = not element_exists(driver, "code-input-1")
    passed = "sent to the admin" in answer and "No account uses this email" in row and no_code_box
    return passed, "User saw: " + answer + " | Admin sees: No account uses this email, code box shown: " + str(not no_code_box)


TEST_CASE = ("TC108", "Verify a request for an unknown email looks normal but the admin cannot give a code",
             "Email: nobody@gmail.com, Mobile: 01711999888", test)


def run():
    return run_test_module("Forgot Password", [TEST_CASE], logout_before_each=True)


if __name__ == "__main__":
    run()
