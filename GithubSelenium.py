from selenium import webdriver
from selenium.webdriver.common.by import By
import time

def login_to_github():
    driver = webdriver.Chrome()

    driver.get("https://github.com/login")

    driver.implicitly_wait(10)

    # Fill in the username and password inputs
    username_input = driver.find_element(By.NAME, "login")
    username_input.send_keys("")
    time.sleep(20)

    password_input = driver.find_element(By.NAME, "password")
    password_input.send_keys("")
    time.sleep(20)

    # Click the "Sign in" button
    sign_in_button = driver.find_element(By.NAME, "commit")
    sign_in_button.click()

    time.sleep(20)

    # After clicking "Sign in," GitHub may prompt for two-factor authentication (2FA) for some accounts.
    # You may need to handle the 2FA process manually if it occurs.

    # Print the page title after logging in (for demonstration purposes)
    print("Page title after logging in:", driver.title)
    time.sleep(20)

    # Don't forget to close the browser when you're done
    driver.quit()
    

login_to_github()
