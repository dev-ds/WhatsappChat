# -*- coding: utf-8 -*-
"""
Created on Mon Jan 21 13:07:02 2019

@author: devds
"""

from selenium import webdriver 
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC 
from selenium.webdriver.common.keys import Keys 
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import autoit
import os
import shutil
from datetime import datetime, date
import time

# after login into Whatsapp, get the username, find them, and activate their chat
def findUser(wait, target):
    print(" {} :trying to get the user".format(datetime.now()))
    x_arg = '//*[@dir="auto"][@title="' + target + '"]'
    group_title = wait.until(EC.presence_of_element_located((By.XPATH, x_arg)))
    group_title.click()
    print(" {} :have picked up the user id".format(datetime.now()))
    #group_title.click()  # Sometimes Selenium one click will not work


# find the msg box and input the string and hit enter
def sendTxtMsg(wait, string):
    inp_xpath = '//*[@dir="ltr"][@data-tab="1"]'
    input_box = wait.until(EC.presence_of_element_located((By.XPATH, inp_xpath)))
    input_box.send_keys(string + Keys.ENTER)
    time.sleep(1)

# install pyautoit using the below command
#
# pip install -U https://github.com/jacexh/pyautoit/archive/master.zip
#https://stackoverflow.com/questions/3301561/calling-autoit-functions-in-python
#


def getImage(imageDir):
    # should have code to randomly pick up and image for from 365 images
    pass

def sendIMG(driver, imageDir, fileName):
    clipButton = driver.find_element_by_xpath('//*[@role="button"][@title="Attach"]')
    clipButton.click()
    time.sleep(3)
    
    print(" {} :found the clip".format(datetime.now()))
    mediaButton = driver.find_element_by_xpath('//*[@class=""][@data-icon="image"]')
    mediaButton.click()
    time.sleep(3)
    
    print(" {} :found the media button".format(datetime.now()))

	# sometimes it takes time for the code to perform a certain action like clicking a button so just added a loop to try it thrice
    
    imagePath = imageDir + fileName
    autoit.control_focus("File Upload", "Edit1")
    autoit.control_set_text("File Upload", "Edit1",(imagePath) )
    autoit.control_click("File Upload", "Button1")
    time.sleep(3)
    for i in range(3):
        try:
            print(" {} :try : ".format(datetime.now()) + str(i))
            whatsapp_send_button = driver.find_element_by_xpath('//*[@class=""][@data-icon="send-light"]')
            print(" {} :Found it".format(datetime.now()))
            break
        except:
            pass
		time.sleep(2)
		
    whatsapp_send_button.click()
    print(" {} :sent".format(datetime.now()))
    time.sleep(3)

# move the file to history.
def moveToHist(quotesDir, fileName):
    historyDir = quotesDir + "\\history"
    todaysQuote = quotesDir+ "\\" + fileName
    timeStamp = str(date.today()).split('-')
    moveHistory = historyDir + "\\" + fileName + "_" + ''.join(map(str, timeStamp)) 
    if os.path.isdir(quotesDir):
        if os.path.isfile(todaysQuote):
            try:
                shutil.move(todaysQuote, moveHistory)
                print(" {} :moved ".format(datetime.now()) + fileName + " to history.")
            except:
                print(" {} :moving ".format(datetime.now()) + fileName + " to history Dir failed")
        else:
            print(" {} :Todays file went missing".format(datetime.now()))
    else:
        print(" {} :whole directory is missing".format(datetime.now()))

# Main Function

if __name__ == '__main__':
    driver = webdriver.Firefox()
    driver.get("https://web.whatsapp.com/") 
    wait = WebDriverWait(driver, 600) 

    imageDir = "D:\\Path\\to\\Quotes\\Dir"
    # Target is the user and string is the msg
    target = '<whatsapp contact>'
    string = "Good Morning <xxx>"
    fileName = "LQ01.jpg"
    findUser(wait, target)
#    imageName = getImage(imageDir)
    sendIMG(driver, imageDir, fileName)
    sendTxtMsg(wait, string)    
    print(" {} :Sent Image to ".format(datetime.now()) + target)
    moveToHist(imageDir, fileName)