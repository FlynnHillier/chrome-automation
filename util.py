import time
import random
from typing import Union
from undetected_chromedriver import Chrome



def spreadSendKey(driverElem : Chrome,string : str,ms :int =145,randomOffSet : Union[bool,int] =20):
    for char in string:
        delay = ms if randomOffSet == False else ms + random.randint(-randomOffSet,randomOffSet)
        time.sleep(delay / 1000)
        driverElem.send_keys(char)



def sleepChain(mindelay=1000,maxdelay=1600,*events):
    for event in events:
        time.sleep(random.randint(mindelay,maxdelay) / 1000)
        event()


def pause(min=1000,max = 1500):
    time.sleep(random.randint(min,max) /1000)

def short_pause():
    pause(350,600)
