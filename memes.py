from selenium import webdriver
import os
import time
from config import *

chrome_options = webdriver.ChromeOptions()
chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--no-sandbox")
driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)
driver.get(URL)

def get_memes():
    memes = []
    SCROLL_PAUSE_TIME = 0.5
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)
        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    elements = driver.find_elements_by_class_name('_2_tDEnGMLxpM6uOa2kaDB3._1XWObl-3b9tPy64oaG6fax')

    for element in elements:
        mem = element.get_attribute('src')
        if str(mem).count('external') == 0:
            memes.append(str(mem))

    print(memes)
    print("--------------" + len(memes))
    return memes