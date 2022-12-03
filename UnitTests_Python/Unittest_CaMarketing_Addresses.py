import unittest
import time
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, NoSuchElementException, NoSuchWindowException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
import helpers as H


class Chrome_AddressesTests(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()

    def test1_ChromePos_CheckDeleteAddr(self):
        driver = self.driver
        driver.get(H.main_url)  # open URL - home page
        # driver.set_window_size(1200, 800)  # Set another Window Size
        print("***********************************************************\n"
              "TEST 1 - SHOW ALL SAVED ADDRESSES AND DELETE IF ARE PRESENT\n"
              "***********************************************************")
        H.check_API_code(driver)  # Check API response code
        H.assert_title(driver, "Home | California Marcketing")  # Verify Homepage Title
        wait = WebDriverWait(driver, 10)  # Create variable for wait.until
        # Check that an elements are present and visible on the Home page
        H.home_page_elements(driver, "LET CALIFORNIA MARKETING GROW YOUR BUSINECS", "CALIFORNIA MARCKETING",)
        H.delay()
        H.login(driver)  # Log In in exist account
        # Wait and click on user's account button for opening drop-down menu
        wait.until(EC.element_to_be_clickable((By.XPATH, H.btn_users_account)))
        driver.find_element(By.XPATH, H.btn_users_account).click()
        wait.until(EC.element_to_be_clickable((By.XPATH, H.item_My_addresses)))
        driver.find_element(By.XPATH, H.item_My_addresses).click()  # Select item 'My Addresses' in drop-down menu
        time.sleep(3)
        H.assert_title(driver, "My Addresses")  # Verify page 'My Addresses' Title
        driver.switch_to.frame(0)  # Switch to Frame (For Chrome and Edge index=0, for FireFox index=1)
        time.sleep(3)
        H.scroll_to_my_addresses(driver)  # Scroll to list 'My Addresses'
        print("Saved addresses in the list:\n------------------------------------------------")
        H.check_and_delete_sav_addresses(driver)  # Check, print and delete all addresses in the list
        # Check that all addresses is deleted from list or List 'My Addresses' was empty" and make screenshot
        try:
            wait.until(EC.visibility_of_element_located((By.XPATH, "//div[@class='_3oKYs']"
                                                                   "[contains(text(), 'saved any addresses yet.')]")))
            print("---------------------------------------------------------\n"
                  "All addresses is removed or List 'My Addresses' was empty\nTEST1 - PASS")
            driver.get_screenshot_as_file("All addresses is deleted-Chrome.png")
        except TimeoutException:
            print("-----------------------------------\nAddresses is not completely removed\nTEST 1 - FAIL")
            raise Exception("-----------------------------------\nAddresses is not completely removed\nTEST 1 - FAIL")
        driver.close()

    def test2_ChromePos_CreateAddr1(self):
        driver = self.driver
        driver.get(H.main_url)  # open URL - home page
        # driver.set_window_size(1200, 800)  # Set another Window Size
        print("***************************************\n"
              "TEST 2 - CREATING THE FIRST NEW ADDRESS\n"
              "***************************************")
        H.check_API_code(driver)  # Check API response code
        H.assert_title(driver, "Home | California Marcketing")  # Verify Homepage Title
        wait = WebDriverWait(driver, 5)  # Create variable for wait.until
        # Check that an elements are present and visible on the Home page
        H.home_page_elements(driver, "LET CALIFORNIA MARKETING GROW YOUR BUSINECS", "CALIFORNIA MARCKETING")
        H.delay()
        H.login(driver)  # Log In in exist account
        # Wait and click on user's account button for opening drop-down menu
        wait.until(EC.element_to_be_clickable((By.XPATH, H.btn_users_account)))
        driver.find_element(By.XPATH, H.btn_users_account).click()
        wait.until(EC.element_to_be_clickable((By.XPATH, H.item_My_addresses)))
        driver.find_element(By.XPATH, H.item_My_addresses).click()  # Select item 'My Addresses' in drop-down menu
        time.sleep(5)
        H.assert_title(driver, "My Addresses")  # Verify page 'My Addresses' Title
        driver.switch_to.frame(0)  # Switch to Frame (For Chrome and Edge index=0, for FireFox index=1)
        time.sleep(3)
        driver.find_element(By.XPATH, H.btn_Add_New_Address).click()  # Find button "Add new address" and click on it
        driver.switch_to.default_content()  # Go to parent Frame
        driver.switch_to.frame(3)  # Switch to another Frame
        H.delay()
        H.address_create(driver, H.faker_class.first_name())  # Enter random values of first new Address by Faker
        H.scroll_to_bottom_frame3(driver)  # Scroll bottom in frame 3
        driver.find_element(By.XPATH, H.btn_Add_Address).click()  # Click on button 'Add Address'
        time.sleep(3)
        driver.switch_to.frame(0)  # Go to Frame (for Chrome and Edge index=0, for FireFox index=1)
        time.sleep(3)
        H.scroll_to_my_addresses(driver)  # Scroll to list 'My Addresses'
        # Check that First New address is created
        try:
            wait.until(EC.visibility_of_element_located((By.XPATH, "//address[@class='m-wda']"
                                                                   "[@data-hook='formatted-address']")))
            print("First new address is created:")
            print(driver.find_element(By.XPATH, "//address[@class='m-wda'][@data-hook='formatted-address']").text)
            driver.get_screenshot_as_file("First new address-Chrome.png")
        except TimeoutException:
            print("First new address is not in list")
        if not "You haven't saved any addresses yet." in driver.page_source:
            print("New address with correct values is added.\nTEST 2 PASS")
        else:
            print("You haven't saved any addresses yet.\nTEST 2 FAIL")
            raise Exception("You haven't saved any addresses yet.\n TEST 2 FAIL")
        driver.close()

    def test3_ChromePos_CreateAddr2Default(self):
        driver = self.driver
        driver.get(H.main_url)  # open URL - home page
        # driver.set_window_size(1200, 800)  # Set another Window Size
        print("***********************************************************\n"
              "TEST 3 - CREATING THE SECOND NEW ADDRESS AND SET IT DEFAULT\n"
              "***********************************************************")
        H.check_API_code(driver)  # Check API response code
        H.assert_title(driver, "Home | California Marcketing")  # Verify Homepage Title
        wait = WebDriverWait(driver, 5)  # Create variable for wait.until
        # Check that an elements are present and visible on the Home page
        H.home_page_elements(driver, "LET CALIFORNIA MARKETING GROW YOUR BUSINECS", "CALIFORNIA MARCKETING")
        H.delay()
        H.login(driver)  # Log In in exist account
        # Wait and click on user's account button for opening drop-down menu
        wait.until(EC.element_to_be_clickable((By.XPATH, H.btn_users_account)))
        driver.find_element(By.XPATH, H.btn_users_account).click()
        wait.until(EC.element_to_be_clickable((By.XPATH, H.item_My_addresses)))
        driver.find_element(By.XPATH, H.item_My_addresses).click()  # Select item 'My Addresses' in drop-down menu
        time.sleep(5)
        H.assert_title(driver, "My Addresses")  # Verify page 'My Addresses' Title
        driver.switch_to.frame(0)  # Switch to Frame (For Chrome and Edge index=0, for FireFox index=1)
        time.sleep(3)
        driver.find_element(By.XPATH, H.btn_Add_New_Address).click()  # Find button "Add new address" and click on it
        driver.switch_to.default_content()  # Go to parent Frame
        driver.switch_to.frame(3)  # Switch to another Frame
        H.delay()
        # Enter second new Address manually
        driver.find_element(By.ID, "firstName-field").click()
        driver.find_element(By.ID, "firstName-field").send_keys("Wolfgang Amadeus")
        driver.find_element(By.ID, "lastName-field").click()
        driver.find_element(By.ID, "lastName-field").send_keys("Mozart")
        driver.find_element(By.ID, "company-field").click()
        driver.find_element(By.ID, "company-field").send_keys("Requiem")
        driver.find_element(By.ID, "addressLine1-field").click()
        driver.find_element(By.ID, "addressLine1-field").send_keys("Glocknerstrasse 63")
        driver.find_element(By.ID, "addressLine2-field").click()
        driver.find_element(By.ID, "addressLine2-field").send_keys("63")
        driver.find_element(By.ID, "city-field").click()
        driver.find_element(By.ID, "city-field").send_keys("Hochgreit")
        H.delay()
        # Enter country and subdivision manually from drop-down list
        H.scroll_to_bottom_frame3(driver)  # Scroll to bottom in frame3
        # Click on country-field, find and choose country from list
        driver.find_element(By.ID, "country-field").click()
        driver.findElement(By.XPATH, "//*[contains(text(),'Austria')]")
        time.sleep(1)
        driver.find_element(By.XPATH, "//*[contains(text(),'Austria')]").click()
        # Click on subdivision-field, find and choose subdivision from list
        driver.find_element(By.ID, "subdivision-field").click()
        driver.findElement(By.XPATH, "//*[contains(text(),'Wien')]")
        time.sleep(1)
        driver.find_element(By.XPATH, "//*[contains(text(),'Wien')]").click()
        driver.find_element(By.ID, "zipCode-field").click()
        driver.find_element(By.ID, "zipCode-field").send_keys("8045")
        driver.find_element(By.ID, "phone-field").click()
        driver.find_element(By.ID, "phone-field").send_keys("0688 515 10 71")
        H.scroll_to_bottom_frame3(driver)  # Scroll to current frame's bottom
        driver.find_element(By.XPATH, H.checkbox_default).click()  # Set second new address as default
        driver.find_element(By.XPATH, H.btn_Add_Address).click()  # Click on button 'Add Address'
        time.sleep(3)
        driver.switch_to.frame(0)  # Go to Frame (for Chrome and Edge index=0, for FireFox index=1)
        time.sleep(3)
        H.scroll_to_my_addresses(driver)  # Scroll to list 'My Addresses'
        # Check that second New address is created and make it screenshot
        try:
            wait.until(EC.visibility_of_element_located((By.XPATH, "//*[contains(text(),'Wolfgang Amadeus Mozart')]")))
            print("Second new address is created:")
            print(driver.find_element(By.XPATH, "//*[contains(text(),'Wolfgang Amadeus Mozart')]").text)
            driver.get_screenshot_as_file("Second address as default-Chrome.png")
        except TimeoutException:
            print("Second new address is not in list")
        # Wait for row with needed values loading
        wait.until(EC.visibility_of_all_elements_located((By.XPATH, "//*[contains(text(),'Wolfgang Amadeus "
                                                                    "Mozart')]//following::div[1]")))
        # Check that second New address set as default
        try:
            default = driver.find_element(By.XPATH, "//*[contains(text(),'Wolfgang Amadeus Mozart')]"
                                                    "//following::div[4]/span")
            print("Second new address has attribute: ", default.get_attribute("data-hook"))
            print("Second new address is set as", default.text, "\nTEST 3 PASS")
        except NoSuchElementException:
            print("Second new address is not set as default\nTEST 3 FAIL")
            raise Exception("Second new address is not set as default\nTEST 3 FAIL")
        driver.close()

    def test4_ChromePos_UpdateAddr2(self):
        driver = self.driver
        driver.get(H.main_url)  # open URL - home page
        # driver.set_window_size(1200, 800)  # Set another Window Size
        print("****************************************\n"
              "TEST 4 - UPDATING THE SECOND NEW ADDRESS\n"
              "****************************************")
        H.check_API_code(driver)  # Check API response code
        H.assert_title(driver, "Home | California Marcketing")  # Verify Homepage Title
        wait = WebDriverWait(driver, 5)  # Create variable for wait.until
        # Check that an elements are present and visible on the Home page
        H.home_page_elements(driver, "LET CALIFORNIA MARKETING GROW YOUR BUSINECS", "CALIFORNIA MARCKETING")
        H.delay()
        H.login(driver)  # Log In in exist account
        # Wait and click on user's account button for opening drop-down menu
        wait.until(EC.element_to_be_clickable((By.XPATH, H.btn_users_account)))
        driver.find_element(By.XPATH, H.btn_users_account).click()
        wait.until(EC.element_to_be_clickable((By.XPATH, H.item_My_addresses)))
        driver.find_element(By.XPATH, H.item_My_addresses).click()  # Select item 'My Addresses' in drop-down menu
        time.sleep(5)
        H.assert_title(driver, "My Addresses")  # Verify page 'My Addresses' Title
        driver.switch_to.frame(0)  # Switch to Frame (For Chrome and Edge index=0, for FireFox index=1)
        H.scroll_to_my_addresses(driver)  # Scroll to list 'My Addresses'
        time.sleep(3)
        # Find button 'Edit' of the second new address and click on it
        driver.find_element(By.XPATH, "//*[contains(text(),'Wolfgang Amadeus Mozart')]"
                                      "//following::button[1]").click()
        driver.switch_to.default_content()  # Go to parent Frame
        driver.switch_to.frame(3)  # Switch to another Frame
        time.sleep(3)
        # Update second new Address manually
        driver.find_element(By.ID, "firstName-field").click()
        driver.find_element(By.ID, "firstName-field").send_keys(Keys.CONTROL + "a", Keys.DELETE)
        driver.find_element(By.ID, "firstName-field").send_keys("Antonio")
        driver.find_element(By.ID, "lastName-field").click()
        driver.find_element(By.ID, "lastName-field").send_keys(Keys.CONTROL + "a", Keys.DELETE)
        driver.find_element(By.ID, "lastName-field").send_keys("Salieri")
        driver.find_element(By.ID, "company-field").click()
        driver.find_element(By.ID, "company-field").send_keys(Keys.CONTROL + "a", Keys.DELETE)
        driver.find_element(By.ID, "company-field").send_keys("Der Rauchfangkehrer ")
        driver.find_element(By.ID, "addressLine1-field").click()
        driver.find_element(By.ID, "addressLine1-field").send_keys(Keys.CONTROL + "a", Keys.DELETE)
        driver.find_element(By.ID, "addressLine1-field").send_keys("Leopoldstrabe 77")
        driver.find_element(By.ID, "addressLine2-field").click()
        driver.find_element(By.ID, "addressLine2-field").send_keys(Keys.CONTROL + "a", Keys.DELETE)
        driver.find_element(By.ID, "addressLine2-field").send_keys("55")
        driver.find_element(By.ID, "city-field").click()
        driver.find_element(By.ID, "city-field").send_keys(Keys.CONTROL + "a", Keys.DELETE)
        driver.find_element(By.ID, "city-field").send_keys("Berlin Dahlem")
        H.delay()
        # Enter country and subdivision manually from drop-down list
        H.scroll_to_bottom_frame3(driver)  # Scroll to current frame's bottom
        # Click on country-field, find and choose country from list
        driver.find_element(By.ID, "country-field").click()
        driver.findElement(By.XPATH, "//*[contains(text(),'Germany')]")
        time.sleep(1)
        driver.find_element(By.XPATH, "//*[contains(text(),'Germany')]").click()
        # Click on subdivision-field, find and choose subdivision from list
        driver.find_element(By.ID, "subdivision-field").click()
        driver.findElement(By.XPATH, "//*[contains(text(),'Berlin')]")
        time.sleep(1)
        driver.find_element(By.XPATH, "//*[contains(text(),'Berlin')]").click()
        driver.find_element(By.ID, "zipCode-field").click()
        driver.find_element(By.ID, "zipCode-field").send_keys(Keys.CONTROL + "a", Keys.DELETE)
        driver.find_element(By.ID, "zipCode-field").send_keys("14195")
        driver.find_element(By.ID, "phone-field").click()
        driver.find_element(By.ID, "phone-field").send_keys(Keys.CONTROL + "a", Keys.DELETE)
        driver.find_element(By.ID, "phone-field").send_keys("030 19 40 32")
        H.scroll_to_bottom_frame3(driver)  # Scroll to current frame's bottom
        driver.find_element(By.XPATH, H.btn_Update_Address).click()  # Click on button 'Update Address'
        time.sleep(3)
        driver.switch_to.frame(0)  # Go to Frame (for Chrome and Edge index=0, for FireFox index=1)
        time.sleep(3)
        H.scroll_to_my_addresses(driver)  # Scroll to list 'My Addresses'
        # Check that second New address is updated and make it screenshot
        try:
            wait.until(EC.visibility_of_element_located((By.XPATH, "//*[contains(text(),'Antonio Salieri')]")))
            print("Second new address is updated:")
            print(driver.find_element(By.XPATH, "//*[contains(text(),'Antonio Salieri')]").text)
            print("Changing values in second new address is available\nTEST 4 PASS")
            driver.get_screenshot_as_file("Second address updated-Chrome.png")
        except TimeoutException:
            print("Second new address is NOT updated\nTEST 4 FAIL")
            raise Exception("Second new address is NOT updated\nTEST 4 FAIL")
        driver.close()

    def test5_ChromePos_DeleteAddr2(self):
        driver = self.driver
        driver.get(H.main_url)  # open URL - home page
        # driver.set_window_size(1200, 800)  # Set another Window Size
        print("****************************************\n"
              "TEST 5 - DELETING THE SECOND NEW ADDRESS\n"
              "****************************************")
        H.check_API_code(driver)  # Check API response code
        H.assert_title(driver, "Home | California Marcketing")  # Verify Homepage Title
        wait = WebDriverWait(driver, 5)  # Create variable for wait.until
        # Check that an elements are present and visible on the Home page
        H.home_page_elements(driver, "LET CALIFORNIA MARKETING GROW YOUR BUSINECS", "CALIFORNIA MARCKETING")
        H.delay()
        H.login(driver)  # Log In in exist account
        # Wait and click on user's account button for opening drop-down menu
        wait.until(EC.element_to_be_clickable((By.XPATH, H.btn_users_account)))
        driver.find_element(By.XPATH, H.btn_users_account).click()
        wait.until(EC.element_to_be_clickable((By.XPATH, H.item_My_addresses)))
        driver.find_element(By.XPATH, H.item_My_addresses).click()  # Select item 'My Addresses' in drop-down menu
        time.sleep(5)
        H.assert_title(driver, "My Addresses")  # Verify page 'My Addresses' Title
        driver.switch_to.frame(0)  # Switch to Frame (For Chrome and Edge index=0, for FireFox index=1)
        H.scroll_to_my_addresses(driver)  # Scroll to list 'My Addresses'
        time.sleep(3)
        # Find and click on button 'Remove' of the new second address, then click on button 'Yes'
        driver.find_element(By.XPATH, "//*[contains(text(),'Antonio Salieri')]//following::button[2]").click()
        H.delay()
        driver.find_element(By.XPATH, "//*[contains(text(),'Antonio Salieri')]//following::span[2]/div/button").click()
        time.sleep(3)
        H.scroll_to_my_addresses(driver)  # Scroll to list 'My Addresses'
        # Check that second New address is deleted and make screenshot
        try:
            wait.until(EC.visibility_of_element_located((By.XPATH, "//*[contains(text(),'Antonio Salieri')]")))
            print("Second new address is NOT deleted")
        except TimeoutException:
            print("Second new address is deleted")
            driver.get_screenshot_as_file("Second address deleted-Chrome.png")
        if not "Antonio Salieri" in driver.page_source:
            print("Address removing completed successfully\nTEST 5 PASS")
        else:
            print("Address removing is NOT completed\nTEST 5 FAIL")
            raise Exception("Address removing is NOT completed\nTEST 5 FAIL")
        print("**********************************************************\n"
              "CHECK SAVED ADDRESSES IN THE LIST AND DELETE ALL ADDRESSES\n"
              "**********************************************************")
        H.check_and_delete_sav_addresses(driver)
        try:
            wait = WebDriverWait(driver, 5)  # Create variable for wait.until
            wait.until(EC.visibility_of_element_located((By.XPATH, "//div[@class='_3oKYs']"
                                                                   "[contains(text(), 'saved any addresses yet.')]")))
            print("---------------------------------------------------------\n"
                  "All addresses is removed or List 'My Addresses' was empty")
            driver.get_screenshot_as_file("All addresses is deleted-Chrome.png")
        except TimeoutException:
            print("-----------------------------------\nAddresses is not completely removed")
        driver.close()

    def test6_ChromeNeg_Fname_numbers(self):
        driver = self.driver
        driver.get(H.main_url)  # open URL - home page
        # driver.set_window_size(1200, 800)  # Set another Window Size
        print("*****************************************************************\n"
              "TEST 6 - CREATING THE ADDRESS WITH INCORRECT FIRST NAME (NUMBERS)\n"
              "*****************************************************************")
        H.check_API_code(driver)  # Check API response code
        H.assert_title(driver, "Home | California Marcketing")  # Verify Homepage Title
        wait = WebDriverWait(driver, 5)  # Create variable for wait.until
        # Check that an elements are present and visible on the Home page
        H.home_page_elements(driver, "LET CALIFORNIA MARKETING GROW YOUR BUSINECS", "CALIFORNIA MARCKETING")
        H.delay()
        H.login(driver)  # Log In in exist account
        # Wait and click on user's account button for opening drop-down menu
        wait.until(EC.element_to_be_clickable((By.XPATH, H.btn_users_account)))
        driver.find_element(By.XPATH, H.btn_users_account).click()
        wait.until(EC.element_to_be_clickable((By.XPATH, H.item_My_addresses)))
        driver.find_element(By.XPATH, H.item_My_addresses).click()  # Select item 'My Addresses' in drop-down menu
        time.sleep(5)
        H.assert_title(driver, "My Addresses")  # Verify page 'My Addresses' Title
        driver.switch_to.frame(0)  # Switch to Frame (For Chrome and Edge index=0, for FireFox index=1)
        time.sleep(3)
        driver.find_element(By.XPATH, H.btn_Add_New_Address).click()  # Find button "Add new address" and click on it
        driver.switch_to.default_content()  # Go to parent Frame
        driver.switch_to.frame(3)  # Switch to another Frame
        H.delay()
        H.address_create(driver, "0123456789")  # Enter First name manually, other values of Address random by Faker
        H.scroll_to_bottom_frame3(driver)  # Scroll bottom in frame 3
        driver.find_element(By.XPATH, H.btn_Add_Address).click()  # Click on button 'Add Address'
        H.check_btn_AddAddress(driver, TimeoutException)  # Check button 'Add Address' working
        time.sleep(3)
        driver.switch_to.frame(0)  # Go to Frame (for Chrome and Edge index=0, for FireFox index=1)
        time.sleep(3)
        H.scroll_to_my_addresses(driver)  # Scroll to list 'My Addresses'
        # Check that the Address with incorrect First name is not created and delete it if created
        H.check_createAddr_incorrect_FirstName(driver, "//address[contains(text(),'0123456789')]", "6", "Chrome")
        driver.close()

    def test7_ChromeNeg_Fname_spec_char(self):
        driver = self.driver
        driver.get(H.main_url)  # open URL - home page
        # driver.set_window_size(1200, 800)  # Set another Window Size
        print("****************************************************************************\n"
              "TEST 7 - CREATING THE ADDRESS WITH INCORRECT FIRST NAME (SPECIAL CHARACTERS)\n"
              "****************************************************************************")
        H.check_API_code(driver)  # Check API response code
        H.assert_title(driver, "Home | California Marcketing")  # Verify Homepage Title
        wait = WebDriverWait(driver, 5)  # Create variable for wait.until
        # Check that an elements are present and visible on the Home page
        H.home_page_elements(driver, "LET CALIFORNIA MARKETING GROW YOUR BUSINECS", "CALIFORNIA MARCKETING")
        H.delay()
        H.login(driver)  # Log In in exist account
        # Wait and click on user's account button for opening drop-down menu
        wait.until(EC.element_to_be_clickable((By.XPATH, H.btn_users_account)))
        driver.find_element(By.XPATH, H.btn_users_account).click()
        wait.until(EC.element_to_be_clickable((By.XPATH, H.item_My_addresses)))
        driver.find_element(By.XPATH, H.item_My_addresses).click()  # Select item 'My Addresses' in drop-down menu
        time.sleep(5)
        H.assert_title(driver, "My Addresses")  # Verify page 'My Addresses' Title
        driver.switch_to.frame(0)  # Switch to Frame (For Chrome and Edge index=0, for FireFox index=1)
        time.sleep(3)
        driver.find_element(By.XPATH, H.btn_Add_New_Address).click()  # Find button "Add new address" and click on it
        driver.switch_to.default_content()  # Go to parent Frame
        driver.switch_to.frame(3)  # Switch to another Frame
        H.delay()
        H.address_create(driver, "!@#$%^&*()")  # Enter First name manually, other values of Address random by Faker
        H.scroll_to_bottom_frame3(driver)  # Scroll bottom in frame 3
        driver.find_element(By.XPATH, H.btn_Add_Address).click()  # Click on button 'Add Address'
        H.check_btn_AddAddress(driver, TimeoutException)  # Check button 'Add Address' working
        time.sleep(3)
        driver.switch_to.frame(0)  # Go to Frame (for Chrome and Edge index=0, for FireFox index=1)
        time.sleep(3)
        H.scroll_to_my_addresses(driver)  # Scroll to list 'My Addresses'
        # Check that the Address with incorrect First name is not created and delete it if created
        H.check_createAddr_incorrect_FirstName(driver, "//address[contains(text(),'!@#$%^&*()')]", "7", "Chrome")
        driver.close()

    def test8_ChromeNeg_Fname_empty(self):
        driver = self.driver
        driver.get(H.main_url)  # open URL - home page
        # driver.set_window_size(1200, 800)  # Set another Window Size
        print("***************************************************************\n"
              "TEST 8 - CREATING THE ADDRESS WITH INCORRECT FIRST NAME (EMPTY)\n"
              "***************************************************************")
        H.check_API_code(driver)  # Check API response code
        H.assert_title(driver, "Home | California Marcketing")  # Verify Homepage Title
        wait = WebDriverWait(driver, 5)  # Create variable for wait.until
        # Check that an elements are present and visible on the Home page
        H.home_page_elements(driver, "LET CALIFORNIA MARKETING GROW YOUR BUSINECS", "CALIFORNIA MARCKETING")
        H.delay()
        H.login(driver)  # Log In in exist account
        # Wait and click on user's account button for opening drop-down menu
        wait.until(EC.element_to_be_clickable((By.XPATH, H.btn_users_account)))
        driver.find_element(By.XPATH, H.btn_users_account).click()
        wait.until(EC.element_to_be_clickable((By.XPATH, H.item_My_addresses)))
        driver.find_element(By.XPATH, H.item_My_addresses).click()  # Select item 'My Addresses' in drop-down menu
        time.sleep(5)
        H.assert_title(driver, "My Addresses")  # Verify page 'My Addresses' Title
        driver.switch_to.frame(0)  # Switch to Frame (For Chrome and Edge index=0, for FireFox index=1)
        time.sleep(3)
        driver.find_element(By.XPATH, H.btn_Add_New_Address).click()  # Find button "Add new address" and click on it
        driver.switch_to.default_content()  # Go to parent Frame
        driver.switch_to.frame(3)  # Switch to another Frame
        H.delay()
        H.address_create(driver, "")  # Enter First name manually, other values of Address random by Faker
        H.scroll_to_bottom_frame3(driver)  # Scroll bottom in frame 3
        driver.find_element(By.XPATH, H.btn_Add_Address).click()  # Click on button 'Add Address'
        H.check_btn_AddAddress(driver, TimeoutException)  # Check button 'Add Address' working
        time.sleep(3)
        driver.switch_to.frame(0)  # Go to Frame (for Chrome and Edge index=0, for FireFox index=1)
        time.sleep(3)
        H.scroll_to_my_addresses(driver)  # Scroll to list 'My Addresses'
        # Check that the Address with incorrect First name is not created and delete it if created
        H.check_createAddr_incorrect_FirstName(driver, "//address[contains(text(),'')]", "8", "Chrome")
        driver.close()

    def test9_ChromeNeg_Fname_lot_of_letter(self):
        driver = self.driver
        driver.get(H.main_url)  # open URL - home page
        # driver.set_window_size(1200, 800)  # Set another Window Size
        print("*****************************************************************************\n"
              "TEST 9 - CREATING THE ADDRESS WITH INCORRECT FIRST NAME (A LOT OF LETTER 'a')\n"
              "*****************************************************************************")
        H.check_API_code(driver)  # Check API response code
        H.assert_title(driver, "Home | California Marcketing")  # Verify Homepage Title
        wait = WebDriverWait(driver, 5)  # Create variable for wait.until
        # Check that an elements are present and visible on the Home page
        H.home_page_elements(driver, "LET CALIFORNIA MARKETING GROW YOUR BUSINECS", "CALIFORNIA MARCKETING")
        H.delay()
        H.login(driver)  # Log In in exist account
        # Wait and click on user's account button for opening drop-down menu
        wait.until(EC.element_to_be_clickable((By.XPATH, H.btn_users_account)))
        driver.find_element(By.XPATH, H.btn_users_account).click()
        wait.until(EC.element_to_be_clickable((By.XPATH, H.item_My_addresses)))
        driver.find_element(By.XPATH, H.item_My_addresses).click()  # Select item 'My Addresses' in drop-down menu
        time.sleep(5)
        H.assert_title(driver, "My Addresses")  # Verify page 'My Addresses' Title
        driver.switch_to.frame(0)  # Switch to Frame (For Chrome and Edge index=0, for FireFox index=1)
        time.sleep(3)
        driver.find_element(By.XPATH, H.btn_Add_New_Address).click()  # Find button "Add new address" and click on it
        driver.switch_to.default_content()  # Go to parent Frame
        driver.switch_to.frame(3)  # Switch to another Frame
        H.delay()
        # Enter First name manually, other values of Address random by Faker
        H.address_create(driver, "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
        H.scroll_to_bottom_frame3(driver)  # Scroll bottom in frame 3
        driver.find_element(By.XPATH, H.btn_Add_Address).click()  # Click on button 'Add Address'
        H.check_btn_AddAddress(driver, TimeoutException)  # Check button 'Add Address' working
        time.sleep(3)
        driver.switch_to.frame(0)  # Go to Frame (for Chrome and Edge index=0, for FireFox index=1)
        time.sleep(3)
        H.scroll_to_my_addresses(driver)  # Scroll to list 'My Addresses'
        # Check that the Address with incorrect First name is not created and delete it if created
        H.check_createAddr_incorrect_FirstName(driver, "//address[contains(text(),"
                                                       "'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')]", "9",
                                                       "Chrome")
        driver.close()

    def tearDown(self):
        self.driver.quit()  # Close the browser.


class Edge_AddressesTests(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Edge()
        self.driver.maximize_window()

    def test1_EdgePos_CheckDeleteAddr(self):
        driver = self.driver
        driver.get(H.main_url)  # open URL - home page
        # driver.set_window_size(1200, 800)  # Set another Window Size
        print("***********************************************************\n"
              "TEST 1 - SHOW ALL SAVED ADDRESSES AND DELETE IF ARE PRESENT\n"
              "***********************************************************")
        H.check_API_code(driver)  # Check API response code
        H.assert_title(driver, "Home | California Marcketing")  # Verify Homepage Title
        wait = WebDriverWait(driver, 10)  # Create variable for wait.until
        # Check that an elements are present and visible on the Home page
        H.home_page_elements(driver, "LET CALIFORNIA MARKETING GROW YOUR BUSINECS", "CALIFORNIA MARCKETING")
        H.delay()
        H.login(driver)  # Log In in exist account
        # Wait and click on user's account button for opening drop-down menu
        wait.until(EC.element_to_be_clickable((By.XPATH, H.btn_users_account)))
        driver.find_element(By.XPATH, H.btn_users_account).click()
        wait.until(EC.element_to_be_clickable((By.XPATH, H.item_My_addresses)))
        driver.find_element(By.XPATH, H.item_My_addresses).click()  # Select item 'My Addresses' in drop-down menu
        time.sleep(3)
        H.assert_title(driver, "My Addresses")  # Verify page 'My Addresses' Title
        driver.switch_to.frame(0)  # Switch to Frame (For Chrome and Edge index=0, for FireFox index=1)
        time.sleep(3)
        H.scroll_to_my_addresses(driver)  # Scroll to list 'My Addresses'
        print("Saved addresses in the list:\n------------------------------------------------")
        H.check_and_delete_sav_addresses(driver)  # Check, print and delete all addresses in the list
        # Check that all addresses is deleted from list or List 'My Addresses' was empty" and make screenshot
        try:
            wait.until(EC.visibility_of_element_located((By.XPATH, "//div[@class='_3oKYs']"
                                                                   "[contains(text(), 'saved any addresses yet.')]")))
            print("---------------------------------------------------------\n"
                  "All addresses is removed or List 'My Addresses' was empty\nTEST1 - PASS")
            driver.get_screenshot_as_file("All addresses is deleted-Edge.png")
        except TimeoutException:
            print("-----------------------------------\nAddresses is not completely removed\nTEST 1 - FAIL")
            raise Exception("-----------------------------------\nAddresses is not completely removed\nTEST 1 - FAIL")
        driver.close()

    def test2_EdgePos_CreateAddr1(self):
        driver = self.driver
        driver.get(H.main_url)  # open URL - home page
        # driver.set_window_size(1200, 800)  # Set another Window Size
        print("***************************************\n"
              "TEST 2 - CREATING THE FIRST NEW ADDRESS\n"
              "***************************************")
        H.check_API_code(driver)  # Check API response code
        H.assert_title(driver, "Home | California Marcketing")  # Verify Homepage Title
        wait = WebDriverWait(driver, 5)  # Create variable for wait.until
        # Check that an elements are present and visible on the Home page
        H.home_page_elements(driver, "LET CALIFORNIA MARKETING GROW YOUR BUSINECS", "CALIFORNIA MARCKETING")
        H.delay()
        H.login(driver)  # Log In in exist account
        # Wait and click on user's account button for opening drop-down menu
        wait.until(EC.element_to_be_clickable((By.XPATH, H.btn_users_account)))
        driver.find_element(By.XPATH, H.btn_users_account).click()
        wait.until(EC.element_to_be_clickable((By.XPATH, H.item_My_addresses)))
        driver.find_element(By.XPATH, H.item_My_addresses).click()  # Select item 'My Addresses' in drop-down menu
        time.sleep(5)
        H.assert_title(driver, "My Addresses")  # Verify page 'My Addresses' Title
        driver.switch_to.frame(0)  # Switch to Frame (For Chrome and Edge index=0, for FireFox index=1)
        time.sleep(3)
        driver.find_element(By.XPATH, H.btn_Add_New_Address).click()  # Find button "Add new address" and click on it
        driver.switch_to.default_content()  # Go to parent Frame
        driver.switch_to.frame(3)  # Switch to another Frame
        H.delay()
        H.address_create(driver, H.faker_class.first_name())  # Enter random values of first new Address by Faker
        H.scroll_to_bottom_frame3(driver)  # Scroll bottom in frame 3
        driver.find_element(By.XPATH, H.btn_Add_Address).click()  # Click on button 'Add Address'
        time.sleep(3)
        driver.switch_to.frame(0)  # Go to Frame (for Chrome and Edge index=0, for FireFox index=1)
        time.sleep(3)
        H.scroll_to_my_addresses(driver)  # Scroll to list 'My Addresses'
        # Check that First New address is created
        try:
            wait.until(EC.visibility_of_element_located((By.XPATH, "//address[@class='m-wda']"
                                                                   "[@data-hook='formatted-address']")))
            print("First new address is created:")
            print(driver.find_element(By.XPATH, "//address[@class='m-wda'][@data-hook='formatted-address']").text)
            driver.get_screenshot_as_file("First new address-Edge.png")
        except TimeoutException:
            print("First new address is not in list")
        if not "You haven't saved any addresses yet." in driver.page_source:
            print("New address with correct values is added.\nTEST 2 PASS")
        else:
            print("You haven't saved any addresses yet.\nTEST 2 FAIL")
            raise Exception("You haven't saved any addresses yet.\n TEST 2 FAIL")
        driver.close()

    def test3_EdgePos_CreateAddr2Default(self):
        driver = self.driver
        driver.get(H.main_url)  # open URL - home page
        # driver.set_window_size(1200, 800)  # Set another Window Size
        print("***********************************************************\n"
              "TEST 3 - CREATING THE SECOND NEW ADDRESS AND SET IT DEFAULT\n"
              "***********************************************************")
        H.check_API_code(driver)  # Check API response code
        H.assert_title(driver, "Home | California Marcketing")  # Verify Homepage Title
        wait = WebDriverWait(driver, 5)  # Create variable for wait.until
        # Check that an elements are present and visible on the Home page
        H.home_page_elements(driver, "LET CALIFORNIA MARKETING GROW YOUR BUSINECS", "CALIFORNIA MARCKETING")
        H.delay()
        H.login(driver)  # Log In in exist account
        # Wait and click on user's account button for opening drop-down menu
        wait.until(EC.element_to_be_clickable((By.XPATH, H.btn_users_account)))
        driver.find_element(By.XPATH, H.btn_users_account).click()
        wait.until(EC.element_to_be_clickable((By.XPATH, H.item_My_addresses)))
        driver.find_element(By.XPATH, H.item_My_addresses).click()  # Select item 'My Addresses' in drop-down menu
        time.sleep(5)
        H.assert_title(driver, "My Addresses")  # Verify page 'My Addresses' Title
        driver.switch_to.frame(0)  # Switch to Frame (For Chrome and Edge index=0, for FireFox index=1)
        time.sleep(3)
        driver.find_element(By.XPATH, H.btn_Add_New_Address).click()  # Find button "Add new address" and click on it
        driver.switch_to.default_content()  # Go to parent Frame
        driver.switch_to.frame(3)  # Switch to another Frame
        H.delay()
        # Enter second new Address manually
        driver.find_element(By.ID, "firstName-field").click()
        driver.find_element(By.ID, "firstName-field").send_keys("Wolfgang Amadeus")
        driver.find_element(By.ID, "lastName-field").click()
        driver.find_element(By.ID, "lastName-field").send_keys("Mozart")
        driver.find_element(By.ID, "company-field").click()
        driver.find_element(By.ID, "company-field").send_keys("Requiem")
        driver.find_element(By.ID, "addressLine1-field").click()
        driver.find_element(By.ID, "addressLine1-field").send_keys("Glocknerstrasse 63")
        driver.find_element(By.ID, "addressLine2-field").click()
        driver.find_element(By.ID, "addressLine2-field").send_keys("63")
        driver.find_element(By.ID, "city-field").click()
        driver.find_element(By.ID, "city-field").send_keys("Hochgreit")
        H.delay()
        # Enter country and subdivision manually from drop-down list
        H.scroll_to_bottom_frame3(driver)  # Scroll to bottom in frame3
        # Click on country-field, find and choose country from list
        driver.find_element(By.ID, "country-field").click()
        driver.findElement(By.XPATH, "//*[contains(text(),'Austria')]")
        time.sleep(1)
        driver.find_element(By.XPATH, "//*[contains(text(),'Austria')]").click()
        # Click on subdivision-field, find and choose subdivision from list
        driver.find_element(By.ID, "subdivision-field").click()
        driver.findElement(By.XPATH, "//*[contains(text(),'Wien')]")
        time.sleep(1)
        driver.find_element(By.XPATH, "//*[contains(text(),'Wien')]").click()
        driver.find_element(By.ID, "zipCode-field").click()
        driver.find_element(By.ID, "zipCode-field").send_keys("8045")
        driver.find_element(By.ID, "phone-field").click()
        driver.find_element(By.ID, "phone-field").send_keys("0688 515 10 71")
        H.scroll_to_bottom_frame3(driver)  # Scroll to current frame's bottom
        driver.find_element(By.XPATH, H.checkbox_default).click()  # Set second new address as default
        driver.find_element(By.XPATH, H.btn_Add_Address).click()  # Click on button 'Add Address'
        time.sleep(3)
        driver.switch_to.frame(0)  # Go to Frame (for Chrome and Edge index=0, for FireFox index=1)
        time.sleep(3)
        H.scroll_to_my_addresses(driver)  # Scroll to list 'My Addresses'
        # Check that second New address is created and make it screenshot
        try:
            wait.until(EC.visibility_of_element_located((By.XPATH, "//*[contains(text(),'Wolfgang Amadeus Mozart')]")))
            print("Second new address is created:")
            print(driver.find_element(By.XPATH, "//*[contains(text(),'Wolfgang Amadeus Mozart')]").text)
            driver.get_screenshot_as_file("Second address as default-Edge.png")
        except TimeoutException:
            print("Second new address is not in list")
        # Wait for row with needed values loading
        wait.until(EC.visibility_of_all_elements_located((By.XPATH, "//*[contains(text(),'Wolfgang Amadeus "
                                                                    "Mozart')]//following::div[1]")))
        # Check that second New address set as default
        try:
            default = driver.find_element(By.XPATH, "//*[contains(text(),'Wolfgang Amadeus Mozart')]"
                                                    "//following::div[4]/span")
            print("Second new address has attribute: ", default.get_attribute("data-hook"))
            print("Second new address is set as", default.text, "\nTEST 3 PASS")
        except NoSuchElementException:
            print("Second new address is not set as default\nTEST 3 FAIL")
            raise Exception("Second new address is not set as default\nTEST 3 FAIL")
        driver.close()

    def test4_EdgePos_UpdateAddr2(self):
        driver = self.driver
        driver.get(H.main_url)  # open URL - home page
        # driver.set_window_size(1200, 800)  # Set another Window Size
        print("****************************************\n"
              "TEST 4 - UPDATING THE SECOND NEW ADDRESS\n"
              "****************************************")
        H.check_API_code(driver)  # Check API response code
        H.assert_title(driver, "Home | California Marcketing")  # Verify Homepage Title
        wait = WebDriverWait(driver, 5)  # Create variable for wait.until
        # Check that an elements are present and visible on the Home page
        H.home_page_elements(driver, "LET CALIFORNIA MARKETING GROW YOUR BUSINECS", "CALIFORNIA MARCKETING")
        H.delay()
        H.login(driver)  # Log In in exist account
        # Wait and click on user's account button for opening drop-down menu
        wait.until(EC.element_to_be_clickable((By.XPATH, H.btn_users_account)))
        driver.find_element(By.XPATH, H.btn_users_account).click()
        wait.until(EC.element_to_be_clickable((By.XPATH, H.item_My_addresses)))
        driver.find_element(By.XPATH, H.item_My_addresses).click()  # Select item 'My Addresses' in drop-down menu
        time.sleep(5)
        H.assert_title(driver, "My Addresses")  # Verify page 'My Addresses' Title
        driver.switch_to.frame(0)  # Switch to Frame (For Chrome and Edge index=0, for FireFox index=1)
        H.scroll_to_my_addresses(driver)  # Scroll to list 'My Addresses'
        time.sleep(3)
        # Find button 'Edit' of the second new address and click on it
        driver.find_element(By.XPATH, "//*[contains(text(),'Wolfgang Amadeus Mozart')]"
                                      "//following::button[1]").click()
        driver.switch_to.default_content()  # Go to parent Frame
        driver.switch_to.frame(3)  # Switch to another Frame
        time.sleep(3)
        # Update second new Address manually
        driver.find_element(By.ID, "firstName-field").click()
        driver.find_element(By.ID, "firstName-field").send_keys(Keys.CONTROL + "a", Keys.DELETE)
        driver.find_element(By.ID, "firstName-field").send_keys("Antonio")
        driver.find_element(By.ID, "lastName-field").click()
        driver.find_element(By.ID, "lastName-field").send_keys(Keys.CONTROL + "a", Keys.DELETE)
        driver.find_element(By.ID, "lastName-field").send_keys("Salieri")
        driver.find_element(By.ID, "company-field").click()
        driver.find_element(By.ID, "company-field").send_keys(Keys.CONTROL + "a", Keys.DELETE)
        driver.find_element(By.ID, "company-field").send_keys("Der Rauchfangkehrer ")
        driver.find_element(By.ID, "addressLine1-field").click()
        driver.find_element(By.ID, "addressLine1-field").send_keys(Keys.CONTROL + "a", Keys.DELETE)
        driver.find_element(By.ID, "addressLine1-field").send_keys("Leopoldstrabe 77")
        driver.find_element(By.ID, "addressLine2-field").click()
        driver.find_element(By.ID, "addressLine2-field").send_keys(Keys.CONTROL + "a", Keys.DELETE)
        driver.find_element(By.ID, "addressLine2-field").send_keys("55")
        driver.find_element(By.ID, "city-field").click()
        driver.find_element(By.ID, "city-field").send_keys(Keys.CONTROL + "a", Keys.DELETE)
        driver.find_element(By.ID, "city-field").send_keys("Berlin Dahlem")
        H.delay()
        # Enter country and subdivision manually from drop-down list
        H.scroll_to_bottom_frame3(driver)  # Scroll to current frame's bottom
        # Click on country-field, find and choose country from list
        driver.find_element(By.ID, "country-field").click()
        driver.findElement(By.XPATH, "//*[contains(text(),'Germany')]")
        time.sleep(1)
        driver.find_element(By.XPATH, "//*[contains(text(),'Germany')]").click()
        # Click on subdivision-field, find and choose subdivision from list
        driver.find_element(By.ID, "subdivision-field").click()
        driver.findElement(By.XPATH, "//*[contains(text(),'Berlin')]")
        time.sleep(1)
        driver.find_element(By.XPATH, "//*[contains(text(),'Berlin')]").click()
        driver.find_element(By.ID, "zipCode-field").click()
        driver.find_element(By.ID, "zipCode-field").send_keys(Keys.CONTROL + "a", Keys.DELETE)
        driver.find_element(By.ID, "zipCode-field").send_keys("14195")
        driver.find_element(By.ID, "phone-field").click()
        driver.find_element(By.ID, "phone-field").send_keys(Keys.CONTROL + "a", Keys.DELETE)
        driver.find_element(By.ID, "phone-field").send_keys("030 19 40 32")
        H.scroll_to_bottom_frame3(driver)  # Scroll to current frame's bottom
        driver.find_element(By.XPATH, H.btn_Update_Address).click()  # Click on button 'Update Address'
        time.sleep(3)
        driver.switch_to.frame(0)  # Go to Frame (for Chrome and Edge index=0, for FireFox index=1)
        time.sleep(3)
        H.scroll_to_my_addresses(driver)  # Scroll to list 'My Addresses'
        # Check that second New address is updated and make it screenshot
        try:
            wait.until(EC.visibility_of_element_located((By.XPATH, "//*[contains(text(),'Antonio Salieri')]")))
            print("Second new address is updated:")
            print(driver.find_element(By.XPATH, "//*[contains(text(),'Antonio Salieri')]").text)
            print("Changing values in second new address is available\nTEST 4 PASS")
            driver.get_screenshot_as_file("Second address updated-Edge.png")
        except TimeoutException:
            print("Second new address is NOT updated\nTEST 4 FAIL")
            raise Exception("Second new address is NOT updated\nTEST 4 FAIL")
        driver.close()

    def test5_EdgePos_DeleteAddr2(self):
        driver = self.driver
        driver.get(H.main_url)  # open URL - home page
        # driver.set_window_size(1200, 800)  # Set another Window Size
        print("****************************************\n"
              "TEST 5 - DELETING THE SECOND NEW ADDRESS\n"
              "****************************************")
        H.check_API_code(driver)  # Check API response code
        H.assert_title(driver, "Home | California Marcketing")  # Verify Homepage Title
        wait = WebDriverWait(driver, 5)  # Create variable for wait.until
        # Check that an elements are present and visible on the Home page
        H.home_page_elements(driver, "LET CALIFORNIA MARKETING GROW YOUR BUSINECS", "CALIFORNIA MARCKETING")
        H.delay()
        H.login(driver)  # Log In in exist account
        # Wait and click on user's account button for opening drop-down menu
        wait.until(EC.element_to_be_clickable((By.XPATH, H.btn_users_account)))
        driver.find_element(By.XPATH, H.btn_users_account).click()
        wait.until(EC.element_to_be_clickable((By.XPATH, H.item_My_addresses)))
        driver.find_element(By.XPATH, H.item_My_addresses).click()  # Select item 'My Addresses' in drop-down menu
        time.sleep(5)
        H.assert_title(driver, "My Addresses")  # Verify page 'My Addresses' Title
        driver.switch_to.frame(0)  # Switch to Frame (For Chrome and Edge index=0, for FireFox index=1)
        H.scroll_to_my_addresses(driver)  # Scroll to list 'My Addresses'
        time.sleep(3)
        # Find and click on button 'Remove' of the new second address, then click on button 'Yes'
        driver.find_element(By.XPATH, "//*[contains(text(),'Antonio Salieri')]//following::button[2]").click()
        H.delay()
        driver.find_element(By.XPATH, "//*[contains(text(),'Antonio Salieri')]//following::span[2]/div/button").click()
        time.sleep(3)
        H.scroll_to_my_addresses(driver)  # Scroll to list 'My Addresses'
        # Check that second New address is deleted and make screenshot
        try:
            wait.until(EC.visibility_of_element_located((By.XPATH, "//*[contains(text(),'Antonio Salieri')]")))
            print("Second new address is NOT deleted")
        except TimeoutException:
            print("Second new address is deleted")
            driver.get_screenshot_as_file("Second address deleted-Edge.png")
        if not "Antonio Salieri" in driver.page_source:
            print("Address removing completed successfully\nTEST 5 PASS")
        else:
            print("Address removing is NOT completed\nTEST 5 FAIL")
            raise Exception("Address removing is NOT completed\nTEST 5 FAIL")
        print("**********************************************************\n"
              "CHECK SAVED ADDRESSES IN THE LIST AND DELETE ALL ADDRESSES\n"
              "**********************************************************")
        H.check_and_delete_sav_addresses(driver)
        try:
            wait = WebDriverWait(driver, 5)  # Create variable for wait.until
            wait.until(EC.visibility_of_element_located((By.XPATH, "//div[@class='_3oKYs']"
                                                                   "[contains(text(), 'saved any addresses yet.')]")))
            print("---------------------------------------------------------\n"
                  "All addresses is removed or List 'My Addresses' was empty")
            driver.get_screenshot_as_file("All addresses is deleted-Chrome.png")
        except TimeoutException:
            print("-----------------------------------\nAddresses is not completely removed")
        driver.close()

    def test6_EdgeNeg_Fname_numbers(self):
        driver = self.driver
        driver.get(H.main_url)  # open URL - home page
        # driver.set_window_size(1200, 800)  # Set another Window Size
        print("*****************************************************************\n"
              "TEST 6 - CREATING THE ADDRESS WITH INCORRECT FIRST NAME (NUMBERS)\n"
              "*****************************************************************")
        H.check_API_code(driver)  # Check API response code
        H.assert_title(driver, "Home | California Marcketing")  # Verify Homepage Title
        wait = WebDriverWait(driver, 5)  # Create variable for wait.until
        # Check that an elements are present and visible on the Home page
        H.home_page_elements(driver, "LET CALIFORNIA MARKETING GROW YOUR BUSINECS", "CALIFORNIA MARCKETING")
        H.delay()
        H.login(driver)  # Log In in exist account
        # Wait and click on user's account button for opening drop-down menu
        wait.until(EC.element_to_be_clickable((By.XPATH, H.btn_users_account)))
        driver.find_element(By.XPATH, H.btn_users_account).click()
        wait.until(EC.element_to_be_clickable((By.XPATH, H.item_My_addresses)))
        driver.find_element(By.XPATH, H.item_My_addresses).click()  # Select item 'My Addresses' in drop-down menu
        time.sleep(5)
        H.assert_title(driver, "My Addresses")  # Verify page 'My Addresses' Title
        driver.switch_to.frame(0)  # Switch to Frame (For Chrome and Edge index=0, for FireFox index=1)
        time.sleep(3)
        driver.find_element(By.XPATH, H.btn_Add_New_Address).click()  # Find button "Add new address" and click on it
        driver.switch_to.default_content()  # Go to parent Frame
        driver.switch_to.frame(3)  # Switch to another Frame
        H.delay()
        H.address_create(driver, "0123456789")  # Enter First name manually, other values of Address random by Faker
        H.scroll_to_bottom_frame3(driver)  # Scroll bottom in frame 3
        driver.find_element(By.XPATH, H.btn_Add_Address).click()  # Click on button 'Add Address'
        H.check_btn_AddAddress(driver, TimeoutException)  # Check button 'Add Address' working
        time.sleep(3)
        driver.switch_to.frame(0)  # Go to Frame (for Chrome and Edge index=0, for FireFox index=1)
        time.sleep(3)
        H.scroll_to_my_addresses(driver)  # Scroll to list 'My Addresses'
        # Check that the Address with incorrect First name is not created and delete it if created
        H.check_createAddr_incorrect_FirstName(driver, "//address[contains(text(),'0123456789')]", "6", "Edge")
        driver.close()

    def test7_EdgeNeg_Fname_spec_char(self):
        driver = self.driver
        driver.get(H.main_url)  # open URL - home page
        # driver.set_window_size(1200, 800)  # Set another Window Size
        print("****************************************************************************\n"
              "TEST 7 - CREATING THE ADDRESS WITH INCORRECT FIRST NAME (SPECIAL CHARACTERS)\n"
              "****************************************************************************")
        H.check_API_code(driver)  # Check API response code
        H.assert_title(driver, "Home | California Marcketing")  # Verify Homepage Title
        wait = WebDriverWait(driver, 5)  # Create variable for wait.until
        # Check that an elements are present and visible on the Home page
        H.home_page_elements(driver, "LET CALIFORNIA MARKETING GROW YOUR BUSINECS", "CALIFORNIA MARCKETING")
        H.delay()
        H.login(driver)  # Log In in exist account
        # Wait and click on user's account button for opening drop-down menu
        wait.until(EC.element_to_be_clickable((By.XPATH, H.btn_users_account)))
        driver.find_element(By.XPATH, H.btn_users_account).click()
        wait.until(EC.element_to_be_clickable((By.XPATH, H.item_My_addresses)))
        driver.find_element(By.XPATH, H.item_My_addresses).click()  # Select item 'My Addresses' in drop-down menu
        time.sleep(5)
        H.assert_title(driver, "My Addresses")  # Verify page 'My Addresses' Title
        driver.switch_to.frame(0)  # Switch to Frame (For Chrome and Edge index=0, for FireFox index=1)
        time.sleep(3)
        driver.find_element(By.XPATH, H.btn_Add_New_Address).click()  # Find button "Add new address" and click on it
        driver.switch_to.default_content()  # Go to parent Frame
        driver.switch_to.frame(3)  # Switch to another Frame
        H.delay()
        H.address_create(driver, "!@#$%^&*()")  # Enter First name manually, other values of Address random by Faker
        H.scroll_to_bottom_frame3(driver)  # Scroll bottom in frame 3
        driver.find_element(By.XPATH, H.btn_Add_Address).click()  # Click on button 'Add Address'
        H.check_btn_AddAddress(driver, TimeoutException)  # Check button 'Add Address' working
        time.sleep(3)
        driver.switch_to.frame(0)  # Go to Frame (for Chrome and Edge index=0, for FireFox index=1)
        time.sleep(3)
        H.scroll_to_my_addresses(driver)  # Scroll to list 'My Addresses'
        # Check that the Address with incorrect First name is not created and delete it if created
        H.check_createAddr_incorrect_FirstName(driver, "//address[contains(text(),'!@#$%^&*()')]", "7", "Edge")
        driver.close()

    def test8_EdgeNeg_Fname_empty(self):
        driver = self.driver
        driver.get(H.main_url)  # open URL - home page
        # driver.set_window_size(1200, 800)  # Set another Window Size
        print("***************************************************************\n"
              "TEST 8 - CREATING THE ADDRESS WITH INCORRECT FIRST NAME (EMPTY)\n"
              "***************************************************************")
        H.check_API_code(driver)  # Check API response code
        H.assert_title(driver, "Home | California Marcketing")  # Verify Homepage Title
        wait = WebDriverWait(driver, 5)  # Create variable for wait.until
        # Check that an elements are present and visible on the Home page
        H.home_page_elements(driver, "LET CALIFORNIA MARKETING GROW YOUR BUSINECS", "CALIFORNIA MARCKETING")
        H.delay()
        H.login(driver)  # Log In in exist account
        # Wait and click on user's account button for opening drop-down menu
        wait.until(EC.element_to_be_clickable((By.XPATH, H.btn_users_account)))
        driver.find_element(By.XPATH, H.btn_users_account).click()
        wait.until(EC.element_to_be_clickable((By.XPATH, H.item_My_addresses)))
        driver.find_element(By.XPATH, H.item_My_addresses).click()  # Select item 'My Addresses' in drop-down menu
        time.sleep(5)
        H.assert_title(driver, "My Addresses")  # Verify page 'My Addresses' Title
        driver.switch_to.frame(0)  # Switch to Frame (For Chrome and Edge index=0, for FireFox index=1)
        time.sleep(3)
        driver.find_element(By.XPATH, H.btn_Add_New_Address).click()  # Find button "Add new address" and click on it
        driver.switch_to.default_content()  # Go to parent Frame
        driver.switch_to.frame(3)  # Switch to another Frame
        H.delay()
        H.address_create(driver, "")  # Enter First name manually, other values of Address random by Faker
        H.scroll_to_bottom_frame3(driver)  # Scroll bottom in frame 3
        driver.find_element(By.XPATH, H.btn_Add_Address).click()  # Click on button 'Add Address'
        H.check_btn_AddAddress(driver, TimeoutException)  # Check button 'Add Address' working
        time.sleep(3)
        driver.switch_to.frame(0)  # Go to Frame (for Chrome and Edge index=0, for FireFox index=1)
        time.sleep(3)
        H.scroll_to_my_addresses(driver)  # Scroll to list 'My Addresses'
        # Check that the Address with incorrect First name is not created and delete it if created
        H.check_createAddr_incorrect_FirstName(driver, "//address[contains(text(),'')]", "8", "Edge")
        driver.close()

    def test9_EdgeNeg_Fname_lot_of_letter(self):
        driver = self.driver
        driver.get(H.main_url)  # open URL - home page
        # driver.set_window_size(1200, 800)  # Set another Window Size
        print("*****************************************************************************\n"
              "TEST 9 - CREATING THE ADDRESS WITH INCORRECT FIRST NAME (A LOT OF LETTER 'a')\n"
              "*****************************************************************************")
        H.check_API_code(driver)  # Check API response code
        H.assert_title(driver, "Home | California Marcketing")  # Verify Homepage Title
        wait = WebDriverWait(driver, 5)  # Create variable for wait.until
        # Check that an elements are present and visible on the Home page
        H.home_page_elements(driver, "LET CALIFORNIA MARKETING GROW YOUR BUSINECS", "CALIFORNIA MARCKETING")
        H.delay()
        H.login(driver)  # Log In in exist account
        # Wait and click on user's account button for opening drop-down menu
        wait.until(EC.element_to_be_clickable((By.XPATH, H.btn_users_account)))
        driver.find_element(By.XPATH, H.btn_users_account).click()
        wait.until(EC.element_to_be_clickable((By.XPATH, H.item_My_addresses)))
        driver.find_element(By.XPATH, H.item_My_addresses).click()  # Select item 'My Addresses' in drop-down menu
        time.sleep(5)
        H.assert_title(driver, "My Addresses")  # Verify page 'My Addresses' Title
        driver.switch_to.frame(0)  # Switch to Frame (For Chrome and Edge index=0, for FireFox index=1)
        time.sleep(3)
        driver.find_element(By.XPATH, H.btn_Add_New_Address).click()  # Find button "Add new address" and click on it
        driver.switch_to.default_content()  # Go to parent Frame
        driver.switch_to.frame(3)  # Switch to another Frame
        H.delay()
        # Enter First name manually, other values of Address random by Faker
        H.address_create(driver, "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
        H.scroll_to_bottom_frame3(driver)  # Scroll bottom in frame 3
        driver.find_element(By.XPATH, H.btn_Add_Address).click()  # Click on button 'Add Address'
        H.check_btn_AddAddress(driver, TimeoutException)  # Check button 'Add Address' working
        time.sleep(3)
        driver.switch_to.frame(0)  # Go to Frame (for Chrome and Edge index=0, for FireFox index=1)
        time.sleep(3)
        H.scroll_to_my_addresses(driver)  # Scroll to list 'My Addresses'
        # Check that the Address with incorrect First name is not created and delete it if created
        H.check_createAddr_incorrect_FirstName(driver, "//address[contains(text(),"
                                                       "'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')]", "9",
                                                       "Edge")
        driver.close()

    def tearDown(self):
        self.driver.quit()  # Close the browser.


class Firefox_AddressesTests(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.maximize_window()

    def test1_FirefoxPos_CheckDeleteAddr(self):
        driver = self.driver
        driver.get(H.main_url)  # open URL - home page
        # driver.set_window_size(1200, 800)  # Set another Window Size
        print("***********************************************************\n"
              "TEST 1 - SHOW ALL SAVED ADDRESSES AND DELETE IF ARE PRESENT\n"
              "***********************************************************")
        H.check_API_code(driver)  # Check API response code
        H.assert_title(driver, "Home | California Marcketing")  # Verify Homepage Title
        wait = WebDriverWait(driver, 10)  # Create variable for wait.until
        # Check that an elements are present and visible on the Home page
        H.home_page_elements(driver, "LET CALIFORNIA MARKETING GROW YOUR BUSINECS", "CALIFORNIA MARCKETING")
        H.delay()
        H.login(driver)  # Log In in exist account
        # Wait and click on user's account button for opening drop-down menu
        wait.until(EC.element_to_be_clickable((By.XPATH, H.btn_users_account)))
        driver.find_element(By.XPATH, H.btn_users_account).click()
        wait.until(EC.element_to_be_clickable((By.XPATH, H.item_My_addresses)))
        driver.find_element(By.XPATH, H.item_My_addresses).click()  # Select item 'My Addresses' in drop-down menu
        time.sleep(3)
        H.assert_title(driver, "My Addresses")  # Verify page 'My Addresses' Title
        driver.switch_to.frame(1)  # Switch to Frame (For Chrome and Edge index=0, for FireFox index=1)
        time.sleep(3)
        H.scroll_to_my_addresses(driver)  # Scroll to list 'My Addresses'
        print("Saved addresses in the list:\n------------------------------------------------")
        H.check_and_delete_sav_addresses(driver)  # Check, print and delete all addresses in the list
        # Check that all addresses is deleted from list or List 'My Addresses' was empty" and make screenshot
        try:
            wait.until(EC.visibility_of_element_located((By.XPATH, "//div[@class='_3oKYs']"
                                                                   "[contains(text(), 'saved any addresses yet.')]")))
            print("---------------------------------------------------------\n"
                  "All addresses is removed or List 'My Addresses' was empty\nTEST1 - PASS")
            driver.get_screenshot_as_file("All addresses is deleted-Firefox.png")
        except TimeoutException:
            print("-----------------------------------\nAddresses is not completely removed\nTEST 1 - FAIL")
            raise Exception("-----------------------------------\nAddresses is not completely removed\nTEST 1 - FAIL")
        driver.close()

    def test2_FirefoxPos_CreateAddr1(self):
        driver = self.driver
        driver.get(H.main_url)  # open URL - home page
        # driver.set_window_size(1200, 800)  # Set another Window Size
        print("***************************************\n"
              "TEST 2 - CREATING THE FIRST NEW ADDRESS\n"
              "***************************************")
        H.check_API_code(driver)  # Check API response code
        H.assert_title(driver, "Home | California Marcketing")  # Verify Homepage Title
        wait = WebDriverWait(driver, 5)  # Create variable for wait.until
        # Check that an elements are present and visible on the Home page
        H.home_page_elements(driver, "LET CALIFORNIA MARKETING GROW YOUR BUSINECS", "CALIFORNIA MARCKETING")
        H.delay()
        H.login(driver)  # Log In in exist account
        # Wait and click on user's account button for opening drop-down menu
        wait.until(EC.element_to_be_clickable((By.XPATH, H.btn_users_account)))
        driver.find_element(By.XPATH, H.btn_users_account).click()
        wait.until(EC.element_to_be_clickable((By.XPATH, H.item_My_addresses)))
        driver.find_element(By.XPATH, H.item_My_addresses).click()  # Select item 'My Addresses' in drop-down menu
        time.sleep(3)
        H.assert_title(driver, "My Addresses")  # Verify page 'My Addresses' Title
        driver.switch_to.frame(1)  # Switch to Frame (For Chrome and Edge index=0, for FireFox index=1)
        time.sleep(3)
        H.scroll_to_my_addresses(driver)  # Scroll to list 'My Addresses'
        driver.find_element(By.XPATH, H.btn_Add_New_Address).click()  # Find button "Add new address" and click on it
        driver.switch_to.default_content()  # Go to parent Frame
        driver.switch_to.frame(3)  # Switch to another Frame
        H.delay()
        H.address_create(driver, H.faker_class.first_name())  # Enter random values of first new Address by Faker
        H.scroll_to_bottom_frame3(driver)  # Scroll to current frame's bottom
        driver.find_element(By.XPATH, H.btn_Add_Address).click()  # Click on button 'Add Address'
        time.sleep(3)
        driver.switch_to.default_content()  # Switch to parent frame - Only for Firefox!!!
        driver.switch_to.frame(1)  # Go to Frame (for Chrome and Edge index=0, for FireFox index=1)
        time.sleep(3)
        H.scroll_to_my_addresses(driver)  # Scroll in the frame to list 'My Addresses'
        # Check that First New address is created
        try:
            wait.until(EC.visibility_of_element_located((By.XPATH, "//address[@class='m-wda']"
                                                                   "[@data-hook='formatted-address']")))
            print("First new address is created:")
            print(driver.find_element(By.XPATH, "//address[@class='m-wda'][@data-hook='formatted-address']").text)
            driver.get_screenshot_as_file("First new address-Firefox.png")
        except TimeoutException:
            print("First new address is not in list")

        if not "You haven't saved any addresses yet." in driver.page_source:
            print("New address with correct values is added.\nTEST 2 PASS")
        else:
            print("You haven't saved any addresses yet.\nTEST 2 FAIL")
            raise Exception("You haven't saved any addresses yet.\n TEST 2 FAIL")
        driver.close()

    def test3_FirefoxPos_CreateAddr2Default(self):
        driver = self.driver
        driver.get(H.main_url)  # open URL - home page
        # driver.set_window_size(1200, 800)  # Set another Window Size
        print("***********************************************************\n"
              "TEST 3 - CREATING THE SECOND NEW ADDRESS AND SET IT DEFAULT\n"
              "***********************************************************")
        H.check_API_code(driver)  # Check API response code
        H.assert_title(driver, "Home | California Marcketing")  # Verify Homepage Title
        wait = WebDriverWait(driver, 5)  # Create variable for wait.until
        # Check that an elements are present and visible on the Home page
        H.home_page_elements(driver, "LET CALIFORNIA MARKETING GROW YOUR BUSINECS", "CALIFORNIA MARCKETING")
        H.delay()
        H.login(driver)  # Log In in exist account
        # Wait and click on user's account button for opening drop-down menu
        wait.until(EC.element_to_be_clickable((By.XPATH, H.btn_users_account)))
        driver.find_element(By.XPATH, H.btn_users_account).click()
        wait.until(EC.element_to_be_clickable((By.XPATH, H.item_My_addresses)))
        driver.find_element(By.XPATH, H.item_My_addresses).click()  # Select item 'My Addresses' in drop-down menu
        time.sleep(3)
        H.assert_title(driver, "My Addresses")  # Verify page 'My Addresses' Title
        driver.switch_to.frame(1)  # Switch to Frame (For Chrome and Edge index=0, for FireFox index=1)
        time.sleep(3)
        H.scroll_to_my_addresses(driver)  # Scroll to list 'My Addresses'
        driver.find_element(By.XPATH, H.btn_Add_New_Address).click()  # Find button "Add new address" and click on it
        driver.switch_to.default_content()  # Go to parent Frame
        driver.switch_to.frame(3)  # Switch to another Frame
        H.delay()
        # Enter second new Address manually
        driver.find_element(By.ID, "firstName-field").click()
        driver.find_element(By.ID, "firstName-field").send_keys("Wolfgang Amadeus")
        driver.find_element(By.ID, "lastName-field").click()
        driver.find_element(By.ID, "lastName-field").send_keys("Mozart")
        driver.find_element(By.ID, "company-field").click()
        driver.find_element(By.ID, "company-field").send_keys("Requiem")
        driver.find_element(By.ID, "addressLine1-field").click()
        driver.find_element(By.ID, "addressLine1-field").send_keys("Glocknerstrasse 63")
        driver.find_element(By.ID, "addressLine2-field").click()
        driver.find_element(By.ID, "addressLine2-field").send_keys("63")
        driver.find_element(By.ID, "city-field").click()
        driver.find_element(By.ID, "city-field").send_keys("Hochgreit")
        H.delay()
        # Enter country and subdivision manually from drop-down list
        H.scroll_to_bottom_frame3(driver)  # Scroll to bottom in frame3
        # Click on country-field, find and choose country from list
        driver.find_element(By.ID, "country-field").click()
        driver.findElement(By.XPATH, "//*[contains(text(),'Austria')]")
        time.sleep(1)
        driver.find_element(By.XPATH, "//*[contains(text(),'Austria')]").click()
        # Click on subdivision-field, find and choose subdivision from list
        driver.find_element(By.ID, "subdivision-field").click()
        driver.findElement(By.XPATH, "//*[contains(text(),'Wien')]")
        time.sleep(1)
        driver.find_element(By.XPATH, "//*[contains(text(),'Wien')]").click()
        driver.find_element(By.ID, "zipCode-field").click()
        driver.find_element(By.ID, "zipCode-field").send_keys("8045")
        driver.find_element(By.ID, "phone-field").click()
        driver.find_element(By.ID, "phone-field").send_keys("0688 515 10 71")
        H.scroll_to_bottom_frame3(driver)  # Scroll to current frame's bottom
        driver.find_element(By.XPATH, H.checkbox_default).click()  # Set second new address as default
        driver.find_element(By.XPATH, H.btn_Add_Address).click()  # Click on button 'Add Address'
        time.sleep(3)
        driver.switch_to.default_content()  # Switch to parent frame - Only for Firefox!!!
        driver.switch_to.frame(1)  # Go to Frame (for Chrome and Edge index=0, for FireFox index=1)
        time.sleep(3)
        H.scroll_to_my_addresses(driver)  # Scroll to list 'My Addresses'
        # Check that second New address is created and make it screenshot
        try:
            wait.until(EC.visibility_of_element_located((By.XPATH, "//*[contains(text(),'Wolfgang Amadeus Mozart')]")))
            print("Second new address is created:")
            print(driver.find_element(By.XPATH, "//*[contains(text(),'Wolfgang Amadeus Mozart')]").text)
            driver.get_screenshot_as_file("Second address as default-Firefox.png")
        except TimeoutException:
            print("Second new address is not in list")
        # Wait for row with needed values loading
        wait.until(EC.visibility_of_all_elements_located((By.XPATH, "//*[contains(text(),'Wolfgang Amadeus "
                                                                    "Mozart')]//following::div[1]")))
        # Check that second New address set as default
        try:
            default = driver.find_element(By.XPATH, "//*[contains(text(),'Wolfgang Amadeus Mozart')]"
                                                    "//following::div[4]/span")
            print("Second new address has attribute: ", default.get_attribute("data-hook"))
            print("Second new address is set as", default.text, "\nTEST 3 PASS")
        except NoSuchElementException:
            print("Second new address is not set as default\nTEST 3 FAIL")
            raise Exception("Second new address is not set as default\nTEST 3 FAIL")
        driver.close()

    def test4_FirefoxPos_UpdateAddr2(self):
        driver = self.driver
        driver.get(H.main_url)  # open URL - home page
        # driver.set_window_size(1200, 800)  # Set another Window Size
        print("****************************************\n"
              "TEST 4 - UPDATING THE SECOND NEW ADDRESS\n"
              "****************************************")
        H.check_API_code(driver)  # Check API response code
        H.assert_title(driver, "Home | California Marcketing")  # Verify Homepage Title
        wait = WebDriverWait(driver, 5)  # Create variable for wait.until
        # Check that an elements are present and visible on the Home page
        H.home_page_elements(driver, "LET CALIFORNIA MARKETING GROW YOUR BUSINECS", "CALIFORNIA MARCKETING")
        H.delay()
        H.login(driver)  # Log In in exist account
        # Wait and click on user's account button for opening drop-down menu
        wait.until(EC.element_to_be_clickable((By.XPATH, H.btn_users_account)))
        driver.find_element(By.XPATH, H.btn_users_account).click()
        wait.until(EC.element_to_be_clickable((By.XPATH, H.item_My_addresses)))
        driver.find_element(By.XPATH, H.item_My_addresses).click()  # Select item 'My Addresses' in drop-down menu
        time.sleep(3)
        H.assert_title(driver, "My Addresses")  # Verify page 'My Addresses' Title
        driver.switch_to.frame(1)  # Switch to Frame (For Chrome and Edge index=0, for FireFox index=1)
        time.sleep(3)
        H.scroll_to_my_addresses(driver)  # Scroll to list 'My Addresses'
        # Find button 'Edit' of the new second address and click on it
        driver.find_element(By.XPATH, "//*[contains(text(),'Wolfgang Amadeus Mozart')]"
                                      "//following::button[1]").click()
        driver.switch_to.default_content()  # Go to parent Frame
        driver.switch_to.frame(3)  # Switch to another Frame
        time.sleep(3)
        # Update second new Address manually
        driver.find_element(By.ID, "firstName-field").click()
        driver.find_element(By.ID, "firstName-field").clear()
        driver.find_element(By.ID, "firstName-field").send_keys("Antonio")
        driver.find_element(By.ID, "lastName-field").click()
        driver.find_element(By.ID, "lastName-field").clear()
        driver.find_element(By.ID, "lastName-field").send_keys("Salieri")
        driver.find_element(By.ID, "company-field").click()
        driver.find_element(By.ID, "company-field").clear()
        driver.find_element(By.ID, "company-field").send_keys("Der Rauchfangkehrer ")
        driver.find_element(By.ID, "addressLine1-field").click()
        driver.find_element(By.ID, "addressLine1-field").clear()
        driver.find_element(By.ID, "addressLine1-field").send_keys("Leopoldstrabe 77")
        driver.find_element(By.ID, "addressLine2-field").click()
        driver.find_element(By.ID, "addressLine2-field").clear()
        driver.find_element(By.ID, "addressLine2-field").send_keys("55")
        driver.find_element(By.ID, "city-field").click()
        driver.find_element(By.ID, "city-field").clear()
        driver.find_element(By.ID, "city-field").send_keys("Berlin Dahlem")
        # Enter country and subdivision manually from drop-down list
        H.delay()
        H.scroll_to_bottom_frame3(driver)  # Scroll to current frame's bottom
        # Click on country-field, find and choose country from list
        driver.find_element(By.ID, "country-field").click()
        driver.findElement(By.XPATH, "//*[contains(text(),'Germany')]")
        time.sleep(1)
        driver.find_element(By.XPATH, "//*[contains(text(),'Germany')]").click()
        # Click on subdivision-field, find and choose subdivision from list
        driver.find_element(By.ID, "subdivision-field").click()
        driver.findElement(By.XPATH, "//*[contains(text(),'Berlin')]")
        time.sleep(1)
        driver.find_element(By.XPATH, "//*[contains(text(),'Berlin')]").click()
        driver.find_element(By.ID, "zipCode-field").click()
        driver.find_element(By.ID, "zipCode-field").clear()
        driver.find_element(By.ID, "zipCode-field").send_keys("14195")
        driver.find_element(By.ID, "phone-field").click()
        driver.find_element(By.ID, "phone-field").clear()
        driver.find_element(By.ID, "phone-field").send_keys("030 19 40 32")
        H.scroll_to_bottom_frame3(driver) # Scroll to current frame's bottom
        driver.find_element(By.XPATH, H.btn_Update_Address).click()  # Click on button 'Update Address'
        time.sleep(3)
        driver.switch_to.default_content()  # Switch to parent frame - Only for Firefox!!!
        driver.switch_to.frame(1)  # Go to Frame (for Chrome and Edge index=0, for FireFox index=1)
        time.sleep(3)
        H.scroll_to_my_addresses(driver)  # Scroll to list 'My Addresses'
        # Check that second New address is updated and make it screenshot
        try:
            wait.until(EC.visibility_of_element_located((By.XPATH, "//*[contains(text(),'Antonio Salieri')]")))
            print("Second new address is updated:")
            print(driver.find_element(By.XPATH, "//*[contains(text(),'Antonio Salieri')]").text)
            print("Changing values in second new address is available\nTEST 4 PASS")
            driver.get_screenshot_as_file("Second address updated-Firefox.png")
        except TimeoutException:
            print("Second new address is NOT updated\nTEST 4 FAIL")
            raise Exception("Second new address is NOT updated\nTEST 4 FAIL")
        driver.close()

    def test5_FirefoxPos_DeleteAddr2(self):
        driver = self.driver
        driver.get(H.main_url)  # open URL - home page
        # driver.set_window_size(1200, 800)  # Set another Window Size
        print("****************************************\n"
              "TEST 5 - DELETING THE SECOND NEW ADDRESS\n"
              "****************************************")
        H.check_API_code(driver)  # Check API response code
        H.assert_title(driver, "Home | California Marcketing")  # Verify Homepage Title
        wait = WebDriverWait(driver, 5)  # Create variable for wait.until
        # Check that an elements are present and visible on the Home page
        H.home_page_elements(driver, "LET CALIFORNIA MARKETING GROW YOUR BUSINECS", "CALIFORNIA MARCKETING")
        H.delay()
        H.login(driver)  # Log In in exist account
        # Wait and click on user's account button for opening drop-down menu
        wait.until(EC.element_to_be_clickable((By.XPATH, H.btn_users_account)))
        driver.find_element(By.XPATH, H.btn_users_account).click()
        wait.until(EC.element_to_be_clickable((By.XPATH, H.item_My_addresses)))
        driver.find_element(By.XPATH, H.item_My_addresses).click()  # Select item 'My Addresses' in drop-down menu
        time.sleep(3)
        H.assert_title(driver, "My Addresses")  # Verify page 'My Addresses' Title
        driver.switch_to.frame(1)  # Switch to Frame (For Chrome and Edge index=0, for FireFox index=1)
        time.sleep(3)
        H.scroll_to_my_addresses(driver)  # Scroll to list 'My Addresses'
        # Find and click on button 'Remove' of the new second address, then click on button 'Yes'
        driver.find_element(By.XPATH, "//*[contains(text(),'Antonio Salieri')]//following::button[2]").click()
        H.delay()
        driver.find_element(By.XPATH, "//*[contains(text(),'Antonio Salieri')]//following::span[2]/div/button").click()
        time.sleep(3)
        H.scroll_to_my_addresses(driver)  # Scroll to list 'My Addresses'
        # Check that second New address is deleted and make screenshot
        try:
            wait.until(EC.visibility_of_element_located((By.XPATH, "//*[contains(text(),'Antonio Salieri')]")))
            print("Second new address is NOT deleted")
        except TimeoutException:
            print("Second new address is deleted")
            driver.get_screenshot_as_file("Second address deleted-Firefox.png")
        if not "Antonio Salieri" in driver.page_source:
            print("Address removing completed successfully\nTEST 5 PASS")
        else:
            print("Address removing is NOT completed\nTEST 5 FAIL")
            raise Exception("Address removing is NOT completed\nTEST 5 FAIL")
        print("**********************************************************\n"
              "CHECK SAVED ADDRESSES IN THE LIST AND DELETE ALL ADDRESSES\n"
              "**********************************************************")
        H.check_and_delete_sav_addresses(driver)
        try:
            wait = WebDriverWait(driver, 5)  # Create variable for wait.until
            wait.until(EC.visibility_of_element_located((By.XPATH, "//div[@class='_3oKYs']"
                                                                   "[contains(text(), 'saved any addresses yet.')]")))
            print("---------------------------------------------------------\n"
                  "All addresses is removed or List 'My Addresses' was empty")
            driver.get_screenshot_as_file("All addresses is deleted-Chrome.png")
        except TimeoutException:
            print("-----------------------------------\nAddresses is not completely removed")
        driver.close()

    def test6_FirefoxNeg_Fname_numbers(self):
        driver = self.driver
        driver.get(H.main_url)  # open URL - home page
        # driver.set_window_size(1200, 800)  # Set another Window Size
        print("*****************************************************************\n"
              "TEST 6 - CREATING THE ADDRESS WITH INCORRECT FIRST NAME (NUMBERS)\n"
              "*****************************************************************")
        H.check_API_code(driver)  # Check API response code
        H.assert_title(driver, "Home | California Marcketing")  # Verify Homepage Title
        wait = WebDriverWait(driver, 5)  # Create variable for wait.until
        # Check that an elements are present and visible on the Home page
        H.home_page_elements(driver, "LET CALIFORNIA MARKETING GROW YOUR BUSINECS", "CALIFORNIA MARCKETING")
        H.delay()
        H.login(driver)  # Log In in exist account
        # Wait and click on user's account button for opening drop-down menu
        wait.until(EC.element_to_be_clickable((By.XPATH, H.btn_users_account)))
        driver.find_element(By.XPATH, H.btn_users_account).click()
        wait.until(EC.element_to_be_clickable((By.XPATH, H.item_My_addresses)))
        driver.find_element(By.XPATH, H.item_My_addresses).click()  # Select item 'My Addresses' in drop-down menu
        time.sleep(3)
        H.assert_title(driver, "My Addresses")  # Verify page 'My Addresses' Title
        driver.switch_to.frame(1)  # Switch to Frame (For Chrome and Edge index=0, for FireFox index=1)
        time.sleep(3)
        H.scroll_to_my_addresses(driver)  # Scroll to list 'My Addresses'
        driver.find_element(By.XPATH, H.btn_Add_New_Address).click()  # Find button "Add new address" and click on it
        driver.switch_to.default_content()  # Go to parent Frame
        driver.switch_to.frame(3)  # Switch to another Frame
        H.delay()
        H.address_create(driver, "0123456789")  # Enter First name manually, other values of Address random by Faker
        H.scroll_to_bottom_frame3(driver)  # Scroll bottom in frame 3
        driver.find_element(By.XPATH, H.btn_Add_Address).click()  # Click on button 'Add Address'
        H.check_btn_AddAddress(driver, NoSuchWindowException)  # Check button 'Add Address' working
        time.sleep(3)
        driver.switch_to.default_content()  # Switch to parent frame - Only for Firefox!!!
        driver.switch_to.frame(1)  # Go to Frame (for Chrome and Edge index=0, for FireFox index=1)
        time.sleep(3)
        H.scroll_to_my_addresses(driver)  # Scroll in the frame to list 'My Addresses'
        # Check that the Address with incorrect First name is not created and delete it if created
        H.check_createAddr_incorrect_FirstName(driver, "//address[contains(text(),'0123456789')]", "6", "Firefox")
        driver.close()

    def test7_FirefoxNeg_Fname_spec_char(self):
        driver = self.driver
        driver.get(H.main_url)  # open URL - home page
        # driver.set_window_size(1200, 800)  # Set another Window Size
        print("****************************************************************************\n"
              "TEST 7 - CREATING THE ADDRESS WITH INCORRECT FIRST NAME (SPECIAL CHARACTERS)\n"
              "****************************************************************************")
        H.check_API_code(driver)  # Check API response code
        H.assert_title(driver, "Home | California Marcketing")  # Verify Homepage Title
        wait = WebDriverWait(driver, 5)  # Create variable for wait.until
        # Check that an elements are present and visible on the Home page
        H.home_page_elements(driver, "LET CALIFORNIA MARKETING GROW YOUR BUSINECS", "CALIFORNIA MARCKETING")
        H.delay()
        H.login(driver)  # Log In in exist account
        # Wait and click on user's account button for opening drop-down menu
        wait.until(EC.element_to_be_clickable((By.XPATH, H.btn_users_account)))
        driver.find_element(By.XPATH, H.btn_users_account).click()
        wait.until(EC.element_to_be_clickable((By.XPATH, H.item_My_addresses)))
        driver.find_element(By.XPATH, H.item_My_addresses).click()  # Select item 'My Addresses' in drop-down menu
        time.sleep(3)
        H.assert_title(driver, "My Addresses")  # Verify page 'My Addresses' Title
        driver.switch_to.frame(1)  # Switch to Frame (For Chrome and Edge index=0, for FireFox index=1)
        time.sleep(3)
        H.scroll_to_my_addresses(driver)  # Scroll to list 'My Addresses'
        driver.find_element(By.XPATH, H.btn_Add_New_Address).click()  # Find button "Add new address" and click on it
        driver.switch_to.default_content()  # Go to parent Frame
        driver.switch_to.frame(3)  # Switch to another Frame
        H.delay()
        H.address_create(driver, "!@#$%^&*()")  # Enter First name manually, other values of Address random by Faker
        H.scroll_to_bottom_frame3(driver)  # Scroll bottom in frame 3
        driver.find_element(By.XPATH, H.btn_Add_Address).click()  # Click on button 'Add Address'
        H.check_btn_AddAddress(driver, NoSuchWindowException)  # Check button 'Add Address' working
        time.sleep(3)
        driver.switch_to.default_content()  # Switch to parent frame - Only for Firefox!!!
        driver.switch_to.frame(1)  # Go to Frame (for Chrome and Edge index=0, for FireFox index=1)
        time.sleep(3)
        H.scroll_to_my_addresses(driver)  # Scroll in the frame to list 'My Addresses'
        # Check that the Address with incorrect First name is not created and delete it if created
        H.check_createAddr_incorrect_FirstName(driver, "//address[contains(text(),'!@#$%^&*()')]", "7", "Firefox")
        driver.close()

    def test8_FirefoxNeg_Fname_empty(self):
        driver = self.driver
        driver.get(H.main_url)  # open URL - home page
        # driver.set_window_size(1200, 800)  # Set another Window Size
        print("***************************************************************\n"
              "TEST 8 - CREATING THE ADDRESS WITH INCORRECT FIRST NAME (EMPTY)\n"
              "***************************************************************")
        H.check_API_code(driver)  # Check API response code
        H.assert_title(driver, "Home | California Marcketing")  # Verify Homepage Title
        wait = WebDriverWait(driver, 5)  # Create variable for wait.until
        # Check that an elements are present and visible on the Home page
        H.home_page_elements(driver, "LET CALIFORNIA MARKETING GROW YOUR BUSINECS", "CALIFORNIA MARCKETING")
        H.delay()
        H.login(driver)  # Log In in exist account
        # Wait and click on user's account button for opening drop-down menu
        wait.until(EC.element_to_be_clickable((By.XPATH, H.btn_users_account)))
        driver.find_element(By.XPATH, H.btn_users_account).click()
        wait.until(EC.element_to_be_clickable((By.XPATH, H.item_My_addresses)))
        driver.find_element(By.XPATH, H.item_My_addresses).click()  # Select item 'My Addresses' in drop-down menu
        time.sleep(3)
        H.assert_title(driver, "My Addresses")  # Verify page 'My Addresses' Title
        driver.switch_to.frame(1)  # Switch to Frame (For Chrome and Edge index=0, for FireFox index=1)
        time.sleep(3)
        H.scroll_to_my_addresses(driver)  # Scroll to list 'My Addresses'
        driver.find_element(By.XPATH, H.btn_Add_New_Address).click()  # Find button "Add new address" and click on it
        driver.switch_to.default_content()  # Go to parent Frame
        driver.switch_to.frame(3)  # Switch to another Frame
        H.delay()
        H.address_create(driver, "")  # Enter First name manually, other values of Address random by Faker
        H.scroll_to_bottom_frame3(driver)  # Scroll bottom in frame 3
        driver.find_element(By.XPATH, H.btn_Add_Address).click()  # Click on button 'Add Address'
        H.check_btn_AddAddress(driver, NoSuchWindowException)  # Check button 'Add Address' working
        time.sleep(3)
        driver.switch_to.default_content()  # Switch to parent frame - Only for Firefox!!!
        driver.switch_to.frame(1)  # Go to Frame (for Chrome and Edge index=0, for FireFox index=1)
        time.sleep(3)
        H.scroll_to_my_addresses(driver)  # Scroll in the frame to list 'My Addresses'
        # Check that the Address with incorrect First name is not created and delete it if created
        H.check_createAddr_incorrect_FirstName(driver, "//address[contains(text(),'')]", "8", "Firefox")
        driver.close()

    def test9_FirefoxNeg_Fname_lot_of_letter(self):
        driver = self.driver
        driver.get(H.main_url)  # open URL - home page
        # driver.set_window_size(1200, 800)  # Set another Window Size
        print("*****************************************************************************\n"
              "TEST 9 - CREATING THE ADDRESS WITH INCORRECT FIRST NAME (A LOT OF LETTER 'a')\n"
              "*****************************************************************************")
        H.check_API_code(driver)  # Check API response code
        H.assert_title(driver, "Home | California Marcketing")  # Verify Homepage Title
        wait = WebDriverWait(driver, 5)  # Create variable for wait.until
        # Check that an elements are present and visible on the Home page
        H.home_page_elements(driver, "LET CALIFORNIA MARKETING GROW YOUR BUSINECS", "CALIFORNIA MARCKETING")
        H.delay()
        H.login(driver)  # Log In in exist account
        # Wait and click on user's account button for opening drop-down menu
        wait.until(EC.element_to_be_clickable((By.XPATH, H.btn_users_account)))
        driver.find_element(By.XPATH, H.btn_users_account).click()
        wait.until(EC.element_to_be_clickable((By.XPATH, H.item_My_addresses)))
        driver.find_element(By.XPATH, H.item_My_addresses).click()  # Select item 'My Addresses' in drop-down menu
        time.sleep(3)
        H.assert_title(driver, "My Addresses")  # Verify page 'My Addresses' Title
        driver.switch_to.frame(1)  # Switch to Frame (For Chrome and Edge index=0, for FireFox index=1)
        time.sleep(3)
        H.scroll_to_my_addresses(driver)  # Scroll to list 'My Addresses'
        driver.find_element(By.XPATH, H.btn_Add_New_Address).click()  # Find button "Add new address" and click on it
        driver.switch_to.default_content()  # Go to parent Frame
        driver.switch_to.frame(3)  # Switch to another Frame
        H.delay()
        # Enter First name manually, other values of Address random by Faker
        H.address_create(driver, "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
        H.scroll_to_bottom_frame3(driver)  # Scroll bottom in frame 3
        driver.find_element(By.XPATH, H.btn_Add_Address).click()  # Click on button 'Add Address'
        H.check_btn_AddAddress(driver, NoSuchWindowException)  # Check button 'Add Address' working
        time.sleep(3)
        driver.switch_to.default_content()  # Switch to parent frame - Only for Firefox!!!
        driver.switch_to.frame(1)  # Go to Frame (for Chrome and Edge index=0, for FireFox index=1)
        time.sleep(3)
        H.scroll_to_my_addresses(driver)  # Scroll in the frame to list 'My Addresses'
        # Check that the Address with incorrect First name is not created and delete it if created
        H.check_createAddr_incorrect_FirstName(driver, "//address[contains(text(), "
                                                       "'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')]", "9",
                                                       "Firefox")
        driver.close()

    def tearDown(self):
        self.driver.quit()  # Close the browser.


if __name__ == "__main__":
    unittest.main()
