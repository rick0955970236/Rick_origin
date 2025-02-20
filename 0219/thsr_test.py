import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select  # 下拉式選單使用
from selenium.common.exceptions import NoSuchElementException # Handle exception
from ocr_component import get_captcha_code
from collections import defaultdict

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
select.select_by_visible_text("台中")  # 方法 1：透過可見文字選擇 選擇台中

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
date_element = driver.find_element(By.XPATH,
                                f"//span[@class='flatpickr-day' and @aria-label='{star_date}']")
date_element.click()

while True:
    # captcha
    captcha_img = driver.find_element(
        By.ID, 'BookingS1Form_homeCaptcha_passCode')
    captcha_img.screenshot('captcha.png')
    captcha_code = get_captcha_code()
    captcha_input = driver.find_element(By.ID, 'securityCode')
    captcha_input.send_keys(captcha_code)
    time.sleep(2)

    # submit
    driver.find_element(By.ID, 'SubmitButton').click()

    # check validation is success or not
    try:
        time.sleep(5)
        driver.find_element(By.ID, 'BookingS2Form_TrainQueryDataViewPanel')
        print("驗證碼正確, 進到第二步驟")
        break
    except NoSuchElementException:
        print("驗證碼錯誤，重新驗證")


### 第二步 ###

trains_info = [] # 儲存所有車次資訊
# 找到所有列車選項
trains = driver.find_element(By.CLASS_NAME, 'result-listing').find_elements(By.TAG_NAME, 'label')

# 遍歷所有列車選項
for train in trains:
    info = train.find_element(By.CLASS_NAME, 'uk-radio')  # 單選按鈕 (radio)

    # 提取車次資訊
    train_data = {
        'depart_time': info.get_attribute('querydeparture'),  # 出發時間
        'arrival_time': info.get_attribute('queryarrival'),  # 到達時間
        'duration': info.get_attribute('queryestimatedtime'),  # 行駛時間
        'train_code': info.get_attribute('querycode'),  # 車次編號
        'radio_box': info  # 單選按鈕元素
    }
    trains_info.append(train_data)

# **輸出所有車次資訊**
print("\n🚆 可選擇的列車：")
for idx, train in enumerate(trains_info):
    print(f"({idx}) - 車次 {train['train_code']} | 行駛時間={train['duration']} \
    | {train['depart_time']} ➝ {train['arrival_time']}")

# **請使用者選擇列車**
while True:
    try:
        which_train = int(input("\n請選擇列車,輸入 0~9:\n"))
        if 0 <= which_train < len(trains_info):  # 確保輸入在範圍內
            break
        else:
            print("❌ 輸入超出範圍，請重新輸入！")
    except ValueError:
        print("❌ 無效輸入，請輸入數字！")

# **點擊選擇的列車**
trains_info[which_train]['radio_box'].click()
print(f"\n✅ 已選擇車次 {trains_info[which_train]['train_code']},\
出發時間 {trains_info[which_train]['depart_time']}")

# Submit booking requests
driver.find_element(By.NAME, 'SubmitButton').click()
print("選擇車次完成, 進到第三步驟")


## 第三步驟 ##

# Check booking infomation for user
driver.find_element(
    By.CLASS_NAME, 'ticket-summary').screenshot('thsr_summary.png')

# Enter personal detail
input_personal_id = driver.find_element(By.ID, 'idNumber')
# personal_id = input("請輸入身分證字號:\n")
personal_id = os.getenv('FORPYTHON_PERSONAL_ID') # 系統中'環境變數'的KEY 要去系統設定 目前先亂填
input_personal_id.send_keys(personal_id)

input_phone_number = driver.find_element(By.ID, 'mobilePhone')
# phone_number = input("請輸入手機號碼:\n")
phone_number = os.getenv('FORPYTHON_PHONE_NUMBER')
input_phone_number.send_keys(phone_number)

input_email = driver.find_element(By.ID, 'email')
# email = input("請輸入Email:\n")
email = os.getenv('FORPYTHON_EMAIL')
input_email.send_keys(email)

# Final Check
driver.find_element(By.NAME, 'agree').click()  # 接受使用者個資條款
driver.find_element(By.ID, 'isSubmit').click()  # 送出表單


# Save booking result
driver.find_element(
    By.CLASS_NAME, 'ticket-summary').screenshot('thsr_booking_result.png')
print("訂票完成!")

time.sleep(200)
driver.quit()