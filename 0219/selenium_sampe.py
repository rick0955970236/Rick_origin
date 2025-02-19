import time
from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()
# driver = webdriver.Firefox()
# driver = webdriver.Edge()
# driver = webdriver.Safari()

driver.get("https://www.selenium.dev/selenium/web/web-form.html")

title = driver.title

driver.implicitly_wait(0.5)
# text_box = soup.find(name='my-text') # bs4的寫法
text_box = driver.find_element(by=By.NAME, value="my-text")
# submit_button
submit_button = driver.find_element(by=By.TAG_NAME, value="button")
submit_button = driver.find_element(by=By.CSS_SELECTOR, value="button")

# Step 6:
text_box.send_keys("XXXXXXXXXX")
time.sleep(5)
submit_button.click()

time.sleep(10)
driver.quit()
