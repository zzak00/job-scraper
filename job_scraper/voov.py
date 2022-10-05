# selenium 4
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import random
from selenium.webdriver.chrome.options import Options
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)

id_meet = "672 4623 3849"
user = "F20110209Asmae"
pwd = "Azertya123"
phone = "659459721"
url = "https://voovmeeting.com/phone-login.html?redirect_link=%2Fr&redirect_type=3"
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)
driver.get(url)
time.sleep(random.randint(1,3))
driver.find_element(by=By.XPATH, value='//*[@id="phone-num"]').send_keys(phone)
time.sleep(random.randint(1,3))
driver.find_element(by=By.XPATH, value='//*[@id="password"]').send_keys(pwd)
time.sleep(random.randint(1,3))
driver.find_element(by=By.XPATH, value='//*[@id="contentCtrl"]/div[1]/div[2]/div[3]/button').click()
# time to switch btw login/meet
time.sleep(40)
driver.find_element(by=By.XPATH, value='//*[@id="root"]/div/div[2]/div[1]/input').send_keys(id_meet)
time.sleep(random.randint(1,3))
driver.find_element(by=By.XPATH, value='//*[@id="root"]/div/div[2]/button').click()
# meeting duration
time.sleep(10) 
driver.find_element(by=By.XPATH, value='//*[@id="root"]/section/footer/div/div[5]/button').click()
time.sleep(random.randint(1,3))
driver.find_element(by=By.XPATH, value='//*[@id="tea-overlay-root"]/div/div[3]/div/div/div[2]/button[2]').click()
