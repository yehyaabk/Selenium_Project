from selenium  import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui  import WebDriverWait
from selenium.webdriver.support  import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import time
from selenium.common.exceptions import  TimeoutException

DURATION = 1

url="https://demoqa.com/automation-practice-form"
picture_path= r"C:\Users\DELL\Desktop\image.jfif"

options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=options)

driver.get(url)

WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "input#firstName" ))
)

first_name = driver.find_element(By.CSS_SELECTOR, "input#firstName")
first_name.send_keys("yehya")
time.sleep(DURATION)

last_name = driver.find_element(By.CSS_SELECTOR, "input#lastName")
last_name.send_keys("ABOU KHECHFE")
time.sleep(DURATION)

email = driver.find_element(By.ID, "userEmail")
email.send_keys("yehya@gmail.com")
time.sleep(DURATION)

gender = driver.find_element(By.CSS_SELECTOR, "input#gender-radio-1.form-check-input")
gender.click()
time.sleep(DURATION)

number = driver.find_element(By.CSS_SELECTOR, "input#userNumber")
number.send_keys("0123456789")
time.sleep(DURATION)

date_input = driver.find_element(By.ID, "dateOfBirthInput")
date_input.click()
time.sleep(DURATION)

WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "div.react-datepicker__month-container"))
)

month_dropdown = driver.find_element(By.CSS_SELECTOR, "select.react-datepicker__month-select")
select = Select(month_dropdown)
select.select_by_index(8)
time.sleep(DURATION)

year_dropdown = driver.find_element(By.CSS_SELECTOR, "select.react-datepicker__year-select")
select = Select(year_dropdown)
select.select_by_visible_text("1998")
time.sleep(DURATION)

day = driver.find_element(By.CSS_SELECTOR, "div.react-datepicker__day.react-datepicker__day--012")
day.click()


picture = driver.find_element(By.CSS_SELECTOR, 'input[label="Select picture"]')
picture.send_keys(picture_path)
time.sleep(DURATION)

state_input = driver.find_element(By.ID, "react-select-3-input")
state_input.click()
time.sleep(DURATION)
state_input.send_keys(Keys.ARROW_DOWN)
time.sleep(DURATION)
state_input.send_keys(Keys.ARROW_DOWN)
time.sleep(DURATION)
state_input.send_keys(Keys.ENTER)
time.sleep(DURATION)

city_input = driver.find_element(By.ID, "react-select-4-input")
city_input.click()
city_input.send_keys(Keys.ENTER)

time.sleep(DURATION)

submit_button = driver.find_element(By.ID, "submit")
submit_button.click()

try:
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "div.modal-dialog.modal-lg"))
    )
    print("Form is Submitted")
except TimeoutException:
    print("Form is not Submitted")







