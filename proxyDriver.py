import os
import shutil
import undetected_chromedriver as uc
from proxies import Proxy

manifest_json = """
{
    "version": "1.0.1",
    "manifest_version": 2,
    "name": "Chrome Proxy",
    "permissions": [
        "proxy",
        "tabs",
        "unlimitedStorage",
        "storage",
        "<all_urls>",
        "webRequest",
        "webRequestBlocking"
    ],
    "background": {
        "scripts": ["background.js"]
    },
    "minimum_chrome_version":"22.0.0"
}
"""


def getProxyChromeDriver(proxy:Proxy,ExtensionFolderName="proxyExtension"):
    background_js = """
    var config = {
            mode: "fixed_servers",
            rules: {
            singleProxy: {
                scheme: "http",
                host: "%s",
                port: parseInt(%s)
            },
            bypassList: ["localhost"]
            }
        };

    chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});

    function callbackFn(details) {
        return {
            authCredentials: {
                username: "%s",
                password: "%s"
            }
        };
    }

    chrome.webRequest.onAuthRequired.addListener(
                callbackFn,
                {urls: ["<all_urls>"]},
                ['blocking']
    );
    """ % (proxy.host, proxy.port, proxy.user, proxy.password)

    chrome_options = uc.ChromeOptions()

    pluginPath = os.path.join(os.path.dirname(os.path.abspath(__file__)),ExtensionFolderName)

    if not os.path.isdir(pluginPath):
        os.mkdir(pluginPath)

    with open(os.path.join(pluginPath,"manifest.json"), "w") as f:
        f.write(manifest_json)
        f.close()
    with open(os.path.join(pluginPath,"background.js"), "w") as f:
        f.write(background_js)
        f.close()

    chrome_options.add_argument(f"--load-extension={','.join([pluginPath])}")


    driver = uc.Chrome(
        options=chrome_options,
        )

    shutil.rmtree(pluginPath)

    return driver