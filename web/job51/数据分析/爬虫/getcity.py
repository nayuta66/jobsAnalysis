#!/usr/bin/env python
# coding: utf-8
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import json


def getCity():
    # 设置selenium使用chrome的无头模式
    chrome_options = Options()
    # chrome_options.add_argument("headless")

    browser = webdriver.Chrome(options=chrome_options, executable_path=r'C:\Pycharm\chromedriver')
    browser.get_cookies()
    browser.get('https://www.51job.com/')

    # 找到城市选择框,并模拟点击
    button = browser.find_element_by_xpath("//div[@class='ush top_wrap']//div[@class='el on']/p\
        [@class='addbut']//input[@id='work_position_input']").click()

    # 选中城市弹出框
    browser.current_window_handle

    # 定义一个空字典
    dic = {}

    # 找到城市,和对应的城市编号
    find_city_elements = browser.find_elements_by_xpath("//div[@id='work_position_layer']//\
        div[@id='work_position_click_center_right_list_000000']//tbody/tr/td")
    for element in find_city_elements:
        number = element.find_element_by_xpath("./em").get_attribute("data-value")  # 城市编号
        city = element.find_element_by_xpath("./em").text  # 城市
        # 添加到字典
        dic.setdefault(city, number)
    # 写入文件
    with open('city.json', 'w', encoding='utf8') as f:
        f.write(json.dumps(dic, ensure_ascii=False))
    print("city.json文件创建完毕")
    browser.quit()


if __name__ == '__main__':
    getCity()
