from selenium import webdriver
import os

chrome_options = webdriver.ChromeOptions()
chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--no-sandbox")
driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)

def get_best_wors_picks(hero):
    elem_text = []
    elem_text2 = []
    hero = hero.lower()

    driver.get("https://ru.dotabuff.com/heroes/" + hero)
    elem_count = driver.find_elements_by_xpath("//div[@class = 'col-8']/section")
    if len(elem_count) == 7:
        elem = driver.find_element_by_xpath("//div[@class = 'col-8']/section[6]").find_elements_by_tag_name('tr')
        elem2 = driver.find_element_by_xpath("//div[@class = 'col-8']/section[7]").find_elements_by_tag_name('tr')
    else:
        elem = driver.find_element_by_xpath("//div[@class = 'col-8']/section[5]").find_elements_by_tag_name('tr')
        elem2 = driver.find_element_by_xpath("//div[@class = 'col-8']/section[6]").find_elements_by_tag_name('tr')


    elem.pop(0)
    elem2.pop(0)

    for element in elem:
        elem_cell = []
        for j in element.find_elements_by_tag_name('td'):
            elem_cell.append(j.text)
        del elem_cell[0]
        elem_text.append(elem_cell)

    for element in elem2:
        elem_cell = []
        for j in element.find_elements_by_tag_name('td'):
            elem_cell.append(j.text)
        del elem_cell[0]
        elem_text2.append(elem_cell)

    elem_text.insert(0, ["Герой", "Преимущество", "ДоляПобед", "Матчи"])
    elem_text2.insert(0, ["Герой", "Невыгодное положение", "Доля Побед", "Матчи"])
    return elem_text, elem_text2

def create_dota_keybord(keyboard):
    with open('heroes.txt') as f:
        thelist = f.readlines()
    i = 0
    tmp = []
    for hero in thelist:
        tmp.append(hero.replace('\n', ''))
        if i%8 == 7 or i == len(thelist)-1:
            if len(tmp) == 8:
                keyboard.row(tmp[0], tmp[1], tmp[2], tmp[3], tmp[4], tmp[5], tmp[6], tmp[7])
            else:
                keyboard.row(tmp[0], tmp[1], tmp[2], tmp[3], tmp[4], tmp[5], tmp[6])
            tmp = []
        i+=1
