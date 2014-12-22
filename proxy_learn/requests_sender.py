#coding=utf8

import os
import sys
import json
import requests

home = os.path.expanduser('~')
proxy = 'http://localhost:8080'
proxies = {
    # requests.exceptions.MissingSchema: Proxy URLs must have explicit schemes.
    #'http': 'localhost:8080',
    'http': proxy,
}
payload = {'key1': 'value1', 'key2': 'value2'}
headers = {'content-type': 'application/json'}


def main():
    if sys.argv[1:]:
        if sys.argv[1] in ['p', 'post']:
            url = 'http://httpbin.org/post'
            r = requests.post(url, data=json.dumps(payload), headers=headers, proxies=proxies)
            print r.text
            return
        if sys.argv[1] in ['c', 'connect']:
            url = 'https://www.paypal.com'
            url = 'https://www.paypal.com/c2/webapps/mpp/home'
            os.environ['https_proxy'] = proxy
            output = os.path.join(home, 'paypal.index.html')
            cmd = 'wget %s -O %s' % (url, output)  # not -o, which is log
            if sys.platform == 'win32':
                cmd += ' --ca-certificate=cacert.pem'
            os.system(cmd)
            '''
            r = requests.get(url, proxies=proxies)
            print r.status_code
            print r.headers
            '''
            return
    #url = 'http://www.baidu.com'
    url = 'http://httpbin.org/get'
    r = requests.get(url, proxies=proxies)
    print r.text

main()
