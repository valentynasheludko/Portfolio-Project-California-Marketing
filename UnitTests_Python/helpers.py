# Helpers file for project Ca-Marketing (Personal Address book)
import time
import random
import requests
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from faker import Faker

faker_class = Faker()

# Set main variables
# URL - home page
main_url = "https://qasvus.wixsite.com/ca-marketing"
# User's E-mail
user_email = "..."  # type your user's E-mail for account
# User's password
user_pass = "..."  # type your user's password for account

# MOST OFTEN USED X-PATHs

# User's account button for opening drop-down menu
btn_users_account = "//div[@class='_3gZId'][contains(.,'Hello')]"

# Item 'My Addresses' in drop-down menu
item_My_addresses = "//span[contains(text(),'My Addresses')]"

# Button "Add New Address"
btn_Add_New_Address = "//div[@class='_10o0_ _26mkp hidden-mobile']" \
                      "//button[@class='_172js'][contains(text(),'Add New Address')]"

# Button 'Add Address'
btn_Add_Address = "//*[@class='col-sm-6']//*[contains(text(),'Add Address')]"

# Check box 'Set as default'
checkbox_default = "//span[@class='_udoS wixSdkShowFocusOnSibling']"

# Button 'Update Address'
btn_Update_Address = "//*[@class='col-sm-6']//*[contains(text(),'Update Address')]"

# Message 'Please enter first name'
err_message = "firstName-field-error"


# MOST OFTEN USED FUNCTIONS

# Set random delay
def delay():
    time.sleep(random.randint(1, 3))


# Check API response code
def check_API_code(driver):
    code = requests.get(main_url).status_code
    if code == 200:
        print("Url has ", requests.get(main_url).status_code, " as status Code")
    else:
        print("API response code is not 200")


# Verify Pages Title
def assert_title(driver, title):
    wait = WebDriverWait(driver, 10)
    wait.until(EC.title_is(title))
    assert title in driver.title
    print("Page has", driver.title + " as Page title")
    # Screenshot of the page
    driver.get_screenshot_as_file(f"Page {title}.png")
    if not title in driver.title:
        raise Exception(f"Page {title} has wrong Title!")


# Check that an elements are present and visible on the Home page
def home_page_elements(driver, text1, text2):
    try:
        wait = WebDriverWait(driver, 5)
        wait.until(EC.visibility_of_element_located((By.XPATH, "//span[contains(text(), text1)]")))
        print(f"Text {text1} is visible!")
    except TimeoutException:
        print("Loading text too much time!")
        driver.get_screenshot_as_file("Loading text too much time.png")
    element = driver.find_element(By.LINK_TEXT, text2)
    if text2 in driver.page_source:
        print(f"LinkText {text2} has attribute " + element.get_attribute("href"))
    else:
        print(f"Page don't have LinkText = {text2}")
    if not text2 in driver.page_source:
        raise Exception("Link Text is wrong!")


# Log In in exist account
def login(driver):
    # Set wait until button 'Login' will be clickable
    wait = WebDriverWait(driver, 10)
    wait.until(EC.element_to_be_clickable((By.ID, "defaultAvatar-comp-k00e6z1w")))
    # Click on button 'Login'
    driver.find_element(By.ID, "defaultAvatar-comp-k00e6z1w").click()
    delay()
    # Switch from 'Sign Up' to 'Log In'
    wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Log In')]")))
    driver.find_element(By.XPATH, "//button[contains(text(), 'Log In')]").click()
    # Set wait until button 'Log In with Email' will be visible and click on it
    wait.until(EC.visibility_of_element_located((By.XPATH, "//div[@id='switchToEmailLink_SM_ROOT_COMP18']/button")))
    driver.find_element(By.XPATH, "//div[@id='switchToEmailLink_SM_ROOT_COMP18']/button").click()
    # Clear fields and Type user's email and password
    driver.find_element(By.ID, "input_input_emailInput_SM_ROOT_COMP18").click()
    driver.find_element(By.ID, "input_input_emailInput_SM_ROOT_COMP18").clear()
    driver.find_element(By.ID, "input_input_emailInput_SM_ROOT_COMP18").send_keys(user_email)
    driver.find_element(By.ID, "input_input_passwordInput_SM_ROOT_COMP18").click()
    driver.find_element(By.ID, "input_input_passwordInput_SM_ROOT_COMP18").clear()
    driver.find_element(By.ID, "input_input_passwordInput_SM_ROOT_COMP18").send_keys(user_pass)
    driver.find_element(By.XPATH, "//div[@id='okButton_SM_ROOT_COMP18']/button").click()


# Scroll to list 'My Addresses'
def scroll_to_my_addresses(driver):
    listMyAddresses = driver.find_element(By.XPATH, "//h1[@class='_3jEzm'][contains(text(),'My Addresses')]")
    driver.execute_script("arguments[0].scrollIntoView(true)", listMyAddresses)


# Scroll bottom in frame 3
def scroll_to_bottom_frame3(driver):
    frame3 = driver.find_element(By.XPATH, "//*[@class='_3Cqnq'][@data-hook='main-scroll']")
    driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", frame3)


# Check, print and delete all addresses in the list
def check_and_delete_sav_addresses(driver):
    try:
        wait = WebDriverWait(driver, 5)
        wait.until(EC.visibility_of_all_elements_located((By.XPATH, "//address[contains(text(),' ')]")))
        save_Addresses = driver.find_elements(By.XPATH, "//address[contains(text(),' ')]")
        for address in save_Addresses:
            text = address.text
            print(text)  # print address
            print("------------------------------------------------")
            # Scroll to list 'My Addresses'
            scroll_to_my_addresses(driver)
            # delete address
            delay()
            driver.find_element(By.XPATH, "//*[contains(text(),' ')]//following::button[3]").click()
            delay()
            driver.find_element(By.XPATH, "//*[contains(text(),' ')]//following::span[2]/div/button").click()
            delay()
    except TimeoutException:
        print("List 'My Addresses' is empty, deletion not required")


# Enter random values of Address by Faker (First name manually for negative tests)
def address_create(driver, firstname):
    driver.find_element(By.ID, "firstName-field").click()
    driver.find_element(By.ID, "firstName-field").send_keys(firstname)
    driver.find_element(By.ID, "lastName-field").click()
    driver.find_element(By.ID, "lastName-field").send_keys(faker_class.last_name())
    driver.find_element(By.ID, "company-field").click()
    driver.find_element(By.ID, "company-field").send_keys(faker_class.company())
    driver.find_element(By.ID, "addressLine1-field").click()
    driver.find_element(By.ID, "addressLine1-field").send_keys(faker_class.street_address())
    driver.find_element(By.ID, "addressLine2-field").click()
    driver.find_element(By.ID, "addressLine2-field").send_keys(faker_class.random_int())
    driver.find_element(By.ID, "city-field").click()
    driver.find_element(By.ID, "city-field").send_keys(faker_class.city())
    delay()
    # Country is created automatically
    driver.find_element(By.ID, "subdivision-field").click()
    driver.find_element(By.ID, "subdivision-field").send_keys(faker_class.state())
    driver.find_element(By.ID, "zipCode-field").click()
    driver.find_element(By.ID, "zipCode-field").send_keys(faker_class.postcode())
    driver.find_element(By.ID, "phone-field").click()
    driver.find_element(By.ID, "phone-field").send_keys("0123456789")


# Check button 'Add Address' working for negative tests
def check_btn_AddAddress(driver, exception):
    try:
        wait = WebDriverWait(driver, 10)
        wait.until(EC.visibility_of_element_located((By.ID, err_message)))
        print("Button 'Add Address' doesn't work.\n"
              "Message", driver.find_element(By.ID, err_message).text + " appears.")
        # Click on button 'Cancel'
        driver.find_element(By.XPATH, "//*[@class='col-sm-6']//*[contains(text(),'Cancel')]").click()
    except exception:
        print("Button 'Add Address' works.")


# Check that the Address with incorrect First name is not created and delete it if created for negative tests
def check_createAddr_incorrect_FirstName(driver, address_xpath, test_number, browser):
    try:
        wait = WebDriverWait(driver, 5)
        wait.until(EC.invisibility_of_element_located((By.XPATH, address_xpath)))
        print("----------------------------------------------\n"
              "Address with incorrect First name is NOT ADDED\n"
              f"TEST {test_number} PASS")
        driver.get_screenshot_as_file(f"Address_incorrectFN{test_number}_not_added-{browser}.png")
    except TimeoutException:
        print("-------------------------------------------------------\n"
              "Address with incorrect First name is created:")
        print(driver.find_element(By.XPATH, address_xpath).text)
        driver.get_screenshot_as_file(f"Address_incorrectFN{test_number}_added-{browser}.png")
        print("-----------------------------\n"
              "It's a bug, debugging needed!\n"
              f"TEST {test_number} FAIL")
        # Delete address if it created
        try:
            wait = WebDriverWait(driver, 5)
            wait.until(EC.visibility_of_element_located((By.XPATH, "//address[contains(text(),' ')]")))
            # Find and click on button 'Remove' of the Address, then click on button 'Yes'
            driver.find_element(By.XPATH, "//*[contains(text(),' ')]//following::button[3]").click()
            delay()
            driver.find_element(By.XPATH, "//*[contains(text(),' ')]//following::span[2]/div/button").click()
            delay()
            print("------------------\nAddress is deleted")
        except TimeoutException:
            print("------------------------\nNo Addresses in the list")
        raise Exception(f"Address with incorrect First name is ADDED. TEST {test_number} FAIL")
