from selenium import webdriver
from selenium.common import NoSuchElementException
import time
import datetime as dt
import os

chrome_driver_path = "/Users/denisechan/Development/chromedriver"
driver = webdriver.Chrome(executable_path=chrome_driver_path)
spond_login = "https://spond.com/landing/login/"
my_email = os.environ.get("MY_EMAIL")
my_password = os.environ.get("MY_PASSWORD")

#Login to spond
driver.get(spond_login)
time.sleep(5)
email_field = driver.find_element(by="name", value="emailOrPhoneNumber")
email_field.send_keys(my_email)
password_field = driver.find_element(by="name", value="password")
password_field.send_keys(my_password)
submit = driver.find_element(by="xpath", value="/html/body/root/app-login/div/div[2]/section[1]/div[2]/form/spinner-button/button")
submit.click()
time.sleep(5)

#Get today's date
today = dt.datetime.today().date()
fourteen_days = dt.timedelta(days=14)
two_weeks_from_today = (today + fourteen_days).strftime(f"%A, %-d %b at 11:00")
print(two_weeks_from_today)

#Get dates for badminton sessions
spond_dates = driver.find_elements(by="css selector", value=".spondCardstyled__EventStartTime-sc-1adg5oi-22")
badminton_dates = [spond_date.get_attribute('innerHTML') for spond_date in spond_dates]
print(badminton_dates)

# Check if there is a session that is two weeks from today and book session
for badminton_date in badminton_dates:
    if two_weeks_from_today == badminton_date:
        print("There is a session in exactly two weeks from today")
        #Find an element by it's text value using xpath
        #Click the date of the session two weeks from today
        date_button = driver.find_element(by="xpath", value=f"//*[contains(text(), '{badminton_date}')]")
        date_button.click()
        time.sleep(5)
        while True:
            try:
                accept_button = driver.find_element(by="name", value="accept-button")
            except NoSuchElementException:
                pass
            else:
                accept_button.click()
                time.sleep(5)
                break
    else:
        pass

driver.quit()






