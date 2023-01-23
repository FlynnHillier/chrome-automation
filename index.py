import undetected_chromedriver as uc
from selenium.webdriver.remote.webdriver import By
import selenium.webdriver.support.expected_conditions as EC  # noqa
from selenium.webdriver.support.wait import WebDriverWait
from util import spreadSendKey

from selenium.webdriver.common.proxy import Proxy, ProxyType


driver = uc.Chrome()

driver.get('https://accounts.google.com/signup/v2/webcreateaccount?biz=false&cc=GB&continue=https%3A%2F%2Faccounts.google.com%2Fb%2F0%2FAddMailService&dsh=S604852170%3A1674488625616644&flowEntry=SignUp&flowName=GlifWebSignIn&followup=https%3A%2F%2Faccounts.google.com%2Fb%2F0%2FAddMailService&ifkv=AWnogHc85__DkFzCt-goBhMnhsz-AuamPDWhAkj9adkhQ0nfhYm_a0UozBApiDy4WHkYaUWL9RKbVQ')

try:
    WebDriverWait(driver,10).until(
        EC.presence_of_element_located((By.Id,"view_container"))
    )
except:
    print("did not locate element.")




inp_fname = driver.find_element(By.XPATH,"//input[@id='firstName']") #[@autocomplete='username']
inp_lname = driver.find_element(By.XPATH,"//input[@id='lastName']")
inp_username = driver.find_element(By.XPATH,"//input[@id='username']")

inp_passwords = driver.find_elements(By.XPATH,"//input[@autocomplete='new-password']")

next_button = driver.find_element(By.XPATH,'''//*[contains(text(), "Next")]''') #input[@id='view_container']


spreadSendKey(inp_fname,"jospeh")
spreadSendKey(inp_lname,"beamer")
spreadSendKey(inp_username,"josephtest1231")

for elem in inp_passwords:
    spreadSendKey(elem,"Insane123!!")


driver.execute_script("arguments[0].click()",next_button)
