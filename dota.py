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
    try:
        driver.get("https://ru.dotabuff.com/heroes/" + hero)
    except:
        return 'Не правильное имя героя'
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


