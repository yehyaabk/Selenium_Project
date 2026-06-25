from selenium import webdriver
from selenium.webdriver.common.by import By



options= webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=options)

url="https://demoqa.com/dynamic-properties"
driver.implicitly_wait(5)
driver.get(url)

element = driver.find_element(By.CSS_SELECTOR, "button#colorChange.text-danger.btn.btn-primary.mt-4")
print("element found !")



