from selenium import webdriver # type: ignore
from selenium.webdriver.chrome.service import Service # type: ignore
from selenium.webdriver.chrome.options import Options # type: ignore
from selenium.webdriver.common.by import By # type: ignore
from selenium.webdriver.support.ui import Select # type: ignore
import time

options = Options()
options.add_argument("--headless")  
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

service = Service("/usr/bin/chromedriver")

driver = webdriver.Chrome(service=service, options=options)

url = "https://www.bseindia.com/stock-share-price/ltimindtree-ltd/ltim/540005/corp-announcements/"
driver.get(url)

x = driver.find_element(By.XPATH, '//*[@id="ddlPeriod"]')
drop = Select(x)
time.sleep(5)

drop.select_by_visible_text(input("Enter Category: "))  # take this from input 
time.sleep(1)

y = driver.find_element(By.XPATH, '//*[@id="ddlsubcat"]')
drop = Select(y)
drop.select_by_visible_text(input("Enter Category: "))  # take this from input 
time.sleep(2)

btn = driver.find_element(By.XPATH, '//*[@id="btnSubmit"]')
btn.click()

time.sleep(3)
text = driver.find_element(By.XPATH, '//*[@id="deribody"]/div[1]/div[3]')

print("Text content:", text.text)

driver.quit()
