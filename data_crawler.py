from bs4 import BeautifulSoup
from chatterbot import ChatBot
from selenium import webdriver
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
    print(result)
    #result = soupForMenu.find_all(class_="result = menu-item-text")

def main():
    _html = get_HTML_From_URL()
    soup = BeautifulSoup(_html, "lxml")
    get_menu(soup)
    #print(soup.prettify())

if __name__ == "__main__":
    main()