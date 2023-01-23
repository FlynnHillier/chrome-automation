import time
import random
from typing import Union
from selenium.webdriver.support.wait import WebDriverWait


def spreadSendKey(driverElem,string : str,ms :int =145,randomOffSet : Union[bool,int] =20):
    for char in string:
        delay = ms if randomOffSet == False else ms + random.randint(-randomOffSet,randomOffSet)
        time.sleep(delay / 1000)
        driverElem.send_keys(char)