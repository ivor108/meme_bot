
from selenium import webdriver



def parsers(heroes):
    elem_text = []
    elem_text2 = []
    heroes = heroes.lower()
    driver = webdriver.Firefox(executable_path=r'/usr/local/bin/geckodriver')
    driver.get("https://ru.dotabuff.com/heroes/" + heroes)
    elem_count = driver.find_elements_by_xpath("//div[@class = 'col-8']/section")

    if len(elem_count) == 7:

        elem = driver.find_element_by_xpath("//div[@class = 'col-8']/section[6]").find_elements_by_tag_name('tr')
        elem2 = driver.find_element_by_xpath("//div[@class = 'col-8']/section[7]").find_elements_by_tag_name('tr')
    else:
        elem = driver.find_element_by_xpath("//div[@class = 'col-8']/section[5]").find_elements_by_tag_name('tr')
        elem2 = driver.find_element_by_xpath("//div[@class = 'col-8']/section[6]").find_elements_by_tag_name('tr')


    elem.pop(0)
    elem2.pop(0)

    for elemens in elem:
        elem_cell = []
        for j in elemens.find_elements_by_tag_name('td'):
            elem_cell.append(j.text)
        del elem_cell[0]
        elem_text.append(elem_cell)

    for elemens in elem2:
        elem_cell = []
        for j in elemens.find_elements_by_tag_name('td'):
            elem_cell.append(j.text)
        del elem_cell[0]
        elem_text2.append(elem_cell)
    driver.close()
    return elem_text, elem_text2


