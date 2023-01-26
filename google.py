from zombie import Zombie
from selenium.webdriver.remote.webdriver import By

class Google:
    def __init__(self,zombie:Zombie):
        self.z = zombie

    def login(self,username:str,password:str):
        
        
        self.z.pause()
        
        self.z.driver.get("https://accounts.google.com/")


        XPATH_email = "//input[@autocomplete='username'][@type='email']"
        XPATH_next = '''//*[contains(text(), "Next")]'''
        XPATH_password = "//input[@autocomplete='current-password'][@type='password']"

        ELEM_email = self.z.driver.find_element(By.XPATH,XPATH_email)

        self.z.realSendKeys(ELEM_email,username)

        self.z.pause

        ELEM_next = self.z.driver.find_element(By.XPATH,XPATH_next)
        ELEM_next.click()

        ELEM_password = self.z.driver.find_element(By.XPATH,XPATH_password)
        self.z.realSendKeys(ELEM_password,password)

        self.z.pause()
        ELEM_next = self.z.driver.find_element(By.XPATH,XPATH_next)
        ELEM_next.click()



