import os
import shutil
from selenium import webdriver
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class RumbleUploader:
    def __init__(self, username, password, driver_path=None):
        """
        Initializes the RumbleUploader with credentials and sets up the WebDriver.
        :param username: Rumble account username
        :param password: Rumble account password
        :param driver_path: Optional path to the ChromeDriver, defaults to system's PATH
        """
        self.username = username
        self.password = password
        self.driver = self._init_driver(driver_path)

    def _init_driver(self, driver_path):
        """Initializes the Chrome WebDriver."""
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        driver = webdriver.Chrome(executable_path=driver_path, options=options) if driver_path else webdriver.Chrome(
            options=options)
        return driver

    def login(self):
        """
        Logs in to Rumble using the provided credentials.
        """
        print("Logging into Rumble...")
        self.driver.get('https://rumble.com/login')

        # Find the username and password fields and input the credentials
        username_field = self.driver.find_element(By.ID, 'login-username')
        password_field = self.driver.find_element(By.ID, 'login-password')

        # Input login credentials
        username_field.send_keys(self.username)
        password_field.send_keys(self.password)

        # Find the submit button and click it
        login_button = self.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
        login_button.click()

        # Wait for login to complete
        time.sleep(5)

        print("Login successful!")

    def upload_video(self, video_file_path, title):
        """
        Uploads a video to Rumble.
        :param video_file_path: Path to the video file to be uploaded
        :param title: Title of the video
        """
        print(f"Uploading video: {title}")
        self.driver.get('https://rumble.com/upload')

        # Upload the video
        video_input = self.driver.find_element(By.ID, 'Filedata')
        video_input.send_keys(video_file_path)

        # Fill in the title and description fields
        title_input = self.driver.find_element(By.ID, 'title')
        title_input.send_keys(title)

        # Select the Podcast category
        self._select_podcast()

        # Click the upload button
        upload_button = self.driver.find_element(By.ID, 'submitForm')
        self.driver.execute_script("arguments[0].scrollIntoView(true);", upload_button)

        upload_button.click()
        # Wait for the upload to complete
        #time.sleep(5)

        self._wait_until_100_percent()

        # Agree to terms and conditions
        self._agree_to_terms()

        # Submit the final form
        self._submit_final_form()

        print(f"Video uploaded: {title}")

    def _select_podcast(self):
        # Select Podcast category
        category_input = self.driver.find_element(By.CSS_SELECTOR, 'input[placeholder="- Primary category -"]')
        category_input.click()
        category_input.send_keys('P')
        podcast_option = WebDriverWait(self.driver, 1).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//div[contains(@class, 'select-option') and contains(text(), 'Podcast')]"))
        )
        podcast_option.click()

    def _agree_to_terms(self):
        """
        Clicks the checkboxes to agree to terms and conditions.
        """
        print("Agreeing to terms and conditions...")
        checkbox_rights = self.driver.find_element(By.CSS_SELECTOR, 'label[for="crights"]')
        checkbox_terms = self.driver.find_element(By.CSS_SELECTOR, 'label[for="cterms"]')
        checkbox_rights.click()
        checkbox_terms.click()

    import time

    def _wait_until_100_percent(self):
        """
               Scrolls to and submits the final form to complete the upload.
               Waits for the upload progress to reach 100% before clicking the submit button,
               while updating the current progress value every second.
               """
        print("Waiting for the upload to reach 100%...")

        # Poll the progress bar every second to track the current upload progress
        progress_selector = (By.CSS_SELECTOR, "span.top_percent")
        current_value = ""

        # Continuously check the progress until it reaches 100%
        while "100%" not in current_value:
            try:
                # Fetch the current value of the progress bar
                progress_bar = self.driver.find_element(*progress_selector)
                current_value = progress_bar.text.strip()

                # Print the current progress value
                print(f"Current upload progress: {current_value}")
            except Exception as e:
                print(f"Error fetching progress: {str(e)}")
                current_value = ""

            # Sleep for 1 second before checking again
            time.sleep(1)

        print("Upload complete, now submitting the form...")

    def _submit_final_form(self):

        # Scroll to and find the submit button
        submit_button = self.driver.find_element(By.ID, 'submitForm2')
        self.driver.execute_script("arguments[0].scrollIntoView(true);", submit_button)

        # Click the submit button
        submit_button.click()

        # Wait for the process to complete (wait for any post-submit redirects or loading)
        time.sleep(1)

    def close(self):
        """Closes the WebDriver."""
        print("Closing the browser...")
        self.driver.quit()


def main():
    # Folder where videos are located
    video_folder = "/media/alexm/ALEXM_HDD/"
    uploaded_folder = os.path.join(video_folder, "uploaded_video")

    # Create "uploaded_video" folder if it doesn't exist
    if not os.path.exists(uploaded_folder):
        os.makedirs(uploaded_folder)
        print(f"Created folder: {uploaded_folder}")

    # Read the password from a file
    with open("/home/alexm/Desktop/rumble_pw", 'r') as file:
        password = file.read().strip()

    # Initialize the RumbleUploader with credentials
    uploader = RumbleUploader(
        username="alexandre.marcotte.1094@gmail.com",
        password=password
    )

    try:
        # Log in to Rumble
        uploader.login()

        # Get list of all video files in the folder
        video_files = [f for f in os.listdir(video_folder) if f.endswith(('.mp4', '.mkv', '.avi', '.mov', '.flv', '.wmv'))]

        # Loop through all video files and upload
        for video_file in video_files:
            video_file_path = os.path.join(video_folder, video_file)
            title = os.path.splitext(video_file)[0]  # Use the filename (without extension) as title
            #description = "Uploaded via automated script"  # Placeholder description

            # Try to upload the video
            try:
                uploader.upload_video(video_file_path, title)
                # If upload is successful, move the file to the "uploaded_video" folder
                shutil.move(video_file_path, os.path.join(uploaded_folder, video_file))
                print(f"Moved {video_file} to {uploaded_folder}")
            except Exception as e:
                print(f"Failed to upload {video_file}: {str(e)}")

    finally:
        # Close the browser
        uploader.close()


if __name__ == "__main__":
    main()
