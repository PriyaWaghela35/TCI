from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException, TimeoutException

import time
data =[]
service = Service("C:\\Users\\tci\Documents\\1Task\\chromedriver-win64\\chromedriver.exe")
driver = webdriver.Chrome(service=service)

url = "https://www.bseindia.com/stock-share-price/ltimindtree-ltd/ltim/540005/corp-announcements/"
driver.get(url)

# time.sleep(10)
# text = driver.find_element(By.XPATH, '//*[@id="ddlPeriod"]')
# data = text.text
# print("Text content:", data)

x = driver.find_element(By.XPATH, '//*[@id="ddlPeriod"]')
drop = Select(x)
time.sleep(5)

drop.select_by_visible_text("Board Meeting")  # take this from input 
time.sleep(1)

y = driver.find_element(By.XPATH, '//*[@id="ddlsubcat"]')
drop = Select(y)
drop.select_by_visible_text("Board Meeting")  # take this from input 
time.sleep(2)

btn = driver.find_element(By.XPATH, '//*[@id="btnSubmit"]')
btn.click()
time.sleep(1)


text = driver.find_element(By.XPATH, '//*[@id="lblann"]/table/tbody')
data = text.text
print("Text content:", data)

driver.quit()