from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
import time
import random

URL = "https://hltv.org"
PATH = "/Users/user/Google Drive/2020/Custom-News-bot/chromedriver"
options = webdriver.ChromeOptions()
options.add_argument("headless")

def todays_headlines():
    browser = webdriver.Chrome(PATH, options = options)
    try:
        browser.set_page_load_timeout(8)
        browser.get(URL)
    except TimeoutException:
        webdriver.ActionChains(browser).send_keys(Keys.ESCAPE).perform()

    randSleepTime = random.randint(0, 3)
    print("Sleeping for " + str(randSleepTime))
    time.sleep(randSleepTime)

    newsElems = browser.find_elements_by_css_selector("body > div.bgPadding > div > div.colCon > div.contentCol > div.index > div:nth-child(5) > a")
    print(len(newsElems))

    for headline in newsElems:
        newsText = headline.find_element_by_class_name("newstext")
        url = headline.get_attribute("href")

        print(newsText.text)
        print(url)

    browser.quit()

todays_headlines()