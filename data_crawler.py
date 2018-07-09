from bs4 import BeautifulSoup
from selenium import webdriver
import re
import json
import treelib
from treelib import Node, Tree


class DataCrawler():
    USERNAME = "KC_SUEN"
    PASSWORD = "Y5837810y!"

    LOGIN_URL = "https://www.tgwiki.com/CookieAuth.dll?GetLogon?curl=Z2F&reason=0&formdir=9"
    URL = "https://www.tgwiki.com"

    DIRECTORY = ["RootFolder"]
    URL_suffix = ".aspx"

    EXCEPTION_MENU_ITEM = "Service Level Agreement"

    browser = None
    dataTree = None

    def __init__(self):
        self.browser = webdriver.Chrome()
        self.array = []
        self.dataTree = Tree()
        self.dataTree.create_node("Homepage", "homepage/", data=self.URL)

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
        print("Accessing " + str(url))
        self.browser.get(url)
        html = self.browser.page_source
        return html

    def get_menu(self, soup):
        result = soup.find(class_="menu vertical menu-vertical")
        result_in_static = result.findAll("li", class_="static")
        for ele in result_in_static:
            # print("-------------------------------------------------------")
            name = ele.find(class_="menu-item-text")
            inner_ele = ele.findAll("li", class_="dynamic")
            link = None
            parentID = "homepage/"
            if(inner_ele == []):
                # print(name.get_text())  # FOR DEBUGGING
                link_tag, link = self.parseLink(ele)
            self.dataTree.create_node(name.get_text(), parentID + name.get_text().lower() + "/", data=link,
                                      parent=parentID)
            if (self.isDirectory(link)):
                _html = self.get_HTML_From_URL(link)
                soup = BeautifulSoup(_html, "lxml")
                self.parseTable(soup, parentID + link_tag.get_text().lower() + "/")
            # else: # FOR DEBUGGING
            #     print(name.get_text()) # FOR DEBUGGING

            if(name.get_text() == "Technology Update"):
                print("")
            # self.dataTree.show(idhidden=False)
            for small_ele in inner_ele:
                parentID = "homepage/" + name.get_text().lower() + "/"
                link_tag, link = self.parseLink(small_ele, _parent=parentID)
                print("CHECKING IF "+ str(link) +" IS DIRECTORY...")
                #self.dataTree.show()
               # self.dataTree.create_node(small_ele.get_text(), small_ele.get_text().lower(), data=link, parent=name.get_text().lower())
                if (self.isDirectory(link)):
                    _html = self.get_HTML_From_URL(link)
                    soup = BeautifulSoup(_html, "lxml")
                    self.parseTable(soup, parentID + link_tag.get_text().lower() + "/")
            # print("-------------------------------------------------------")

    def parseLink(self, soup_result, _parent=None):
        print("praseLink")
        link_tag = soup_result.a
        link = None
        if (link_tag != None):
            link = link_tag.get('href')
            # print(link_tag.get_text())
            # print(link)
            if (link[0] == '/'):
                link = self.URL + link
            if(_parent != None):
                print("############")
                print("Tag: " + str(link_tag))
                print("Text: " + link_tag.get_text())
                print("Link: " + str(link))
                print("Parent: " + str(_parent))
                print("############")
                # self.dataTree.show(idhidden=False)
                # if(link_tag.get_text() == self.EXCEPTION_MENU_ITEM):
                #     if(self.dataTree.contains(self.EXCEPTION_MENU_ITEM.lower())):
                #         print("dfgdfgdgdfgdfgd")
                #         return link_tag, link

                try:
                    self.dataTree.create_node(str(link_tag.get_text()), _parent + str(link_tag.get_text().lower() + "/"), data=link,
                                              parent=_parent)
                except treelib.tree.DuplicatedNodeIdError:
                    print("duplicated")
                    return link_tag, link

        # if(self.isDirectory(temp)):
        #     _html = self.get_HTML_From_URL(temp)
        #     soup = BeautifulSoup(_html, "lxml")
        #     self.parseTable(soup, link.get_text().lower())
        return link_tag, link

    def parseTable(self, soup_result, _parent=None):
        print("-------------------------------------------------------")
        print("parseTable")
        try:
            table_list = soup_result.findAll("table")
            for table in table_list:
                if(table.has_attr("summary")):
                    table_body = table.find('tbody')
                    row_list = table_body.findAll('td', attrs={"class": "ms-vb-title"})
                    for x in range(0,  len(row_list)):
                        link_tag, link = self.parseLink(row_list[x], _parent)
                        if (self.isDirectory(link)):
                            _html = self.get_HTML_From_URL(link)
                            soup = BeautifulSoup(_html, "lxml")
                            self.parseTable(soup, _parent+link_tag.get_text().lower()+"/")
                    break

        except AttributeError as e:
            print(e)
        print("-------------------------------------------------------")

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

    def writeToJSONFile(self, path, fileName, data):
        filePathNameWExt = './' + path + '/' + fileName + '.json'
        with open(filePathNameWExt, 'w') as fp:
            json.dump(data, fp)

    def main(self):
        _html = self.login()
        soup = BeautifulSoup(_html, "lxml")
        self.get_menu(soup)
        self.dataTree.show()
        tree_in_dict = self.dataTree.to_json(with_data=True)
        tree_in_json = json.dumps(tree_in_dict, indent=4, sort_keys=True, ensure_ascii=False)
        self.writeToJSONFile('./', 'training', tree_in_json)
        self.dataTree.save2file('tree_diagiam.json')

if __name__ == "__main__":
    crawler = DataCrawler()
    crawler.main()
    crawler.browser.close()