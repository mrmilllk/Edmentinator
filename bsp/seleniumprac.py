import os
import time
import json
import re
from bs4 import BeautifulSoup  
from slimit import ast  # $ pip install slimit
from slimit.parser import Parser as JavascriptParser
from slimit.visitors import nodevisitor
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import MoveTargetOutOfBoundsException
from selenium.webdriver.common.keys import Keys
from pathlib import Path 
from secrets import myUsername, myPassword, chromePath

chrome_options = webdriver.ChromeOptions()
extensionPath = (str(Path(__file__).resolve().parents[0]) + r'\8.9_0.crx')
chrome_options.add_extension(extensionPath)
# print(balls) # D:\CodeProjects\VisualStudio repos\BeautifulSoupPractice\bsp\seleniumprac.py\8.9_0.crx
# time.sleep(5)
print('soup was here')

driver = webdriver.Chrome(chromePath, chrome_options=chrome_options)
driver.get("https://launchpad.classlink.com/loudoun")

userURL = "//input[@id='username']"
passURL = "//input[@id='password']"
buttonURL = "//button[@id='signin']"
edButtonURL = "//div[@class='container-fluid result-container no-selection']//div[7]//div[1]"
phyButton = "//div[@id='49021089']//a[contains(text(),'All Activities')]"
econButton = "//div[@id='49007108']//a[contains(text(),'All Activities')]"
hisButton = "//div[@id='49020693']//a[contains(text(),'All Activities')]"
engButton = "//div[@id='49021910']//a[contains(text(),'All Activities')]"
dragBar = "//div[@id='mCSB_2_dragger_vertical']//div[@class='mCSB_dragger_bar']"
dragTo = "//span[contains(text(),'©2020 Edmentum, Inc.')]"
backButton = "//a[contains(text(),'Back to Home')]"



userElement = WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_xpath(userURL))
userElement.send_keys(myUsername)

passElement = WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_xpath(passURL))
passElement.send_keys(myPassword)

print("user/pass entered")
time.sleep(1)
print("signing in...")

buttonElement = WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_xpath(buttonURL))
buttonElement.click()

edbuttonElement = WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_xpath(edButtonURL))
edbuttonElement.click()

time.sleep(15)

driver.switch_to.window(driver.window_handles[-1])
phyButtonElm = WebDriverWait(driver, 20).until(lambda driver: driver.find_element_by_xpath(phyButton))
econButtonElm = WebDriverWait(driver, 20).until(lambda driver: driver.find_element_by_xpath(econButton))
hisButtonElm = WebDriverWait(driver, 20).until(lambda driver: driver.find_element_by_xpath(hisButton))
engButtonElm = WebDriverWait(driver, 20).until(lambda driver: driver.find_element_by_xpath(engButton))
dragBarElm = WebDriverWait(driver, 20).until(lambda driver: driver.find_element_by_xpath(dragBar))

dragToElm = WebDriverWait(driver, 20).until(lambda driver: driver.find_element_by_xpath(dragTo))

hover = ActionChains(driver).move_to_element(dragBarElm)

def classSelect():
    while True:
        pickClass = input ("A) Physics" + '\n' + "B) Econ" + '\n' + "C) History" + '\n' + "D) English" + '\n' +"[a/b/c/d]? ")
        # check if d1a is equal to one of the strings, specified in the list
        if pickClass in ['a', 'b', 'c', 'd']:
            # if it was equal - break from the while loop
            break
    # process the input
    if pickClass == "a": 
        print ("opening physics...") 
        phyButtonElm = WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_xpath(phyButton))
        phyButtonElm.click()
        print("opened")

    elif pickClass == "b": 
        print ("opening econ...")
        econButtonElm = WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_xpath(econButton))
        econButtonElm.click()
        print("opened")

    elif pickClass == "c": 
        print ("opening history...")
        webdriver.ActionChains(driver).drag_and_drop(dragBarElm,dragToElm).perform()
        print("scrolled")
        time.sleep(.5)
        hisButtonElm = WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_xpath(hisButton))
        hisButtonElm.click()
        print("opened")
        
    elif pickClass == "d": 
        print ("opening english...")
        webdriver.ActionChains(driver).drag_and_drop(dragBarElm,dragToElm).perform()
        print("scrolled")
        time.sleep(.5)
        engButtonElm = WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_xpath(engButton))
        engButtonElm.click()
        print("opened")
        
    print("im in")

def openCourse():
    try:
        WebDriverWait(driver, 10).until(expected_conditions.element_to_be_clickable((By.XPATH, "//span[text()='0 of 2']"))).click()

    except NoSuchElementException:
        print("no classes found")
        while True:
            goBack = input ("Go Back and Pick New Class?" + '\n' + "[y/n]? ")
            if goBack in ['y', 'n']:
                break
        if goBack == 'y':
            WebDriverWait(driver, 10).until(expected_conditions.element_to_be_clickable((By.XPATH, "//span[text()='Back to Home']"))).click()
            classSelect()

        elif goBack == 'n':
            print("goodbye!" + "\n" + "you're on your own now.")
    else:
        print("assignment found")

def openTut():
    try:
        WebDriverWait(driver, 10).until(expected_conditions.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Tutorial')]"))).click() 
    
    except NoSuchElementException:
        print("Tutorial Not Found")
    
    else:
        print("Tutorial Opened")

def completeTut():
    try:
        print('is it disabled?')
        driver.find_element_by_xpath("//button[@class='tutorial-nav-next disabled']")

    except NoSuchElementException:
        print("nope")
        WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_xpath("//button[@class='tutorial-nav-next']")).click()
        print("*Next*")
        time.sleep(.5)
        completeTut()
    else:
        print("yes")
        print("work to be done...")
        time.sleep(2)
  
        try:
            isFRQ()
        except NoSuchElementException:
            print("not FRQ")

        try:
            isMPC()
        except NoSuchElementException:
            print("not MPC")
        
        try:
            isFinished()
        except NoSuchElementException:
            print("not done")

        completeTut()
        
def isFRQ():
    try:
        print('is it FRQ?')
        driver.switch_to.frame("content-iframe")
        # driver.find_element_by_class_name("btn buttonDone")
        driver.find_elements_by_xpath("//button[@class='btn buttonDone']")        
    except NoSuchElementException:
        print("nope")
    else:
        print("yes")
        frameArray = driver.find_elements_by_xpath('//*[@title="Rich Text Area. Press ALT-F9 for menu. Press ALT-F10 for toolbar. Press ALT-0 for help"]')
        frameCount = len(frameArray)
        print(str(frameCount) + " FRQs Found")

        count_arr = [str("mce_") + str(i) + str("_ifr") for i, x in enumerate(frameArray, start=0)]

        for x in count_arr:
            driver.switch_to.frame(x)
            print("in")
            box1Elm = driver.find_element_by_id("tinymce").get_attribute("class")
            print(box1Elm)
            answer = driver.find_element_by_xpath("//p")
            answer.send_keys('.')
            driver.switch_to.parent_frame()
            print("out")
            if x == "mce_" + str(frameCount)+"_ifr":
                break

        submitBtnElm = WebDriverWait(driver, 10).until(lambda driver: driver.find_elements_by_xpath("//button[@class='btn buttonDone']"))
        count_button = [str(i) for i, x in enumerate(submitBtnElm, start=0)]
        print(submitBtnElm)
        print(count_button)

        for x in count_button:
            print(int(x))
            int(x)
            try:
                time.sleep(.5)
                body = driver.find_element_by_css_selector('body')
                body.send_keys(Keys.PAGE_UP)
                actions = ActionChains(driver)
                actions.move_to_element(submitBtnElm[int(x)]).perform()
                driver.execute_script("arguments[0].scrollIntoView();", submitBtnElm[int(x)])
            except MoveTargetOutOfBoundsException:
                print("Button in view")
                time.sleep(1)
                submitBtnElm[int(x)].click()
                time.sleep(1)
            else:
                print("this shouldn't happen")
                
            if x == str(frameCount):
                break
        print("FRQ(s) Answered")

def isMPC():
    try:
        print('is it MPC?')
        driver.switch_to.frame("content-iframe")
        driver.find_element_by_id("mcqChoices")
    except NoSuchElementException:
        print("nope")
    else:
        print("yes")
        script = driver.find_element_by_xpath("//script[contains(.,'IsCorrect')]").get_attribute("innerHTML")
        # print(script + '\n')
        scriptElmCut = script[20:-2]
        # print(scriptElmCut + '\n')
        parsedScript = json.loads(scriptElmCut) 
        theEntireNumabet = ['0', '1', '2', '3']
        i = 0
        for choice in parsedScript['Choices']: # this goes thru all the choices
            if choice['IsCorrect']: # if the isCorrect bool is True, then the answer is correct
                print('the answer is ' + theEntireNumabet[i])
                ans = theEntireNumabet[i]
            i += 1
            
        mpcAnsr = 'choice' + ans
        print(mpcAnsr)
        mpcBtn = "\"//input[@id='" + mpcAnsr + "']\""
        print(mpcBtn)
        # mpcBtnElm = driver.find_element_by_xpath(mpcBtn)
        mpcBtnElm = WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_xpath("//input[@id='choice2']"))
        mpcBtnElm.click()
        driver.switch_to.parent_frame()
        print("MPC answered")

def isFinished():
    try:
        print("are we done?")
        driver.switch_to.frame("content-iframe")
        congrats = "//h1[contains(text(),'Congratulations!')]"
        driver.find_element_by_xpath(congrats)
        driver.switch_to.parent_frame()
        
    except NoSuchElementException:
        print("lets hope no one ever has to see this")
    else:
        driver.find_element_by_xpath("//button[@class='tutorial-nav-exit']").click()


classSelect()

time.sleep(.5)

openCourse()

time.sleep(.5)

openTut()

time.sleep(2)

completeTut()

print("done")
