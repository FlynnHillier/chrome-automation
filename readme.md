## setup
- run the command: ***pip install -r requirements.txt***
- create files: ***'proxies.txt'*** & ***'phones.txt'***
- populate each file with appropriate contents
    - Proxies.txt line format - '*\<host>*:*\<port>*:*\<username>*:*\<password>*'
    - phones.txt - phone number on each line
- provided phone numbers will be used to recieve SMS verification codes sent during google signup.
- edit the key strings within index.py
- run index.py and start genning accounts
- to switch to a new profile ( a different phone number & proxy ), send a keyboard interrupt ( CTRL + C ) during run time and enter the character 'Y' when prompted.