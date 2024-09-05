from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

def upload_to_rumble(video_file_path, title, description):
    # Set up the webdriver (Make sure you have ChromeDriver installed)
    driver = webdriver.Chrome()

    # Go to Rumble login page
    driver.get("https://rumble.com/login")

    time.sleep(10)
    # Log in to Rumble
    driver.find_element("login-username").send_keys("alexandre.marcotte.1094@gmail.com")
    with open("/home/alexm/Desktop/rumble_pw", 'r') as file:
        password = file.read()
    driver.find_element("login-password").send_keys(password)
    driver.find_element(By.CSS_SELECTOR, f'class="login-button login-form-button round-button bg-green"').click()

    time.sleep(10)  # Wait for login to complete

    # Navigate to upload page
    driver.get("https://rumble.com/upload")

    # Fill in the upload form
    driver.find_element(By.ID, "video_file").send_keys(video_file_path)
    driver.find_element(By.ID, "title").send_keys(title)
    driver.find_element(By.ID, "description").send_keys(description)

    # Submit the form
    driver.find_element(By.ID, "upload_button").click()

    time.sleep(20)  # Wait for upload to complete

    driver.quit()

# Example usage
upload_to_rumble(
    '/home/alexm/Downloads/Automated Python script to find the World Localisation of Tor IP Addresses.mp4.mp4',
    'Automated Python script to find the World Localisation of Tor IP Addresses',
    'My video description')
