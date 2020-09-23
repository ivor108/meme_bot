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

    '''
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(SCROLL_PAUSE_TIME)
        if len(memes) >= 100:
            break

        elements = driver.find_elements_by_class_name('_2_tDEnGMLxpM6uOa2kaDB3._1XWObl-3b9tPy64oaG6fax')

        for element in elements:
            if len(memes) >= 100:
                break
            mem = str(element.get_attribute('src'))
            if mem.count('external') == 0:
                memes.append(mem)
                if cur.execute("SELECT COUNT(*) FROM memes WHERE meme_img = %s;", (mem,)) == 0:
                    cur.execute("INSERT INTO memes(meme_img) VALUES(%s);", (mem,))
                    print('Строка добавлена!')
                print('Такая строка уже существует!')
    '''

    elements = driver.find_elements_by_class_name('_2_tDEnGMLxpM6uOa2kaDB3._1XWObl-3b9tPy64oaG6fax')

    for element in elements:
        if len(memes) >= 100:
            break
        mem = str(element.get_attribute('src'))
        if mem.count('external') == 0:
            memes.append(mem)
            if cur.execute("SELECT COUNT(*) FROM memes WHERE meme_img = %s;", (mem,)) == 0:
                cur.execute("INSERT INTO memes(meme_img) VALUES(%s);", (mem,))
                print('Строка добавлена!')
            print('Такая строка уже существует!')

    print(memes)
    print("--------------" + str(len(memes)))
    conn.commit()
    return memes

def get_random_meme():
    conn = psycopg2.connect(os.environ.get("DATABASE_URL"), sslmode='require')
    cur = conn.cursor()
    cur.execute("SELECT meme_img FROM memes OFFSET floor(random()*(SELECT COUNT(*) FROM memes)) LIMIT 1;")
    #cur.execute("SELECT COUNT(*) FROM memes;")
    conn.commit()
    return str(cur.fetchone()[0])
