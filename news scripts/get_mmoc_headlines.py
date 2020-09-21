from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
import time
import random

URL = "https://www.mmo-champion.com/content/"
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

    randSleepTime = random.randint(0, 5)
    print("Sleeping for " + str(randSleepTime))
    time.sleep(randSleepTime)

    news_elem = browser.find_element_by_css_selector("#section_content > div:nth-child(1) > div > div > div.title > h3 > a")

    news_text = news_elem.find_element_by_css_selector("span")
    url = news_elem.get_attribute("href")

    print(news_text.text.split('\n', 1)[0])
    print(url)

    browser.quit()

todays_headlines()
