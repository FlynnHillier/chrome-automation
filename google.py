from zombie import Zombie
from selenium.webdriver.remote.webdriver import By

class Google:
    def __init__(self,zombie:Zombie):
        self.z = zombie
        self.loggedIn = False

    def login(self,username:str,password:str):
        self.z.pause()
        self.z.driver.get("https://accounts.google.com/")

        XPATH_email = "//input[@autocomplete='username'][@type='email']"
        XPATH_next = '''//*[contains(text(), "Next")]'''
        XPATH_password = "//input[@autocomplete='current-password'][@type='password']"

        ELEM_email = self.z.driver.find_element(By.XPATH,XPATH_email)

        self.z.realSendKeys(ELEM_email,username)
        self.z.pause()

        ELEM_next = self.z.driver.find_element(By.XPATH,XPATH_next)
        ELEM_next.click()

        ELEM_password = self.z.driver.find_element(By.XPATH,XPATH_password)
        self.z.realSendKeys(ELEM_password,password)

        self.z.pause()
        ELEM_next = self.z.driver.find_element(By.XPATH,XPATH_next)
        ELEM_next.click()
        self.loggedIn = True


    def forwardToEmail(self,forwardTo:str) -> bool:
        driver = self.z.driver
        self.z.pause()
        driver.get("https://mail.google.com/mail/u/0/?tab=rm&ogbl#settings/fwdandpop")


        XPATH_ForwardToSelection = f'''//span[contains(text(), "Forward a copy of incoming mail to")]//option[contains(text(), "{forwardTo}")][not(contains(text(),"Remove"))]'''
        XPATH_ForwardRadioButton = '''//*[contains(text(), "Forward a copy of incoming mail to")]/ancestor::tbody[1]//input[@type="radio"][@value="1"]'''
        XPATH_saveChanges = '''//*[contains(text(), "Save Changes")]'''
        XPATH_VERIFYFIELD = f'''//tr//*[contains(text(), "Verify {forwardTo}")]/ancestor::tr[1]//input[@act='verifyText']'''
        XPATH_onSubmitIsForwarding = f'''//*[contains(text(), "You are forwarding your email to {forwardTo}.")]'''

        XPATH_onVerifyCodeSubmitIsInvalid = '''//div[contains(text(), "Incorrect confirmation code.")]'''

        #check if have already validated forwarding email
        forwardToSelection = self.z.getConditionalElement(XPATH_ForwardToSelection)

        if forwardToSelection == False:
            #forward request already sent to forward to email?
            VerifyField = self.z.getConditionalElement(XPATH_VERIFYFIELD)

            if VerifyField == False:
                #select add forward email address
                XPATH_forwardButton = "//input[@value='Add a forwarding address']"
                ELEM_forwardButton = driver.find_element(By.XPATH,XPATH_forwardButton)
                self.z.pause()
                ELEM_forwardButton.click()

                #input field.
                XPATH_inputField = '''//*[contains(text(), "Please enter a new forwarding email address:")]//input[@type='text']'''
                ELEM_inputField = driver.find_element(By.XPATH,XPATH_inputField)
                self.z.pause()
                ELEM_inputField.click()
                ELEM_inputField.send_keys(forwardTo)

                #handle popup window
                base_window = driver.window_handles[0]
                ELEM_inputField.send_keys("\n")
                popup_winodw = driver.window_handles[1]
                driver.switch_to.window(popup_winodw)
                XPATH_popupSubmit = "//input[@value='Proceed']"
                ELEM_popupSubmit = driver.find_element(By.XPATH,XPATH_popupSubmit)
                ELEM_popupSubmit.click()
                driver.switch_to.window(base_window)

                #handle 'email has been sent to forwardTo'
                XPATH_ForwardOK = "//button[@name='ok']"
                ELEM_ForwardOk = driver.find_element(By.XPATH,XPATH_ForwardOK)
                ELEM_ForwardOk.click()

                VerifyField = driver.find_element(By.XPATH,XPATH_VERIFYFIELD)

            #handle verification code
            verified = False
            while verified == False:
                verifyCode = input("verification code:\n>> ")
                if len(verifyCode) != 9 or not verifyCode.isnumeric():
                    print("invalid verification code format.")
                    continue
                
                VerifyField.click()
                VerifyField.send_keys(f"{verifyCode}\n")

                if self.z.getConditionalElement(XPATH_onVerifyCodeSubmitIsInvalid) != False:
                    driver.execute_script(f'document.evaluate(`{XPATH_onVerifyCodeSubmitIsInvalid}`, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.innerText = "TYPE IN THE CORRECT CODE YOU MUG!";')
                    
                    
                    print("incorrect verification code.")
                    VerifyField.clear()
                else:
                    verified = True


        #select correct forwarding email
        ELEM_forwardToSelection = driver.find_element(By.XPATH,XPATH_ForwardToSelection)
        ELEM_forwardToSelection.click()

        #forward to email radio selection
        ELEM_radioButton = driver.find_element(By.XPATH,XPATH_ForwardRadioButton)
        ELEM_radioButton.click()

        #save changes
        ELEM_saveChanges = driver.find_element(By.XPATH,XPATH_saveChanges)

        if not ELEM_saveChanges.is_enabled():
            print("already forwarding!")
            return True
        else:
            ELEM_saveChanges.click()
            isForwarding = self.z.getConditionalElement(XPATH_onSubmitIsForwarding)
            return True if isForwarding != False else False