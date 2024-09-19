from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


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

    def upload_video(self, video_file_path, title, description):
        """
        Uploads a video to Rumble.
        :param video_file_path: Path to the video file to be uploaded
        :param title: Title of the video
        :param description: Description of the video
        """
        print(f"Uploading video: {title}")
        self.driver.get('https://rumble.com/upload')

        # Upload the video
        video_input = self.driver.find_element(By.ID, 'Filedata')
        video_input.send_keys(video_file_path)

        # Fill in the title and description fields
        title_input = self.driver.find_element(By.ID, 'title')
        ###########description_input = self.driver.find_element(By.ID, 'description')
        title_input.send_keys(title)
        ################descript#ion_input.send_keys(description)

        # Select the Podcast category
        self._select_podcast()

        # Click the upload button
        upload_button = self.driver.find_element(By.ID, 'submitForm')
        self.driver.execute_script("arguments[0].scrollIntoView(true);", upload_button)

        upload_button.click()
        # Wait for the upload to complete
        time.sleep(5)

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
        podcast_option = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//div[contains(@class, 'select-option') and contains(text(), 'Podcast')]"))
        )
        podcast_option.click()

    def _select_category(self, category_name):

        """
        Selects a category from the dropdown menu on the Rumble upload page.
        :param category_name: Name of the category to select
        """
        print(f"Selecting category: {category_name}")
        category_input = self.driver.find_element(By.CSS_SELECTOR, 'input[placeholder="- Primary category -"]')
        category_input.click()

        # Select the Podcast option
        podcast_category_option = self.driver.find_element(By.XPATH,
                                                           f"//div[contains(@class, 'select-option') and normalize-space()='{category_name}']")
        podcast_category_option.click()

    def _agree_to_terms(self):
        """
        Clicks the checkboxes to agree to terms and conditions.
        """
        print("Agreeing to terms and conditions...")
        checkbox_rights = self.driver.find_element(By.CSS_SELECTOR, 'label[for="crights"]')
        checkbox_terms = self.driver.find_element(By.CSS_SELECTOR, 'label[for="cterms"]')
        checkbox_rights.click()
        checkbox_terms.click()

    def _submit_final_form(self):
        """
        Scrolls to and submits the final form to complete the upload.
        """
        print("Submitting the final form...")
        submit_button = self.driver.find_element(By.ID, 'submitForm2')
        self.driver.execute_script("arguments[0].scrollIntoView(true);", submit_button)
        submit_button.click()

        # Wait for the process to complete
        #TODO: replace with a function that look if the file is fully uploaded before clicking or leaving the page.
        time.sleep(20)

    def close(self):
        """Closes the WebDriver."""
        print("Closing the browser...")
        self.driver.quit()


def main():
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

        # Ensure the path is correct and spaces are handled
        uploader.upload_video(
            r"/media/alexm/ALEXM_HDD/1 Corinthians 5 ｜ Bro. Jim Wiebe.mkv",
            'Automated Python script to find the World Localisation of Tor IP Addresses',
            'My video description'
        )
    finally:
        # Close the browser
        uploader.close()



if __name__ == "__main__":
    main()
