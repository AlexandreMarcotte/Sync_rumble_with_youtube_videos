from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

def upload_to_rumble(video_file_path, title, description):
    # Set up the webdriver (Make sure you have ChromeDriver installed)
    driver = webdriver.Chrome()

    # Go to Rumble login page
    driver.get("https://rumble.com/login")

    # Log in to Rumble
    driver.find_element(By.NAME, "username").send_keys("your_rumble_username")
    driver.find_element(By.NAME, "password").send_keys("your_rumble_password")
    driver.find_element(By.NAME, "submit").click()

    time.sleep(5)  # Wait for login to complete

    # Navigate to upload page
    driver.get("https://rumble.com/upload")

    # Fill in the upload form
    driver.find_element(By.ID, "video_file").send_keys(video_file_path)
    driver.find_element(By.ID, "title").send_keys(title)
    driver.find_element(By.ID, "description").send_keys(description)

    # Submit the form
    driver.find_element(By.ID, "upload_button").click()

    time.sleep(10)  # Wait for upload to complete

    driver.quit()

# Example usage
upload_to_rumble('/path/to/your/video.mp4', 'My Video Title', 'My video description')
