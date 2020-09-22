from selenium import webdriver
import os
import time
from config import *
import psycopg2

chrome_options = webdriver.ChromeOptions()
chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--no-sandbox")
driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)
driver.get(URL)

conn = psycopg2.connect(os.environ.get("DATABASE_URL"), sslmode='require')
cur = conn.cursor()

def get_memes():
    memes = []
    SCROLL_PAUSE_TIME = 0.5

    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(SCROLL_PAUSE_TIME)
        if len(memes) >= 100:
            break

        elements = driver.find_elements_by_class_name('_2_tDEnGMLxpM6uOa2kaDB3._1XWObl-3b9tPy64oaG6fax')

        for element in elements:
            if len(memes) >= 100:
                break
            mem = element.get_attribute('src')
            if str(mem).count('external') == 0:
                memes.append(str(mem))

    print(memes)
    print("--------------" + str(len(memes)))
    return memes