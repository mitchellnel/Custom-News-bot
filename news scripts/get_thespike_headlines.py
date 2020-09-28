from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
import time
import random

URL = "https://thespike.gg"
PATH = "/Users/user/Google Drive/2020/Custom-News-bot/chromedriver"
options = webdriver.ChromeOptions()
options.add_argument("headless")

def headlines():
    browser = webdriver.Chrome(PATH, options = options)
    try:
        browser.set_page_load_timeout(8)
        browser.get(URL)
    except TimeoutException:
        webdriver.ActionChains(browser).send_keys(Keys.ESCAPE).perform()

    randSleepTime = random.randint(0, 5)
    print("Sleeping for " + str(randSleepTime))
    time.sleep(randSleepTime)

    todays_news_box = browser.find_elements_by_css_selector("#news-module > ul:nth-child(1) > li")
    print(len(todays_news_box))

    for headline in todays_news_box:
        if headline.get_attribute("class") != "item element-trim-button ":
            continue

        news_info_elem = headline.find_element_by_tag_name("a")
        news_text = news_info_elem.find_element_by_css_selector("div > div.news-title")
        url = news_info_elem.get_attribute("href")

        print(news_text.text.split('\n', 1)[0])
        print(url)

    browser.quit()

headlines()

