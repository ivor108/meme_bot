from selenium import webdriver
import os
from config import *

chrome_options = webdriver.ChromeOptions()
chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--no-sandbox")
driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)


def get_memes():
    driver.get(URL)
    memes = []
    memes_text = []
    elements = driver.find_elements_by_class_name('_2_tDEnGMLxpM6uOa2kaDB3._1XWObl-3b9tPy64oaG6fax')
    elements2 = driver.find_elements_by_class_name('_eYtD2XCVieq6emjKBH3m')
    while len(memes) < 25:
        for element in elements:
            mem = str(element.get_attribute('src'))
            if mem.count('external') == 0:
                memes.append(mem)
    while len(memes_text) < 25:
        for element in elements2:
            memes_text.append(str(element.text))


    print(memes)
    print("------------img: " + str(len(memes)))
    print(memes_text)
    print("-----------text: " + str(len(memes_text)))
    return memes

