from selenium import webdriver
from selenium.webdriver.common.by import By
import time

def login_to_rumble(username, password):
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
    time.sleep(5)

    return driver

def upload_to_rumble(driver, video_file_path, title, description):
    # Navigate to the upload page
    driver.get('https://rumble.com/upload')

    # Upload the video
    video_input = driver.find_element(By.ID, 'Filedata')  # Adjusted for the correct ID
    video_input.send_keys(video_file_path)

    # Fill in the title and description fields
    title_input = driver.find_element(By.ID, 'title')  # Assuming 'title' is the correct element ID
    description_input = driver.find_element(By.ID, 'description')  # Assuming 'description' is the correct element ID
    title_input.send_keys(title)
    description_input.send_keys(description)

    # Select the Podcast category from the dropdown (assuming category value for "Podcast" is known)
    category_input = driver.find_element(By.CSS_SELECTOR, 'input[placeholder="- Primary category -"]')
    category_input.click()

    # Select the Podcast option (assuming the value for podcast is '15' or any correct data-value)
    podcast_category_option = driver.find_element(By.CSS_SELECTOR, 'div.select-option[data-value="15"]')  # Adjust data-value as needed
    podcast_category_option.click()

    # Find the upload button and click it HHHEERRRERE
    upload_button = driver.find_element(By.ID, 'submitForm')  # Adjusted for the correct button ID
    upload_button.click()

    # Wait for the upload to complete (adjust time as necessary)
    time.sleep(10)

    # Toggle the first checkbox: "You have not signed an exclusive agreement with any other parties."
    checkbox_terms = driver.find_element(By.CSS_SELECTOR, 'label[for="crights"]')
    checkbox_terms.click()

    # Toggle the second checkbox: "Check here if you agree to our terms of service."
    checkbox_terms = driver.find_element(By.CSS_SELECTOR, 'label[for="cterms"]')
    checkbox_terms.click()

    time.sleep(2)

    # Scroll to the submit button
    submit_button = driver.find_element(By.ID, 'submitForm2')
    driver.execute_script("arguments[0].scrollIntoView(true);", submit_button)

    # Click the submit button
    submit_button.click()

    # Wait before quitting
    time.sleep(30)

    # Close the browser
    driver.quit()

# Read the password from a file
with open("/home/alexm/Desktop/rumble_pw", 'r') as file:
    password = file.read()

# Example usage of the functions
driver = login_to_rumble(
    username="alexandre.marcotte.1094@gmail.com",
    password=password
)

upload_to_rumble(
    driver,
    '/home/alexm/Downloads/Automated Python script to find the World Localisation of Tor IP Addresses.mp4',
    'Automated Python script to find the World Localisation of Tor IP Addresses',
    'My video description'
)