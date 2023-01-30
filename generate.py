import time
import yaml
import random
import json

from yaml import SafeLoader
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver

# yml
def getconfigdata():
    with open('config.yml', 'r', encoding="utf8") as f:
        data = yaml.load(f, Loader=SafeLoader)
        config = {
            'mail': data['mail'],
            'pw': data['password'],
            'data': data['data'],
            'ln': data['lastname'],
            'fn': data['firstname'],
            'shm': data['surfsharkmail'],
            'shpw': data['surfsharkpassword'],
        }
    return config

def plusdata():
    # data +1
    with open('config.yml', 'r', encoding="utf8") as f:
        data = yaml.load(f, Loader=SafeLoader)
    data['data'] += 1
    with open('config.yml', 'w', encoding="utf8") as f:
        yaml.dump(data, f)

def generator(config):
    # headless mode
    options = webdriver.ChromeOptions()
    # options.add_argument('--headless')
    # surfshark VPN
    options.add_extension('3.18.1_0.crx')
    # 創建一個 Chrome 瀏覽器物件
    driver = webdriver.Chrome(chrome_options=options)
    # 開啟註冊頁面
    driver.get("chrome-extension://ailoabdmgclmfmhdagmlohpjlbpffblp/index.html")
    driver.switch_to.window(driver.window_handles[1])

    # surfshark VPN
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "email"))).send_keys(config.get("shm"))
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "password"))).send_keys(config.get("shpw"))
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "button[data-test='login-in-button']"))).click()
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "button[data-test='cw-quickConnect-button']"))).click()
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "button[data-test='cw-pauseVpn-button']")))

    # microsoft
    driver.get("https://signup.live.com/signup")

    # mail
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "liveSwitch"))).click()
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "MemberName"))).send_keys(f'{config.get("mail")}{config.get("data")}')
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "iSignupAction"))).click()

    # enter password
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "PasswordInput"))).send_keys(f'{config.get("pw")}')
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "iSignupAction"))).click()

    # enter name
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "LastName"))).send_keys(f'{config.get("ln")}')
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "FirstName"))).send_keys(f'{config.get("fn")}')
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "iSignupAction"))).click()

    # gen birth
    birth = random.randint(1950, 2000)
    month = random.randint(1, 12)
    day = random.randint(1, 28)

    # birth
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "BirthYear"))).send_keys(birth)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "BirthMonth"))).send_keys(month)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "BirthDay"))).send_keys(day)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "iSignupAction"))).click()

    # Verify
    # Verify
    # Verify

    #Check verify successful
    WebDriverWait(driver, 20000).until(EC.visibility_of_element_located((By.ID, "idSIButton9"))).click()
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "microsoft_container")))

    # get account detail
    info_data = {"username": config.get("mail") + str(config.get("data")) + "@outlook.com", "password": config.get("pw")}
    json_data = json.dumps(info_data)

    # output to accounts.txt
    with open("accounts.txt", "a") as f:
        f.write(json_data + ',\n')
    print(f'{config.get("mail") + str(config.get("data")) + "@outlook.com"} create successful and register in accounts.txt!')

    # exit
    time.sleep(2)
    driver.quit()

while True:
    try:
        config = getconfigdata()
        generator(config)
        plusdata()
    except:
        print('Something went wrong... retrying!')