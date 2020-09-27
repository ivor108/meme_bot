from selenium import webdriver
import os
from config import *
import time
import psycopg2

chrome_options = webdriver.ChromeOptions()
chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--no-sandbox")
driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)

conn = psycopg2.connect(os.environ.get("DATABASE_URL"), sslmode='require')
cur = conn.cursor()

def get_text_excluding_children(driver, element):
    return driver.execute_script("""
    var parent = arguments[0];
    var child = parent.firstChild;
    var ret = "";
    while(child) {
        if (child.nodeType === Node.TEXT_NODE)
            ret += child.textContent;
        child = child.nextSibling;
    }
    return ret;
    """, element)

def get_memes():
    driver.get('https://www.reddit.com/r/memes/new/')
    memes = []
    memes_text = []
    time.sleep(10)
    elements = driver.find_elements_by_class_name('_1poyrkZ7g36PawDueRza-J')

    for element in elements:
        child = element.find_element_by_class_name('_3Oa0THmZ3f5iZXAQ0hBJ0k ')
        mem = str(child.find_element_by_tag_name('img').get_attribute('src'))
        text = get_text_excluding_children(driver, element.find_element_by_tag_name('h3'))
        if mem.count('external') == 0:
            memes.append(mem)
            memes_text.append(text)
            cur.execute("INSERT INTO memes(meme_text, meme_img, add_time) VALUES(%s, %s, date_trunc('hour', CURRENT_TIMESTAMP));", (text, mem))
            conn.commit()



    print(memes)
    print("------------img: " + str(len(memes)))
    print(memes_text)
    print("-----------text: " + str(len(memes_text)))
    return memes

def get_random_meme():
    conn = psycopg2.connect(os.environ.get("DATABASE_URL"), sslmode='require')
    cur = conn.cursor()
    cur.execute("SELECT meme_text, meme_img FROM memes OFFSET floor(random()*(SELECT COUNT(*) FROM memes)) LIMIT 1;")
    conn.commit()
    return cur.fetchone()