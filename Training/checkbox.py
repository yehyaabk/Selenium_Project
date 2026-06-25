from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains


options= webdriver.ChromeOptions()
options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=options)
url="https://demoqa.com/radio-button"

driver.implicitly_wait(10)

driver.get(url)

radio_button= driver.find_element(By.ID, "yesRadio")

radio_button.click()
