import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select  # 下拉式選單使用
from selenium.common.exceptions import NoSuchElementException # Handle exception
from ocr_component import get_captcha_code

# 越過反爬蟲
options = webdriver.ChromeOptions()  # 創立 driver物件所需的參數物件
options.add_argument("--disable-blink-features=AutomationControlled")
driver = webdriver.Chrome(options=options)

# driver = webdriver.Chrome() # 無須越過反爬蟲的話直接從這行開始
driver.get("https://irs.thsrc.com.tw/IMINT/")

# cookie
accept_cookie_button = driver.find_element(By.ID, "cookieAccpetBtn")
accept_cookie_button.click()

# 找到下拉選單元素
dropdown_star = driver.find_element(By.NAME, "selectStartStation")
select = Select(dropdown_star)
select.select_by_visible_text("台中")  # 方法 1：透過可見文字選擇 選擇台北

dropdown_dest = driver.find_element(By.NAME, "selectDestinationStation")
select = Select(dropdown_dest)
select.select_by_visible_text("板橋")

dropdown_time = driver.find_element(By.NAME, "toTimeTable")
select = Select(dropdown_time)
select.select_by_visible_text("08:00")

# 點擊日期輸入框，打開日曆選擇器
date_input = driver.find_element(By.XPATH, "//input[@class='uk-input' and @readonly='readonly']")
date_input.click()  # 點擊，打開日期選擇器
time.sleep(1)  # 等待日曆展開
# 找到並點擊 "2025 年 3 月 1 日"
star_date = '三月 1, 2025'
date_element = driver.find_element(By.XPATH, f"//span[@class='flatpickr-day' and @aria-label='{star_date}']")
date_element.click()

while True:
    # captcha
    captcha_img = driver.find_element(
        By.ID, 'BookingS1Form_homeCaptcha_passCode')
    captcha_img.screenshot('captcha.png')
    captcha_code = get_captcha_code()
    captcha_input = driver.find_element(By.ID, 'securityCode')
    captcha_input.send_keys(1234)
    time.sleep(2)

    # submit
    driver.find_element(By.ID, 'SubmitButton').click()
    time.sleep(5)

    # check validation is success or not
    try:
        # driver.find_element(By.CLASS_NAME, 'uk-alert-danger uk-alert')
        driver.find_element(By.ID, 'divErrMSG')
    except NoSuchElementException:
        print("進到第二步驟")
        break


time.sleep(2000)
driver.quit()