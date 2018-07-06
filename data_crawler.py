from bs4 import BeautifulSoup
from chatterbot import ChatBot
from selenium import webdriver
import re
import json
from treelib import Node, Tree

class DataCrawler():
    USERNAME = "KC_SUEN"
    PASSWORD = "Y5837810y!"

    LOGIN_URL = "https://www.tgwiki.com/CookieAuth.dll?GetLogon?curl=Z2F&reason=0&formdir=9"
    URL = "https://www.tgwiki.com"

    DIRECTORY = ["RootFolder"]
    URL_suffix = ".aspx"

    browser = None
    dataTree = None

    def __init__(self):
        self.browser = webdriver.Chrome()
        self.array = []
        self.dataTree = Tree()
        self.dataTree.create_node("Homepage", "homepage", data=self.URL)

    def login(self):
        self.browser.get(self.LOGIN_URL)
        username = self.browser.find_element_by_id('username')
        username.send_keys(self.USERNAME)
        password = self.browser.find_element_by_id('password')
        password.send_keys(self.PASSWORD)
        self.browser.find_element_by_id('SubmitCreds').click()
        self.browser.find_element_by_xpath('//a[@href="/department"]').click()
        self.browser.find_element_by_xpath('//a[@href="/department/citd"]').click()
        html = self.browser.page_source
        return html

    def get_HTML_From_URL(self, url):
        self.browser.get(url)
        html = self.browser.page_source
        return html

    def get_menu(self, soup):
        result = soup.find(class_="menu vertical menu-vertical")
        result_in_static = result.findAll("li", class_="static")

        for ele in result_in_static:
            print("-------------------------------------------------------")
            name = ele.find(class_="menu-item-text")
            inner_ele = ele.findAll("li", class_="dynamic")
            link = None
            if(inner_ele == []):
                link = self.parseLink(ele)
            else: # FOR DEBUGGING
                print(name.get_text()) # FOR DEBUGGING
            self.dataTree.create_node(name.get_text(), name.get_text().lower(), data=link, parent="homepage")
            for small_ele in inner_ele:
                link = self.parseLink(small_ele)
                self.dataTree.create_node(small_ele.get_text(), small_ele.get_text().lower(), data=link, parent=name.get_text().lower())
            print("-------------------------------------------------------")

    def parseLink(self, soup_result, _parent=None):
        link = soup_result.a
        temp = None
        if (link != None):
            temp = link.get('href')
            print(link.get_text())
            print(temp)
            if (temp[0] == '/'):
                temp = self.URL + temp
            if(_parent != None):
                self.dataTree.create_node(link.get_text(), link.get_text().lower(), data=link, parent=_parent)
        if(self.isDirectory(temp)):
            _html = self.get_HTML_From_URL(temp)
            soup = BeautifulSoup(_html, "lxml")
            self.parseTable(soup)
        return temp

    def parseTable(self, soup_result):
        # print("-------------------------------------------------------")
        # print("parseTable")
        try:
            table_list = soup_result.findAll("table")
            for table in table_list:
                if(table.has_attr("summary")):
                    table_body = table.find('tbody')
                    row_list = table_body.findAll('td', attrs={"class": "ms-vb-title"})
                    for x in range(0,  len(row_list)):
                        self.parseLink(row_list[x])
                    break

        except AttributeError as e:
            print(e)
        # print("-------------------------------------------------------")

    def isDirectory(self, link):
        if(link == None):
            return False
        isDirectory = False
        if (self.URL_suffix == link[-5:]):
            return True
        for directory in self.DIRECTORY:
            if (directory in link):
                isDirectory = True
        return isDirectory

    def getJSON_Tree(self):
        return self.dataTree.to_json(with_data=True)

    def writeToJSONFile(self, path, fileName, data):
        filePathNameWExt = './' + path + '/' + fileName + '.json'
        with open(filePathNameWExt, 'w') as fp:
            json.dump(data, fp)

    def main(self):
        _html = self.login()
        soup = BeautifulSoup(_html, "lxml")
        self.get_menu(soup)
        tree_in_json = self.getJSON_Tree()
        print(tree_in_json)
        parsed = json.loads(tree_in_json)
        # print(json.dumps(parsed, indent=4, sort_keys=True))
        self.writeToJSONFile('./', 'training', parsed)
        self.dataTree.show()

if __name__ == "__main__":
    crawler = DataCrawler()
    crawler.main()
    crawler.browser.close()