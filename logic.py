from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException, TimeoutException
import undetected_chromedriver as webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time


class Automatter():
    def __init__(self) -> None:
        pass

    def initDriver(self):
        print("Inititating driver...")
        # create driver options
        options = webdriver.ChromeOptions()
        options.add_argument('--ignore-certificate-errors')
        # options.add_experimental_option('excludeSwitches', ['enable-logging'])

        # initiate the driver:
        driver = webdriver.Chrome(options=options)

        self.driver = driver

    def navToWebsite(self):
        print('navigating to website...')
        # open the web page in the browser:
        self.driver.get("https://www.herald.co.zw/")

        # wait for cookies modal to pop up and then click accept
        ignored_exceptions=(NoSuchElementException,StaleElementReferenceException,TimeoutException)
        cookie_accept_btn = WebDriverWait(self.driver, 120, ignored_exceptions=ignored_exceptions).until( #using explicit wait for 120 seconds
            EC.presence_of_element_located((By.ID, "tru_accept_btn")) #finding the element
        )
        cookie_accept_btn.click()

    def collectTopStories(self):
        print('getting stories...')
        # get first column
        # top_stories_col = self.driver.find_element(by=By.CLASS_NAME, value="col-md-6 ptop--30 pbottom--30 article-grid")
        top_stories_col = self.driver.find_element(by=By.CLASS_NAME, value="article-grid")

        # find all anchor tag links
        links = top_stories_col.find_elements(by=By.TAG_NAME, value="a")
        links = [link.get_attribute('href') for link in links]
        links = list(set(links))

        # remove non-story links
        try:
            links.remove('https://www.herald.co.zw/category/articles/top-stories/')
        except ValueError:
            pass

        try:
            links.remove('https://www.herald.co.zw/#')
        except ValueError:
            pass

        print('we have {} stories...'.format(len(links)))
        print('navigate to story...')
        stories = []
        i=1
        for link in links:
            print('navigate to story number {}/{}...'.format(i, len(links)))
            if i>1:
                print('waiting for 3 seconds before moving on to the next story...')
                time.sleep(3)
            self.driver.get(link)
            print('find story...')
            story_column = self.driver.find_element(by=By.CLASS_NAME, value="main--content")
            story_title = story_column.find_element(by=By.CLASS_NAME, value="title").text
            story_content = story_column.find_element(by=By.CLASS_NAME, value="post--content").text
            story = {
                'link': link,
                'story_title': story_title,
                'story_content': story_content
            }
            print('append story to stories...')
            stories.append(story)
            i+=1

        stories = pd.DataFrame(stories)
        print('saving stories as excel file...')
        stories.to_excel('stories.xlsx', index=False)


if __name__ == "__main__":
    auto = Automatter()

    auto.initDriver()
    auto.navToWebsite()
    auto.collectTopStories()

    print('Goodbye!')