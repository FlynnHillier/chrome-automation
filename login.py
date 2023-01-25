from undetected_chromedriver import Chrome
from selenium.webdriver.remote.webdriver import By
from selenium.webdriver.support.wait import WebDriverWait
import selenium.webdriver.support.expected_conditions as EC
from util import spreadSendKey,short_pause,pause



def googleLogin(driver:Chrome,username:str,password:str):
    pause()
    
    driver.get("https://accounts.google.com/")


    XPATH_email = "//input[@autocomplete='username'][@type='email']"
    XPATH_next = '''//*[contains(text(), "Next")]'''

    XPATH_password = "//input[@autocomplete='current-password'][@type='password']"


    WebDriverWait(driver,10).until(
        EC.presence_of_element_located((By.XPATH,XPATH_email))
    )

    pause()
    ELEM_email = driver.find_element(By.XPATH,XPATH_email)
    ELEM_email.click()

    short_pause()

    spreadSendKey(ELEM_email,username)

    pause()

    ELEM_next = driver.find_element(By.XPATH,XPATH_next)
    ELEM_next.click()


    WebDriverWait(driver,10).until(
        EC.presence_of_element_located((By.XPATH,XPATH_password))
    )

    pause()

    ELEM_password = driver.find_element(By.XPATH,XPATH_password)
    ELEM_password.click()
    short_pause()
    
    spreadSendKey(ELEM_password,password)


    pause()
    ELEM_next = driver.find_element(By.XPATH,XPATH_next)
    ELEM_next.click()


    # #if 'your signed in page'.
    # XPTAH_notNow = '''//*[contains(text(), "not now")]'''

    # WebDriverWait(driver,10).until(
    #     EC.presence_of_element_located((By.XPATH,XPTAH_notNow))
    # )

    # ELEM_notNow = driver.find_element(By.XPATH,XPTAH_notNow)

    # pause()
    # ELEM_notNow.click()
    









