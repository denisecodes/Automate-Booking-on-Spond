import time
import datetime as dt
import os
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.os_manager import ChromeType
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

chrome_service = Service(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install())

chrome_options = Options()
options = [
    "--headless",
    "--disable-gpu",
    "--window-size=1920,1200",
    "--ignore-certificate-errors",
    "--disable-extensions",
    "--no-sandbox",
    "--disable-dev-shm-usage"
]
for option in options:
    chrome_options.add_argument(option)

driver = webdriver.Chrome(service=chrome_service, options=chrome_options)

spond_login = "https://spond.com/landing/login/"
my_email = os.environ.get("MY_EMAIL")
my_password = os.environ.get("MY_PASSWORD")

#Login to spond
driver.get(spond_login)
time.sleep(1)
email_field = driver.find_element(By.NAME, "emailOrPhoneNumber")
email_field.send_keys(my_email)
password_field = driver.find_element(By.NAME, "password")
password_field.send_keys(my_password)
submit = driver.find_element(By.CLASS_NAME, "spinner-button")
submit.click()
time.sleep(1)

#Get date 7 days from today
today = dt.datetime.today().date()
seven_days = dt.timedelta(days=7)
one_week_from_today = (today + seven_days).strftime(f"%A, %-d %b at 11:00")
print(f"One week from today: {one_week_from_today}")

#Wait until badminton dates are loaded
WebDriverWait(driver, 20).until(
    EC.presence_of_all_elements_located((By.ID, 'event_card_start_time'))
)

#Check if there is a session one week from today
xpath_query = f"//*[@id='event_card_start_time' and contains(text(), '{one_week_from_today}')]"
try:
    driver.find_element(By.XPATH, xpath_query)
    print("There is a session one week from today")
except NoSuchElementException:
    print("There is no session one week from today")
else:
    date_button = driver.find_element(By.XPATH, xpath_query)
    date_button.click()
    time.sleep(2)
    while True:
        try:
            accept_button = driver.find_element(By.NAME, "accept-button")
        except NoSuchElementException:
            print("Accept button not found")
        else:
            accept_button.click()
            time.sleep(1)
            break
        finally:
            #Refresh the page
            driver.refresh()
            time.sleep(1)

driver.quit()
