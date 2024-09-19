import os
import shutil
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options  # Added for Chrome options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException,
    NoSuchElementException,
    ElementClickInterceptedException,
    ElementNotInteractableException,
)

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

        # Add a small delay before clicking the login button
        time.sleep(1)

        login_button = driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
        login_button.click()

        # Wait for login to complete
        WebDriverWait(driver, 20).until(
            lambda d: 'rumble.com/account' in d.current_url or d.find_elements(By.CSS_SELECTOR, '.alert-danger')
        )

        # Check if login was successful
        if 'rumble.com/account' in driver.current_url:
            print("Login successful!")
        else:
            error_message = driver.find_element(By.CSS_SELECTOR, '.alert-danger').text
            print(f"Login failed. Error message: {error_message}")
            raise Exception("Login failed")

    except TimeoutException:
        print("Login process timed out. Current URL:", driver.current_url)
        raise
    except Exception as e:
        print(f"An error occurred during login: {str(e)}")
        print(f"Current URL: {driver.current_url}")
        raise

def upload_video(driver, video_path, uploaded_folder):
    filename = os.path.basename(video_path)
    title = os.path.splitext(filename)[0]  # Use filename without extension as title

    driver.get('https://rumble.com/upload')

    # Wait for and locate the file input element
    video_input = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.ID, 'Filedata'))
    )
    video_input.send_keys(video_path)

    # Wait for the title field to be clickable
    title_input = WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable((By.ID, 'title'))
    )
    title_input.clear()
    title_input.send_keys(title)

    # Select 'Podcast' category
    category_input = driver.find_element(By.CSS_SELECTOR, 'input[placeholder="- Primary category -"]')
    category_input.click()
    time.sleep(1)  # Wait for the dropdown to load
    podcast_option = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'select-option') and normalize-space()='Podcast']"))
    )
    podcast_option.click()

    # Click the initial upload button
    upload_button = driver.find_element(By.ID, 'submitForm')
    upload_button.click()

    # Wait for the upload to complete and the rights checkboxes to appear
    WebDriverWait(driver, 300).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'label[for="crights"]'))
    )

    # Check the rights and terms checkboxes
    checkbox_rights = driver.find_element(By.CSS_SELECTOR, 'label[for="crights"]')
    checkbox_terms = driver.find_element(By.CSS_SELECTOR, 'label[for="cterms"]')
    checkbox_rights.click()
    checkbox_terms.click()

    # Wait for the final submit button to be clickable, then click it
    submit_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, 'submitForm2'))
    )
    driver.execute_script("arguments[0].scrollIntoView(true);", submit_button)
    submit_button.click()

    # Wait for redirection to the uploaded video page
    WebDriverWait(driver, 60).until(
        EC.url_contains('rumble.com/video/')
    )

    print(f"Successfully uploaded: {title}")

    # Move the uploaded file to the 'uploaded' folder
    shutil.move(video_path, os.path.join(uploaded_folder, filename))
    print(f"Moved {filename} to the uploaded folder")


def main():
    # Update these with your actual Rumble credentials
    username = "alexandre.marcotte.1094@gmail.com"

    # Read the password from a file
    with open("/home/alexm/Desktop/rumble_pw", 'r') as file:
        password = file.read().strip()

    # Set up Chrome options
    chrome_options = Options()
    # chrome_options.add_argument("--headless")  # Uncomment this line to run in headless mode
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--start-maximized")

    # Initialize the Chrome WebDriver
    driver = webdriver.Chrome(options=chrome_options)

    try:
        # Login once
        login_to_rumble(driver, username, password)

        # Directory containing the videos
        video_directory = "/media/alexm/ALEXM_HDD"

        # Create 'uploaded' folder in the root directory if it doesn't exist
        uploaded_folder = os.path.join(video_directory, "uploaded")
        os.makedirs(uploaded_folder, exist_ok=True)

        # List all video files in the directory
        video_files = [f for f in os.listdir(video_directory) if f.lower().endswith(('.mp4', '.avi', '.mov', '.flv', '.wmv'))]

        # Upload each video
        for video_file in video_files:
            video_path = os.path.join(video_directory, video_file)
            if upload_video(driver, video_path, uploaded_folder):
                print(f"Successfully processed {video_file}")
            else:
                print(f"Failed to process {video_file}")

    except Exception as e:
        print(f"An error occurred: {str(e)}")
    finally:
        # Always close the browser, even if an error occurred
        driver.quit()

if __name__ == "__main__":
    main()
