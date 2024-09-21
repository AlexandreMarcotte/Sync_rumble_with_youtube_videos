import os
import shutil
import time
from selenium import webdriver
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
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-software-rasterizer")
        options.add_argument("--no-sandbox")
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
        """
        print(f"Uploading video: {title}")
        self.driver.get('https://rumble.com/upload')

        # Upload the video
        video_input = self.driver.find_element(By.ID, 'Filedata')
        video_input.send_keys(video_file_path)

        # Fill in the title field
        title_input = self.driver.find_element(By.ID, 'title')
        title_input.send_keys(title)

        # Fill in the title and description fields
        description_input = self.driver.find_element(By.ID, 'description')  # Assuming 'description' is the correct element ID
        description_input.send_keys(description)

        time.sleep(2)

        # Select the Podcast category
        self._select_podcast()


        # Click the upload button
        upload_button = self.driver.find_element(By.ID, 'submitForm')
        self.driver.execute_script("arguments[0].scrollIntoView(true);", upload_button)

        upload_button.click()

        # Wait for the upload to complete
        self._wait_until_100_percent()

        # Agree to terms and conditions
        self._agree_to_terms()

        # Submit the final form
        self._submit_final_form()

        print(f"Video uploaded: {title}")

    def _select_podcast(self):
        """Selects Podcast as the category."""
        category_input = self.driver.find_element(By.CSS_SELECTOR, 'input[placeholder="- Primary category -"]')
        category_input.click()
        category_input.send_keys('P')
        podcast_option = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//div[contains(@class, 'select-option') and contains(text(), 'Podcast')]"))
        )
        podcast_option.click()

    def _agree_to_terms(self):
        """Clicks the checkboxes to agree to terms and conditions."""
        print("Agreeing to terms and conditions...")
        checkbox_rights = self.driver.find_element(By.CSS_SELECTOR, 'label[for="crights"]')
        checkbox_terms = self.driver.find_element(By.CSS_SELECTOR, 'label[for="cterms"]')
        checkbox_rights.click()
        checkbox_terms.click()

    def _wait_until_100_percent(self):
        """Waits for the upload progress to reach 100%."""
        print("Waiting for the upload to reach 100%...")

        # Poll the progress bar every second to track the current upload progress
        progress_selector = (By.CSS_SELECTOR, "span.top_percent")
        current_value = ""

        # Continuously check the progress until it reaches 100%
        while "100%" not in current_value:
            try:
                progress_bar = self.driver.find_element(*progress_selector)
                current_value = progress_bar.text.strip()
                #print(f"Current upload progress: {current_value}")
            except Exception as e:
                print(f"Error fetching progress: {str(e)}")
                current_value = ""

            time.sleep(0.1)

        print("Upload complete, now submitting the form...")

    def _submit_final_form(self):
        """Submits the final form after the upload is complete."""
        submit_button = self.driver.find_element(By.ID, 'submitForm2')
        self.driver.execute_script("arguments[0].scrollIntoView(true);", submit_button)
        submit_button.click()
        time.sleep(1)

    def close(self):
        """Closes the WebDriver."""
        print("Closing the browser...")
        self.driver.quit()


### Main Function Clustered into Sub-functions ###

def read_credentials(password_file_path, username, password):
    """Reads credentials from file if needed."""
    if not password and os.path.exists(password_file_path):
        with open(password_file_path, 'r') as file:
            password = file.read().strip()

    if not username or not password:
        raise ValueError("Rumble username and password are required.")

    return username, password


def ensure_folders_exist(uploaded_folder):
    """Ensures the uploaded folder exists, creating it if needed."""
    if not os.path.exists(uploaded_folder):
        os.makedirs(uploaded_folder)
        print(f"Created folder: {uploaded_folder}")


def get_video_files(video_folder):
    """Returns a sorted list of video files based on modified time (oldest first)."""
    video_files = [
        f for f in os.listdir(video_folder)
        if f.endswith(('.mp4', '.mkv', '.avi', '.mov', '.flv', '.wmv', '.webm'))
    ]

    # Sort video files by modified time (oldest first)
    video_files = sorted(video_files, key=lambda x: os.path.getmtime(os.path.join(video_folder, x)))
    return video_files


def upload_videos(uploader, video_files, video_folder, uploaded_folder):
    """Uploads videos and tracks progress."""
    total_videos = len(video_files)
    upload_times = []

    for index, video_file in enumerate(video_files, start=1):
        video_file_path = os.path.join(video_folder, video_file)
        title = os.path.splitext(video_file)[0]
        description = """The Bible Way to Heaven in many Languages: 
https://sfbc.bw2h.com/

Church Website:
https://www.fortressbaptistchurch.com/
"""

        # Calculate videos left and estimate time left
        videos_left = total_videos - index
        if upload_times:
            avg_time_per_video = sum(upload_times) / len(upload_times)
            estimated_time_left = avg_time_per_video * videos_left
            print(f"Videos left to upload: {videos_left}, Estimated time left: {int(estimated_time_left // 60)} minutes, {int(estimated_time_left % 60)} seconds.")
        else:
            print(f"Videos left to upload: {videos_left}")

        # Start upload and measure time
        start_time = time.time()

        try:
            uploader.upload_video(video_file_path, title, description)
            time_taken = time.time() - start_time
            upload_times.append(time_taken)

            # Move uploaded file to "uploaded_video" folder
            shutil.move(video_file_path, os.path.join(uploaded_folder, video_file))
            print(f"Moved {video_file} to {uploaded_folder}")
        except Exception as e:
            print(f"Failed to upload {video_file}: {str(e)}")


def main():
    ### USER-FRIENDLY CONFIGURATION ###
    # Folder where videos are located
    video_folder = "/media/alexm/ALEXM_HDD/"  # Change this to your folder with videos

    # Folder to move uploaded videos
    uploaded_folder = os.path.join(video_folder, "uploaded_video")  # Ensure this folder exists or is created

    # Path to the file containing your Rumble password (optional)
    password_file_path = "/home/alexm/Desktop/rumble_pw"  # Update this to the location of your password file

    # Rumble account credentials (you can either provide directly or leave password as None to read from file)
    username = "FortressBaptist@proton.me"  # Change to your Rumble username
    password = None  # Leave as None if using a password file

    # Path to ChromeDriver (optional, only required if not set in your system PATH)
    driver_path = None  # Update this if you need a specific path for your ChromeDriver

    ### END OF CONFIGURATION ###

    # Read credentials
    username, password = read_credentials(password_file_path, username, password)

    # Ensure folders exist
    ensure_folders_exist(uploaded_folder)

    # Initialize uploader
    uploader = RumbleUploader(username=username, password=password, driver_path=driver_path)

    try:
        # Log in to Rumble
        uploader.login()

        # Get video files
        video_files = get_video_files(video_folder)

        # Upload videos
        upload_videos(uploader, video_files, video_folder, uploaded_folder)

    finally:
        # Close the browser
        uploader.close()


if __name__ == "__main__":
    main()
