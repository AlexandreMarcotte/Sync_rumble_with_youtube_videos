from selenium import webdriver
from selenium.webdriver.common.by import By
import time

def upload_to_rumble(video_file_path, title, description, username, password):
    # Set up the Chrome WebDriver (Make sure the path to chromedriver is correct)
    driver = webdriver.Chrome()

    # Open the Rumble login page
    driver.get('https://rumble.com/login')

    # Find the username and password fields and input the credentials
    username_field = driver.find_element(By.ID, 'login-username')
    password_field = driver.find_element(By.ID, 'login-password')

    # Input login credentials
    username_field.send_keys(username)
    password_field.send_keys(password)

    # Find the submit button and click it
    login_button = driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
    login_button.click()

    # Wait for login to complete
    time.sleep(10)

    # Navigate to the upload page
    driver.get('https://rumble.com/upload')

    # Upload the video
    video_input = driver.find_element(By.ID, 'Filedata')  # Correct ID for the video upload
    video_input.send_keys(video_file_path)

    # Fill in the title and description fields
    title_input = driver.find_element(By.ID, 'title')  # OK Assuming 'title' is the correct element ID
    description_input = driver.find_element(By.ID, 'description')  # OK Assuming 'description' is the correct element ID
    title_input.send_keys(title)
    description_input.send_keys(description)

    # Find the upload button and click it
    upload_button = driver.find_element(By.ID, 'submitForm')  # Correct ID for the upload button
    upload_button.click()

    # Wait for the upload to complete
    time.sleep(10)

    # Close the browser
    driver.quit()

with open("/home/alexm/Desktop/rumble_pw", 'r') as file:
    password = file.read()

# Example usage of the function
upload_to_rumble(
    '/home/alexm/Downloads/Automated Python script to find the World Localisation of Tor IP Addresses.mp4.mp4',
    'Automated Python script to find the World Localisation of Tor IP Addresses',
    'My video description',
    username="alexandre.marcotte.1094@gmail.com",
    password=password)
