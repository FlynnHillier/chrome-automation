from os import path

class Proxy:
    def __init__(self,host:str,port:str,user:str,password:str):
        self.host = host
        self.port = port
        self.user = user
        self.password = password

    def string(self):
        return f"{self.host}:{self.port}:{self.user}:{self.password}"


def loadProxies(filepath:str = path.join(path.dirname(__file__),"proxies.txt")) -> list:
    if not path.isfile(filepath):
        raise BaseException(f"could not locate file: {filepath}")
    
    with open(filepath) as f:
        proxies = f.readlines()
        for index,proxy in enumerate(proxies):
            proxies[index] = getProxyDetails(proxy.rstrip("\n"))

            
    if len(proxies) == 0:
        raise BaseException(f"no proxies found in file {filepath}")


    return proxies


def getProxyDetails(proxyString:str) -> Proxy:
    if not proxyString.count(":") == 3:
        raise BaseException("invalid proxy string.")

    [host,port,user,password] = proxyString.split(":")

    return Proxy(host,port,user,password)