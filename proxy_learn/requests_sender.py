#coding=utf8

import sys
import json
import requests

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
    #url = 'http://www.baidu.com'
    url = 'http://httpbin.org/get'
    r = requests.get(url, proxies=proxies)
    print r.text

main()
