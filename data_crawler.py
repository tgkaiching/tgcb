from bs4 import BeautifulSoup
from chatterbot import ChatBot
from selenium import webdriver
import re
import json

USERNAME = "KC_SUEN"
PASSWORD = "Y5837810y!"

LOGIN_URL = "https://www.tgwiki.com/CookieAuth.dll?GetLogon?curl=Z2F&reason=0&formdir=9"

def get_HTML_From_URL():
    browser = webdriver.Chrome()
    browser.get(LOGIN_URL)
    username = browser.find_element_by_id('username')
    username.send_keys(USERNAME)
    password = browser.find_element_by_id('password')
    password.send_keys(PASSWORD)
    browser.find_element_by_id('SubmitCreds').click()
    browser.find_element_by_xpath('//a[@href="/department"]').click()
    browser.find_element_by_xpath('//a[@href="/department/citd"]').click()
    html = browser.page_source
    return html

def get_menu(soup):
    result = soup.find(class_="menu vertical menu-vertical")
    result_in_static = result.findAll("li", class_="static")
    result_in_static_dynamic = result.findAll("li", class_="static dynamic-children")
    result_in_static_selected = result.findAll("li", class_="static selected")

    print(result_in_static)

    print("static")
    for ele in result_in_static:
        name = ele.find(class_="menu-item-text")
        print(name.get_text())
    print()

    print("result_in_static_dynamic")
    for ele in result_in_static_dynamic:
        inner_ele = ele.findAll("li", class_="dynamic")
        for small_ele in inner_ele:
            print(small_ele.get_text())
    print()

    print("static selected")
    for ele in result_in_static_selected:
        print(ele.get_text())
    print()

    #menuNameList = result.findAll("span", class_=re.compile("menu-item-text"))
    # for ele in innerResult:
    #     print("----------------------------------------------------------------")
    #     #name = ele.find(class_="menu-item-text")
    #     print(ele.get_text())
    #     link = ele.find("a")
    #     if (link != None):
    #         print(link.get('href'))
    #     print("----------------------------------------------------------------")
    #     print()
    # for ele in menuNameList:
    #     print(ele.get_text())
        # print(ele.children)
        # link = ele.find('a')
        # print(link)
        # if(link != None):
        #     print(link.get('href'))

def main():
    _html = get_HTML_From_URL()
    soup = BeautifulSoup(_html, "lxml")
    get_menu(soup)
    #print(soup.prettify())

if __name__ == "__main__":
    main()