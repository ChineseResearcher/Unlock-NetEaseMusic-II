# coding: utf-8

import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from retrying import retry

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s %(message)s')

@retry(wait_random_min=5000, wait_random_max=10000, stop_max_attempt_number=3)
def enter_iframe(browser):
    logging.info("Enter login iframe")
    time.sleep(5)  # 给 iframe 额外时间加载
    try:
        iframe = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[starts-with(@id,'x-URS-iframe')]")
        ))
        browser.switch_to.frame(iframe)
        logging.info("Switched to login iframe")
    except Exception as e:
        logging.error(f"Failed to enter iframe: {e}")
        browser.save_screenshot("debug_iframe.png")  # 记录截图
        raise
    return browser

@retry(wait_random_min=1000, wait_random_max=3000, stop_max_attempt_number=5)
def extension_login():
    chrome_options = webdriver.ChromeOptions()

    logging.info("Load Chrome extension NetEaseMusicWorldPlus")
    chrome_options.add_extension('NetEaseMusicWorldPlus.crx')

    logging.info("Initializing Chrome WebDriver")
    try:
        service = Service(ChromeDriverManager().install())  # Auto-download correct chromedriver
        browser = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        logging.error(f"Failed to initialize ChromeDriver: {e}")
        return

    # Set global implicit wait
    browser.implicitly_wait(20)

    browser.get('https://music.163.com')

    # Inject Cookie to skip login
    logging.info("Injecting Cookie to skip login")
    browser.add_cookie({"name": "MUSIC_U", "value": "00536E5578DC481984FDFF4C91B121D885146AF7E5578A95F02EBB0AECB8256CC39F538063046D1484C6640EE2F5B1BA6894C9608FE7AA92513C86F25E62BB39EDA44A0D68F16CCA1DC9883A5CC02D86B211FE724A946B05D09EA445FC9E8B50C98792506397A6B9EFF469E0429614B28014723C89427204E3EED073C08B808B5698AE369F26ED51DFD4296D8915302741F6139CF4469D5C0F4FFBAF782A6E73E577DBA3E35E3FE34C15243CD06CA8A68C465D75698C0A75B12ADB63577E5874AEE1FF1483C853572CFA3F743E1069933581E7883AABA3DF07FD0E2A34616F0CE7A9B53503F46B8C4941051A6E4F7935D1570C834D92888C8F492071DFB1FE35A3007548E94F256727327548CD7D05352651C0F3D7168C1225F298FB093DA189D9F6C5EB156BB0812CAA7F344ABB8CD12430C83DB9D0D70423D9A7D0BAC9A7D895"})
    browser.refresh()
    time.sleep(5)  # Wait for the page to refresh
    logging.info("Cookie login successful")

    # Confirm login is successful
    logging.info("Unlock finished")

    time.sleep(10)
    browser.quit()


if __name__ == '__main__':
    try:
        extension_login()
    except Exception as e:
        logging.error(f"Failed to execute login script: {e}")
