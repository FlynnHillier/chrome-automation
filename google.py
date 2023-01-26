from zombie import Zombie
from selenium.webdriver.remote.webdriver import By
import random
import string
from selenium.webdriver import Keys
from selenium.webdriver.support.wait import WebDriverWait
import selenium.webdriver.support.expected_conditions as EC

import time


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



    def signup(self,fname:str,lname:str,password:str,phoneNumber : str,email : str | None = None):
        driver = self.z.driver

        driver.get("https://accounts.google.com/signup")

        inp_fname = driver.find_element(By.XPATH,"//input[@id='firstName']") #[@autocomplete='username']
        inp_lname = driver.find_element(By.XPATH,"//input[@id='lastName']")
        inp_username = driver.find_element(By.XPATH,"//input[@id='username']")
        inp_passwords = driver.find_elements(By.XPATH,"//input[@autocomplete='new-password']")
        next_button = driver.find_element(By.XPATH,'''//*[contains(text(), "Next")]''') #input[@id='view_container']

        #generate email from first and last name if one is not provided in arguments
        email = email if email != None else self.__generateEmailAddress(fname,lname) 

        #enter details
        self.z.pause()
        self.z.realSendKeys(inp_fname,fname)
        self.z.pause(shortened=True)
        self.z.realSendKeys(inp_lname,lname)
        self.z.pause(shortened=True)
        inp_username.click()

        #clear email field if suggested is displayed
        if inp_username.get_property("value") != "":
            self.z.pause(shortened=True)
            inp_username.send_keys(Keys.CONTROL, "a")
            self.z.pause(shortened=True)
            inp_username.send_keys(Keys.BACK_SPACE)
        self.z.realSendKeys(inp_username,email)
        
        #enter passwords
        for elem in inp_passwords:
            self.z.pause()
            self.z.realSendKeys(elem,password)
        
        self.z.pause()
        next_button.click()

        

        #if verify phone number
        XPATH_isVerifyPhoneNumber = '''//*[contains(text(), "Verifying your phone number")]'''

        if self.z.getConditionalElement(XPATH_isVerifyPhoneNumber) != False:
            #verify a phone number

            #enter phone number
            XPATH_REGIONDROPDOWN = "//div[@id='countryList']//div[@role='combobox']"
            XPATH_UK = '''//ul[@role='listbox'][@aria-label='Select a country']//span[contains(text(), "United Kingdom (+44)")]'''
            XPATH_NUMBERINPUT = "//input[@id='phoneNumberId']"
            XPATH_NEXTBUTTON = '''//span[contains(text(),"Next")]/ancestor::button[1]'''

            XPATH_ONINVALIDPHONE_SVGICON = "//*[local-name() = 'svg'][@fill='currentColor'][@focusable='false']" #use this icon to detect when an error occurs with an inputted phone number
            XPATH_ERRORMESSAGEDIV = f"{XPATH_ONINVALIDPHONE_SVGICON}/ancestor::div[1]" #the div containing the error message text

            #XPATH verify code
            XPATH_VERIFCODEINP = "//input[@type='tel'][@name='code']" 

            #XPATH personal details
            v_DOBDAY = "12"
            v_DOBMONTH = "4"
            v_DOBYEAR = "1990"

            XPATH_RECOVERYPHONE = "//input[@type='tel'][@id='phoneNumberId']"
            XPATH_DOBDAY = "//input[@type='tel'][@id='day']"
            XPATH_DOBMONTHDROPDOWN = "//select[@id='month']"
            XPATH_DOBMONTHSELECTION = f"{XPATH_DOBMONTHDROPDOWN}//option[@value={v_DOBMONTH}]"
            XPATH_DOBYEAR = "//input[@type='tel'][@id='year']"
            XPATH_GENDERDROPDOWN = "//select[@id='gender']"
            XPATH_GENDERSELECTION = "//select[@id='gender']//option[@value='1']"
            XPATH_NEXTBUTTON = '''//span[contains(text(),"Next")]/ancestor::button[1]'''



            REGION_DROPDOWN = driver.find_element(By.XPATH,XPATH_REGIONDROPDOWN)
            REGION_SELECTION = driver.find_element(By.XPATH,XPATH_UK)
            NUMBERINPUT = driver.find_element(By.XPATH,XPATH_NUMBERINPUT)
            NEXTBUTTON = driver.find_element(By.XPATH,XPATH_NEXTBUTTON)
            
            self.z.pause()
            REGION_DROPDOWN.click()
            self.z.pause(2500,3500)
            REGION_SELECTION.click()
            self.z.pause()
            
            #use default phone number, if denied require user input.
            phoneNumberAccepted = False
            while phoneNumberAccepted == False:
                self.z.realClearField(NUMBERINPUT)
                self.z.pause()
                self.z.realSendKeys(NUMBERINPUT,phoneNumber)
                self.z.pause(shortened=True)
                NUMBERINPUT.send_keys("\n")

                # WebDriverWait(driver,10).until( #wait until the page has updated after button click. (either element from next stage is present or failure trigger element is)
                #     EC.any_of(
                #             EC.presence_of_element_located((By.XPATH,XPATH_ONINVALIDPHONE_SVGICON)),
                #             EC.presence_of_element_located((By.XPATH,XPATH_VERIFCODEINP))
                #         )
                # )

                ### ***FIX THIS*** ###
                # HARD CODED SLEEP TO AWAIT FOR PAGE UPDATE

                print("tiem sleep")
                time.sleep(10)
                print("time")


                print("sleeping")
                self.z.pause(7000,8000) 
                print("slept")

                ERRORICON = self.z.getConditionalElement(XPATH_ONINVALIDPHONE_SVGICON)

                if ERRORICON != False:
                    errorMessage = driver.find_element(By.XPATH,XPATH_ERRORMESSAGEDIV).get_attribute("innerText")
                    self.z.alterElemAttribute(XPATH_ONINVALIDPHONE_SVGICON,"focusable","true") #change focusable attribute (focusable because it is a condition of the xpath used) of invalid phone number icon, so conditional element will not trigger unless element is refreshed to have default value (if another valid phone number is inputted)
                    print(f"phone number denied. Reason:\n'{errorMessage}'")
                    
                    valid = False #check phone number is in valid format before attempting to type it to google
                    while not valid:
                        phoneNumber = input("enter phone number:\n>>")
                        if len(phoneNumber) == 11 and phoneNumber.isnumeric():
                            valid = True
                        else:
                            print("invalid number format.")

                else:
                    phoneNumberAccepted = True


            #enter verification code
            VERIFCODEINP = driver.find_element(By.XPATH,XPATH_VERIFCODEINP)


            veriCodeAccepted = False
            while not veriCodeAccepted: #while verification has not been accepted.

                validFormat = False #while a correctly formatted verification code has not been inputted
                while not validFormat:
                    verifCode = input("enter code:\n>>")
                    if len(verifCode) == 6 and verifCode.isnumeric():
                        validFormat = True
                    else:
                        print("invalid verification code format.")


                self.z.pause(shortened=True)
                self.z.realSendKeys(VERIFCODEINP,verifCode)
                self.z.pause()
                VERIFCODEINP.send_keys("\n")

                # WebDriverWait(driver,10).until( #wait until the page has updated after button click. (either element from next stage is present or failure trigger element is)
                #     EC.any_of(
                #             EC.presence_of_element_located((By.XPATH,XPATH_ONINVALIDPHONE_SVGICON)),
                #             EC.presence_of_element_located((By.XPATH,XPATH_DOBDAY))
                #         )
                # )

                ### ***FIX THIS*** ###
                # HARD CODED SLEEP TO AWAIT FOR PAGE UPDATE
                
                print("sleeping.")
                time.sleep(10)
                print("slept.")

                INVALID = self.z.getConditionalElement(XPATH_ONINVALIDPHONE_SVGICON)

                if INVALID != False: #verification failed
                    errorMessage = driver.find_element(By.XPATH,XPATH_ERRORMESSAGEDIV).get_attribute("innerText")
                    self.z.alterElemAttribute(XPATH_ONINVALIDPHONE_SVGICON,"focusable","true")
                    print(f"verification code not accepted. Reason: '{errorMessage}'")
                    self.z.realClearField(VERIFCODEINP)
                else:
                    veriCodeAccepted = True

            #welcome to google screen (DOB gender)
            RECOVERYPHONE = driver.find_element(By.XPATH,XPATH_RECOVERYPHONE)
            DOBDAY = driver.find_element(By.XPATH,XPATH_DOBDAY)
            DOBMONTHDROPDOWN = driver.find_element(By.XPATH,XPATH_DOBMONTHDROPDOWN)
            DOBMONTHSELECTION = driver.find_element(By.XPATH,XPATH_DOBMONTHSELECTION)
            DOBYEAR = driver.find_element(By.XPATH,XPATH_DOBYEAR)
            GENDERDROPDOWN = driver.find_element(By.XPATH,XPATH_GENDERDROPDOWN)
            GENDERSELECTION = driver.find_element(By.XPATH,XPATH_GENDERSELECTION)
            NEXTBUTTON = driver.find_element(By.XPATH,XPATH_NEXTBUTTON)


            #clear recovery phone
            self.z.pause()
            RECOVERYPHONE.click()
            self.z.pause(shortened=True)

            self.z.realClearField(RECOVERYPHONE)

            #enter date of birth
            self.z.pause()
            self.z.realSendKeys(DOBDAY,v_DOBDAY)
            self.z.pause()
            DOBMONTHDROPDOWN.click()
            self.z.pause()
            DOBMONTHSELECTION.click()
            self.z.pause()
            self.z.realSendKeys(DOBYEAR,v_DOBYEAR)
            self.z.pause()

            #select gender
            GENDERDROPDOWN.click()
            self.z.pause()
            GENDERSELECTION.click()
            self.z.pause()

            NEXTBUTTON.click()


            #personaltion settings
            XPATH_EXPRESSPRSN = "//div[@role='radiogroup']//div[@role='radio'][@data-value='1']"
            
            EXPRESSPRSN = driver.find_element(By.XPATH,XPATH_EXPRESSPRSN)

            self.z.pause(3000,4000)
            EXPRESSPRSN.click()
            self.z.pause()

            NEXTBUTTON2 = driver.find_element(By.XPATH,XPATH_NEXTBUTTON)
            NEXTBUTTON2.click()

            #CONFIRM COOKIE SETTINGS
            XPATH_CONFIRMBUTTON = '//span[contains(text(),"Confirm")]/ancestor::button[1]'
            CONFIRMBUTTON = driver.find_element(By.XPATH,XPATH_CONFIRMBUTTON)
            
            self.z.pause(4000,5000)
            CONFIRMBUTTON.click()

            #agree to TOS
            XPATH_AGREEBUTTON = '//span[contains(text(),"I agree")]/ancestor::button[1]'
            AGREEBUTTON = driver.find_element(By.XPATH,XPATH_AGREEBUTTON)
            self.z.pause(4000,5000)
            AGREEBUTTON.click()
            

            
        print("sign up complete.")

        with open("emails.txt","w+") as f:
            f.write(f"{email}\n")






        


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

    def __generateEmailAddress(self,fname : str,lname : str):
        first = fname[0:: 1 if random.randint(0,1) == 1 else -1]
        last = lname
        numbers = "".join(random.choices(string.digits,k=random.randint(3,5)))
        return f"{first}{last}{numbers}"




