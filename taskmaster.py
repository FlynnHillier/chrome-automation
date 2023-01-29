import json
from proxies import Proxy
import os

class TaskMaster:
    def __init__(self,json:str="browserProfiles.json",phones:str = "phones.txt",proxies:str = "proxies.txt") -> None:
        self.paths = {
            "proxies":proxies,
            "phones":phones,
            "browserProfiles":json,
        }

        self.active = {
            "phone":None,
            "proxy":None,
            "useCount":0,
        }

        self.phones = []
        self.proxies = []

        if not os.path.exists(self.paths["browserProfiles"]):
            self.__createBaseProfilesJson()

        self.refresh()

        if self.__isBlankProfileActive():
            self.rotateActiveBrowserProfile()

    def incrementUseCount(self):
        self.active["useCount"] += 1
        self.__updateActiveProfileInFile()
    


    def refresh(self):
        self.__loadProxies()
        self.__loadPhones()
        self.__loadActiveBrowserProfile()

    def getActiveProxy(self) -> Proxy:
        return self.active["proxy"]

    def getActivePhone(self) -> str:
        return self.active["phone"]


    def rotateActiveBrowserProfile(self):
        self.refresh()
        if len(self.phones) == 0:
            raise BaseException("no remaining phone numbers.")
        
        if len(self.proxies) == 0:
            raise BaseException("no remaining proxies")

        with open(self.paths["browserProfiles"], 'r') as j:
            browserProfileData = json.loads(j.read())

        inUseProfile = browserProfileData["active"]

        if inUseProfile["phone"] != "" and inUseProfile["proxy"] != "": #not first time load
            print("not first time load")
            browserProfileData["utilised"].append(inUseProfile)
        
        newPhone = self.getAvailablePhone()
        newProxy = self.getAvailableProxy()

        self.__deletePhoneFromFile(newPhone)
        self.__deleteProxyFromFile(newProxy)

        browserProfileData["active"] = {
            "phone":newPhone,
            "proxy":newProxy.string(),
            "useCount":0
        }

        self.__updateProfilesJson(browserProfileData)

        self.active = {
            "phone":newPhone,
            "proxy":newProxy,
            "useCount":0
        }


    def getAvailablePhone(self):
        if len(self.phones) == 0:
            raise BaseException("no available phone numbers")
        
        return self.phones[0]
    
    def getAvailableProxy(self) -> Proxy:
        if len(self.proxies) == 0:
            raise BaseException("no available proxies")
        
        return self.proxies[0]

        
    def __deletePhoneFromFile(self,phone :str ):
        with open(self.paths["phones"],"r") as f:
            phones = f.readlines()
            out = []
            for index,phonenumber in enumerate(phones):
                if not phonenumber.rstrip("\n") == phone:
                    out.append(phonenumber)
        
        with open(self.paths["phones"],"w+") as f:
            f.writelines(out)

    
    def __deleteProxyFromFile(self,proxy:Proxy ):
        with open(self.paths["proxies"],"r") as f:
            proxies = f.readlines()
        out = []
        for index,Aproxy in enumerate(proxies):
            if not proxy.string() == Aproxy.rstrip("\n"):
                out.append(Aproxy)
        
        with open(self.paths["proxies"],"w+") as f:
            f.writelines(out)



    def __loadActiveBrowserProfile(self):
        with open(self.paths["browserProfiles"],"r") as f:
            data = json.load(f)
        self.active = data["active"]
        if not self.active["proxy"] == "":
            self.active["proxy"] = self.__getProxyDetails(self.active["proxy"])

    def __createBaseProfilesJson(self):
        base = {
            "active":{
                "phone":"",
                "proxy":"",
                "useCount":0,
            },
            "utilised":[]
        }

        self.__updateProfilesJson(base)

    def __updateActiveProfileInFile(self) -> None:
        with open(self.paths["browserProfiles"],"r") as f:
            existingData = json.loads(f.read())
        
        existingData["active"] = self.active

        with open(self.paths["browserProfiles"],"w+") as f:
            f.write(json.dumps(existingData,indent="\t"))

    def __updateProfilesJson(self,jsonData:object):
        with open(self.paths["browserProfiles"],"w+") as f:
            f.write(json.dumps(jsonData,indent="\t"))

    def __loadProxies(self) -> list:    
        with open(self.paths["proxies"],"r") as f:
            proxies = f.readlines()
            for index,proxy in enumerate(proxies):
                proxies[index] = self.__getProxyDetails(proxy.rstrip("\n"))

        self.proxies = proxies
        return proxies

    def __loadPhones(self) -> list[str]:
        with open(self.paths["phones"],"r") as f:
            phones = f.readlines()
            for index,phonenumber in enumerate(phones):
                phones[index] = phonenumber.rstrip("\n")

        self.phones = phones
        return phones


    def __getProxyDetails(self,proxyString:str) -> Proxy:
        if not proxyString.count(":") == 3:
            raise BaseException("invalid proxy string.")

        [host,port,user,password] = proxyString.split(":")

        return Proxy(host,port,user,password)

    def __isBlankProfileActive(self) -> bool:
        return self.active["phone"] == "" or self.active["proxy"] == ""
