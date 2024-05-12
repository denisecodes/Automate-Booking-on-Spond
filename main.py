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

#Get today's date
today = dt.datetime.today().date()
seven_days = dt.timedelta(days=7)
one_week_from_today = (today + seven_days).strftime(f"%A, %-d %b at 11:00")
print(one_week_from_today)
time.sleep(1)

#Wait until badminton dates are loaded
WebDriverWait(driver, 10).until(
    EC.presence_of_all_elements_located((By.XPATH, '//*[@id="event_card_start_time"]'))
)

#Get dates for badminton sessions
spond_dates = driver.find_elements(By.XPATH, '//*[@id="event_card_start_time"]')
#Retrieves text of badminton dates, storing it into a list
badminton_dates = [spond_date.text for spond_date in spond_dates]
print(badminton_dates)

# Check if there is a session that is one week from today and book session
for badminton_date in badminton_dates:
    if one_week_from_today == badminton_date:
        print("There is a session in exactly one week from today")
        #Find an element by it's text value using xpath
        #Click the date of the session one week from today
        xpath_query = f"//*[@id='event_card_start_time' and contains(text(), '{badminton_date}')]"
        date_button = driver.find_element(By.XPATH, xpath_query)
        date_button.click()
        time.sleep(1)
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
    else:
        pass

driver.quit()
