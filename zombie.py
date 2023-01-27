import undetected_chromedriver as uc
from proxies import Proxy
import uuid
import os
import shutil
from strings import proxyExtensionStrings
import time
import random
from selenium.webdriver.remote.webdriver import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import Keys

class Zombie:
    def __init__(self,proxy:Proxy | None = None,defaultImplTimeout = 6,pause_cnfg : dict = {}):
        options = uc.ChromeOptions()
        self.proxy = proxy
        self.pause_cnfg = {
            "min":1000,
            "max":1500,
            "shortM":0.35,
        }
        locale = "en-GB"
        
        self.pause_cnfg.update(pause_cnfg)
        
        print(self.pause_cnfg)

        if not proxy == None:
            extensionFolderPath = os.path.join(os.path.dirname(__file__),"proxies",str(uuid.uuid4()))
            self.__generateProxyExtensionFolder(extensionFolderPath)
            options.add_argument(f"--load-extension={','.join([extensionFolderPath])}")

        options.add_argument(f"--lang={locale}")
        self.driver = uc.Chrome(
            options=options
        )

        self.driver.implicitly_wait(defaultImplTimeout)

        if not proxy == None:
            shutil.rmtree(extensionFolderPath)


    def getConditionalElement(self,xpath:str):
        try:
            elem = self.driver.find_element(By.XPATH,xpath)
            return elem
        except NoSuchElementException:
            return False

    def queryPageUpdate(self,anchorXpath:str,timeOut: int =10,interval:int =0.1) -> bool:
        Tstart = time.time()
        while time.time() < Tstart + timeOut:
            try:
                print("query!")
                self.driver.find_element(By.XPATH,anchorXpath)
                time.sleep(interval)
            except NoSuchElementException:
                return True
        
        return False


    def querySubmitResult(self,successXpath:str,failXpath:str,timeout: int = 10, interval: int = 0.1) ->bool:
        Tstart = time.time()
        while time.time() < Tstart + timeout:
            try: #check for success Xpath
                self.driver.find_element(By.XPATH,successXpath)
                return True
            except NoSuchElementException:
                pass

            try: #check for fail xpath
                self.driver.find_element(By.XPATH,failXpath)
                return False
            except NoSuchElementException:
                pass
            
            time.sleep(interval)


        
        raise NoSuchElementException("could not find either element proposed, after timeout.")

        
    

    def alterElemAttribute(self,xpath:str,attribute:str,newValue:str):
        self.driver.execute_script(f'document.evaluate(`{xpath}`, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.setAttribute("{attribute}","{newValue}")')


    def realClearField(self,element : uc.WebElement):
            if element.get_property("value") != "":
                self.pause(shortened=True)
                element.send_keys(Keys.CONTROL, "a")
                self.pause(shortened=True)
                element.send_keys(Keys.BACK_SPACE)
                self.pause()

    
    def realSendKeys(self,element : uc.WebElement,string:str,clickElem = True, ms :int =145,randomOffSet : bool | int =20):
        if clickElem == True:
            self.pause(shortened=0.15)
            element.click()

            for char in string:
                delay = ms if randomOffSet == False else ms + random.randint(-randomOffSet,randomOffSet)
                time.sleep(delay / 1000)
                element.send_keys(char)

    def pause(self,min : int | None = None, max : int | None = None,shortened : bool | float = False):
        if(min == None):
            min = self.pause_cnfg["min"]
        if max == None:
            max = self.pause_cnfg["max"]

        if min >= max:
            raise ValueError("min argument cannot be greater than max argument for pause.")
        
        if not shortened == False:
            if shortened == True:
                shortened = self.pause_cnfg["shortM"]

        if shortened >= 1 or shortened < 0:
            raise ValueError(f"invalid argument for shortened: '{shortened}' cannot be >= 1 or <0 .")
            
        time.sleep(random.randint(min,max) / 1000 * shortened if not shortened == False else 1)



    def __generateProxyExtensionFolder(self,folderPath="proxyExtension") -> str:
        if not os.path.isdir(folderPath):
            os.mkdir(folderPath)

        with open(os.path.join(folderPath,"manifest.json"), "w") as f:
            f.write(proxyExtensionStrings["manifest"])
        with open(os.path.join(folderPath,"background.js"), "w") as f:
            f.write(proxyExtensionStrings["script"] % (self.proxy.host, self.proxy.port, self.proxy.user, self.proxy.password))

        return folderPath

    

        

        

