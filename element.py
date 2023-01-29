from undetected_chromedriver import WebElement
from selenium.webdriver import Chrome
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.remote.webdriver import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import Keys
import time
import random

class HideAttribute:
    def __init__(self,attr:str,replaceVal:str | bool | int) -> None:
        self.attr = attr
        self.replaceVal = replaceVal



class Element:
    def __init__(self,driver:Chrome,xpath:str,hideself : HideAttribute | None = None,initGetElement = True):
        self.driver : Chrome = driver
        self.xpath : str = xpath
        self.webelement : WebElement | None = None if initGetElement == False else self.getElement()
        self.hideself : str | None = hideself

    def getElement(self) -> None | WebElement:
        try:
            element = self.driver.find_element(By.XPATH,self.xpath)
            self.webelement = element
            return element
        except NoSuchElementException:
            return None

    def isPresent(self,timeout=3) -> bool:
        try:
            WebDriverWait(self.driver,timeout).until(
                EC.presence_of_element_located((By.XPATH,self.xpath))
            )
            return True
        except TimeoutError:
            return False

    
    def waitUntilPresent(self,timeout=15) -> WebElement:
        if self.isPresent(timeout) == False:
            raise TimeoutError(f"could not locate element within time '{timeout}' seconds with xpath '{self.xpath}'")
        element = self.getElement()
        if element == None:
            raise NoSuchElementException("unexpected error. expecting element to be present, but found no such instance on search.")
        return element

    
    def invalidateXpath(self,hideDetails : HideAttribute | None = None):
        if hideDetails == None:
            hideDetails = self.hideself

        if hideDetails == None:
            raise ValueError("cannot hidelself if hidedetails is not provided.")

        if not self.isPresent(timeout=0.5):
            raise NoSuchElementException("cannot hide self if element is not present.")
        
        self.driver.execute_script(f'document.evaluate(`{self.xpath}`, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.setAttribute("{hideDetails.attr}","{hideDetails.replaceVal}")')

    
    def realClearField(self):
        if self.webelement == None:
            raise NoSuchElementException("cannot clear field on non-existant element.")

        if self.webelement.get_property("value") != "":
            self.sleep(500)
            self.webelement.send_keys(Keys.CONTROL, "a")
            self.sleep(1200)
            self.webelement.send_keys(Keys.BACK_SPACE)
            self.sleep(1200)

    
    def realSendKeys(self,string:str,clickElem = True):
        if clickElem == True:
            self.webelement.click()
            self.sleep(600)

        for char in string:
            self.sleep()
            self.webelement.send_keys(char)

    
    def sleep(self,delay:int = 150,randOffset: int | None = 20): #returns a random time in seconds
        msTime =  delay if randOffset == None else delay + random.randint(-randOffset,randOffset)
        seconds = msTime / 1000
        
        time.sleep(seconds) #in seconds
        return seconds



    

