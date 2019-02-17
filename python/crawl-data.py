# coding:utf-8
from selenium import webdriver
import time


def get_days(month):
    global driver
    option = webdriver.ChromeOptions()
    option.add_argument("disable-infobars")
    option.add_argument("--headless")
    driver = webdriver.Chrome(chrome_options=option)
    url = "https://www.aqistudy.cn/historydata/daydata.php?city=南昌&month={0}".format(month)
    driver.get(url)
    tr_list = []
    start = time.time()
    while len(tr_list) <= 1:
        tr_list = driver.find_elements_by_tag_name('tr')
        if time.time() - start > 10:
            break
    month = []
    for tr in tr_list[1:]:
        day = [td.text.encode('utf-8') for td in tr.find_elements_by_tag_name("td")]
        month.append(",".join(day))
    driver.close()
    driver.quit()
    return "\n".join(month)

