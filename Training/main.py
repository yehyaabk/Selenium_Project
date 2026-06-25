from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

options= webdriver.ChromeOptions()
options.add_experimental_option("detach", True)


driver =  webdriver.Chrome(options=options)
url=r"https://demoqa.com/buttons"
driver.implicitly_wait(10)

driver.get(url)

double_click_button = driver.find_element(By.ID, "doubleClickBtn")
print(dir(double_click_button))
double_click_button.click()
ActionChains(driver).double_click(double_click_button).perform()



