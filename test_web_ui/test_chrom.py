from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
import time
import traceback
from ui_operation import UiOperation


def test_dms_login():
    chromedriver_path = r"D:\tuchuan\tools\chromedriver-win64\chromedriver.exe"
    chrome_options = Options()
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    # 忽略SSL证书错误（因为使用的是IP地址的HTTPS）
    chrome_options.add_argument("--ignore-certificate-errors")
    chrome_options.add_argument("--ignore-ssl-errors")
    chrome_options.add_argument("--allow-running-insecure-content")
    driver = webdriver.Chrome(
        service=Service(executable_path=chromedriver_path),
        options=chrome_options)
    driver.get("https://192.168.6.66:13636/toLogin.do")

    wait = WebDriverWait(driver, 10)
    username_input = wait.until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="uname"]')))
    username_input.send_keys("admin")
    username_input = wait.until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="pwd"]')))
    username_input.send_keys("pwd")
    username_input = wait.until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="vldCode"]')))
    username_input.send_keys("123")
    username_input = wait.until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="loginin"]')))
    username_input.submit()
    return driver


if __name__ == "__main__":
    ui_op = UiOperation(test_dms_login())
    ui_op.open_配置管理()
    ui_op.open_业务配置()
    ui_op.open_xForce配置()
    ui_op.open_xForce配置_基本配置()
    xForce_state = ui_op.xForce基本配置_强制解析功能模块开关_状态()
    if '开启' in xForce_state:
        ui_op.xForce基本配置_强制解析功能模块开关()
    ui_op.xForce基本配置_强制解析功能模块开关()
    print(ui_op.xForce基本配置_强制解析功能模块开关_状态())
    time.sleep(5)
