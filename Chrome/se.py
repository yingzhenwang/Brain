from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
# import Action chains
from selenium.webdriver.common.action_chains import ActionChains
driver = webdriver.Chrome('/Users/hwyz/programming/chromedriver')
driver.get("https://youtu.be/spUNpyF58BY")
print("got")
video = driver.find_element_by_id('movie_player')
#video.send_keys(Keys.SPACE) #hits space
#print("space pressed")
time.sleep(1)
video.send_keys('t')
print("cine_mode")
time.sleep(5)
video.send_keys(Keys.ARROW_RIGHT)
print("forward 5s")
time.sleep(1)
video.send_keys(Keys.ARROW_RIGHT)
print("forward 5s")
time.sleep(1)
video.send_keys(Keys.ARROW_LEFT)
print("forward 5s")
time.sleep(15)
video.click()               #mouse click
print("stopped")

video.send_keys(Keys.ARROW_RIGHT)