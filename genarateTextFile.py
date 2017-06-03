import selenium
from selenium import webdriver
import re
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary


# driver = webdriver.Chrome('C:/Users/Chamee PC/Downloads/chromedriver.exe')
driver = webdriver.Firefox()
driver.get("https://en.wikipedia.org/wiki/Tourism_in_Sri_Lanka")
content = driver.find_element_by_tag_name("body").text
content = re.sub(r'\d+', '', content)
linkList = driver.find_elements_by_tag_name('a')
print(content)
print(linkList)
