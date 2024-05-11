import time
import datetime as dt
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import chromedriver_autoinstaller
from selenium.common import NoSuchElementException

chrome_options = webdriver.ChromeOptions()    
# Add your options as needed    
options = [
  # Define window size here
   "--window-size=1200,1200",
    "--ignore-certificate-errors"
 
    #"--headless",
    #"--disable-gpu",
    #"--window-size=1920,1200",
    #"--ignore-certificate-errors",
    #"--disable-extensions",
    #"--no-sandbox",
    #"--disable-dev-shm-usage",
    #'--remote-debugging-port=9222'
]

for option in options:
    chrome_options.add_argument(option)

    
driver = webdriver.Chrome(options = chrome_options)
spond_login = "https://spond.com/landing/login/"
my_email = os.environ.get("MY_EMAIL")
my_password = os.environ.get("MY_PASSWORD")

#Login to spond
driver.get(spond_login)
time.sleep(2)
email_field = driver.find_element(by="name", value="emailOrPhoneNumber")
email_field.send_keys(my_email)
password_field = driver.find_element(by="name", value="password")
password_field.send_keys(my_password)
submit = driver.find_element(by="xpath", value="/html/body/root/app-login/div/div[2]/section[1]/div[2]/form/spinner-button/button")
submit.click()
time.sleep(2)

#Get today's date
today = dt.datetime.today().date()
# will need to change this to 7 days
seven_days = dt.timedelta(days=7)
one_week_from_today = (today + seven_days).strftime(f"%A, %-d %b at 11:00")
print(one_week_from_today)

#Get dates for badminton sessions
spond_dates = driver.find_elements(by="css selector", value=".spondCardstyled__EventStartTime-sc-1adg5oi-22")
#Retrieves text of badminton dates, storing it into a list
badminton_dates = [spond_date.get_attribute('innerHTML') for spond_date in spond_dates]
print(badminton_dates)

# Check if there is a session that is one week from today and book session
for badminton_date in badminton_dates:
    if one_week_from_today == badminton_date:
        print("There is a session in exactly two weeks from today")
        #Find an element by it's text value using xpath
        #Click the date of the session one week from today
        date_button = driver.find_element(by="xpath", value=f"//*[contains(text(), '{badminton_date}')]")
        date_button.click()
        time.sleep(1)
        while True:
            try:
                accept_button = driver.find_element(by="name", value="accept-button")
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