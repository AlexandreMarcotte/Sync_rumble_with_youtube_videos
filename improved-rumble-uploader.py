import os
import shutil
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

def login_to_rumble(driver, username, password):
    try:
        driver.get('https://rumble.com/login')
        
        # Wait for the username field to be present
        username_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'login-username'))
        )
        password_field = driver.find_element(By.ID, 'login-password')
        
        username_field.send_keys(username)
        password_field.send_keys(password)
        
        login_button = driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
        login_button.click()
        
        # Wait for login to complete
        try:
            WebDriverWait(driver, 20).until(
                EC.any_of(
                    EC.url_contains('rumble.com/account'),
                    EC.presence_of_element_located((By.CSS_SELECTOR, '.alert-danger'))  # Error message
                )
            )
        except TimeoutException:
            print("Login process timed out. Current URL:", driver.current_url)
            print("Page source:", driver.page_source)
            raise

        # Check if login was successful
        if 'rumble.com/account' in driver.current_url:
            print("Login successful!")
        else:
            error_message = driver.find_element(By.CSS_SELECTOR, '.alert-danger').text
            print(f"Login failed. Error message: {error_message}")
            raise Exception("Login failed")

    except Exception as e:
        print(f"An error occurred during login: {str(e)}")
        print(f"Current URL: {driver.current_url}")
        raise

# The rest of the script remains the same...

def main():
    # TODO: Update these with your actual Rumble credentials
    username = "alexandre.marcotte.1094@gmail.com"
    
    # Read the password from a file
    with open("/home/alexm/Desktop/rumble_pw", 'r') as file:
        password = file.read().strip()
    
    # Initialize the Chrome WebDriver
    driver = webdriver.Chrome()
    
    try:
        # Login once
        login_to_rumble(driver, username, password)
        
        # ... (rest of the main function remains the same)

    except Exception as e:
        print(f"An error occurred: {str(e)}")
    finally:
        # Always close the browser, even if an error occurred
        driver.quit()

if __name__ == "__main__":
    main()

# TODO: Before running this script, make sure to:
# 1. Install required libraries: pip install selenium
# 2. Download and install the appropriate ChromeDriver for your Chrome version
# 3. Ensure you have a stable internet connection
# 4. Be aware of Rumble's upload limits and adjust the script if necessary
# 5. Update the username in the main() function if needed
# 6. Make sure the password file path is correct
# 7. Ensure you have write permissions in the video directory to create the 'uploaded' folder
# 8. Check if Rumble has implemented any CAPTCHA or additional security measures

# Note: This script assumes that the Rumble website structure hasn't changed. 
# If you encounter errors, you may need to update the element locators.
