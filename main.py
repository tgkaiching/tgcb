from data_crawler import DataCrawler
from tgChatbot import TkinterGUIExample

def main():
    crawler = DataCrawler()
    crawler.main()
    #json_doc = crawler.getJSON_Tree()
    gui_example = TkinterGUIExample()
    gui_example.mainloop()

if __name__ == '__main__':
    main()