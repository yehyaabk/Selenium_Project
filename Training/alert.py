from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import random
import time

DURATION = 1

options= webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=options)

url="https://demoqa.com/alerts"
time.sleep(2)
driver.get(url)
time.sleep(DURATION)
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "button#alertButton.btn")))

alert_button =  driver.find_element(By.CSS_SELECTOR, "button#alertButton.btn")
alert_button.click()
first_alert = driver.switch_to.alert
time.sleep(DURATION)
first_alert.accept()
time.sleep(DURATION)


timer_alert_button= driver.find_element(By.ID, "timerAlertButton")
timer_alert_button.click()
WebDriverWait(driver, 10).until(
    EC.alert_is_present()
)
time.sleep(DURATION)
second_alert= driver.switch_to.alert
second_alert.accept()
time.sleep(DURATION)

confirm_button = driver.find_element(By.ID, "confirmButton")
confirm_button.click()
third_alert = driver.switch_to.alert
time.sleep(DURATION)
actions=[third_alert.accept, third_alert.dismiss]
chosen = random.choice(actions)
chosen()
time.sleep(DURATION)

prompt_Button= driver.find_element(By.ID, "promtButton")
prompt_Button.click()
time.sleep(DURATION)
alert= driver.switch_to.alert
alert.send_keys("yehya")
time.sleep(DURATION)
alert.accept()















