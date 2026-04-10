import gspread
from oauth2client.service_account import ServiceAccountCredentials
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


# ----------- Google Sheets Setup -----------
scope = ["https://spreadsheets.google.com/feeds",
         "https://www.googleapis.com/auth/drive"]

creds = ServiceAccountCredentials.from_json_keyfile_name(
    r"C:\Users\rudra\OneDrive\Documents\PYscraping\PY\bulkmessenger-491613-71ff5cb64362.json",
    scope
)

client = gspread.authorize(creds)
sheet = client.open("Mail").sheet1
data = sheet.get_all_records()

# ----------- Browser Setup -----------
#     # Path to Brave and ChromeDriver
# brave_path = r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe"
# chromedriver_path = r"C:\Users\rudra\Downloads\Brave\chromedriver-win64\chromedriver.exe"

#     # Setup options
# options = Options()
# options.binary_location = brave_path

#     # Initialize WebDriver
# service = Service(chromedriver_path)
# driver = webdriver.Chrome(service=service, options=options)

options = Options()
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--start-maximized")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
wait = WebDriverWait(driver, 20)

driver.get("https://mail.google.com")

input("Login to Gmail and press Enter...")

count = 0

# ----------- Sending Emails -----------
for row in data:
    name = row['Name']
    email = row['Email']

    subject = f"Application for Internship Opportunity at {name}"
    file_path1 = r"C:\Users\rudra\Downloads\Brave\Rudraksh_Arora_s_Resume.pdf"
    file_path2 = r"C:\Users\rudra\Downloads\Brave\LOR.pdf"


    message = f"""Dear Hiring Team at {name},

I hope this message finds you well.

I am a Computer Science Engineering student currently pursuing my degree, and I am writing to express my interest in securing an internship opportunity at {name}. I am keen to gain practical exposure and contribute to real-world projects in a professional environment like yours.

I have a strong foundation in programming, particularly in Java and Python, along with hands-on experience in projects involving web automation and problem-solving. I am eager to apply my skills, learn from your team, and grow under the guidance of experienced professionals.

I am looking for an internship duration of 2 to 6 months and am flexible to start on any date after April 4, 2026. I have attached my resume and Letter of Recommendation (LOR) for your consideration.

I would greatly appreciate the opportunity to intern at {name} and contribute meaningfully while enhancing my technical and professional abilities.

Thank you for your time and consideration. I look forward to your response.

Sincerely,
Rudraksh Arora
+91-8955134145
rudraksharora2005.ima@gmail.com
"""

    try:
        # Compose
        compose = wait.until(EC.element_to_be_clickable((By.XPATH, '//div[text()="Compose"]')))
        compose.click()
        time.sleep(1)

        # To field (FIXED)
        to_field = wait.until(EC.element_to_be_clickable((By.XPATH, '//input[@aria-label="To recipients"]')))
        to_field.send_keys(email)
        time.sleep(1)

        # Subject (your one was fine)
        subject_field = wait.until(EC.element_to_be_clickable((By.NAME, "subjectbox")))
        subject_field.send_keys(subject)

        # Body (IMPORTANT FIX: click before typing)
        body = wait.until(EC.presence_of_element_located(
        (By.XPATH, '//div[@aria-label="Message Body"]')
        ))
        driver.execute_script("arguments[0].focus();", body)
        body.send_keys(message)
        time.sleep(2)

        # Attachment 1 (hidden input, not the div you found)
        file_input = driver.find_element(By.XPATH, '//input[@type="file"]')
        driver.execute_script("arguments[0].style.display = 'block';", file_input)
        file_input.send_keys(file_path1)

        time.sleep(5)  # wait for upload

        # Attachment 2 (hidden input, not the div you found)
        file_input = driver.find_element(By.XPATH, '//input[@type="file"]')
        driver.execute_script("arguments[0].style.display = 'block';", file_input)
        file_input.send_keys(file_path2)

        time.sleep(5)  # wait for upload

        # Send (better selector)
        send_btn = wait.until(EC.element_to_be_clickable((By.XPATH, '//div[@role="button" and text()="Send"]')))
        send_btn.click()

        print(f"Sent to {name} ({email})")
        time.sleep(3)  # brief pause before next email
        count += 1

    except Exception as e:
        print(f"Failed for {name} {email}: {e}")

print(f"Total emails sent: {count}")