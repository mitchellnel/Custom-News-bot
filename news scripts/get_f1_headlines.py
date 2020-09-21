from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
import time
import random

URL = "https://www.formula1.com/en/latest/all.news.html"
PATH = "/Users/user/Google Drive/2020/Custom-News-bot/chromedriver"
options = webdriver.ChromeOptions()
#options.add_argument("headless")

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

    news_elems = browser.find_elements_by_css_selector("#article-list > div > div.row.js-load-more-container > div")

    print(len(news_elems))

    for headline in news_elems:
        if headline.get_attribute("class") != "f1-latest-listing--grid-item col-12 col-md-6 col-lg-4":
            continue

        news_info_elem = headline.find_element_by_tag_name("a")
        news_text = news_info_elem.find_element_by_css_selector("div.f1-cc--caption > p.no-margin.f1--s")
        url = news_info_elem.get_attribute("href")

        print(news_text.text.split('\n', 1)[0])
        print(url)

    browser.quit()

todays_headlines()
