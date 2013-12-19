import socket, time

news = ('news.163.com', 80)
baidu = ('www.baidu.com', 80)
github = ('github.com', 443)
twitter = ('twitter.com', 443)

timeout = 10
buf_size = 8192 
delimiter = '\r\n'
proxy_addr = ('localhost', 8080)

class Fetcher(object):
    def __init__(self, target_addr):
        self.target_addr = target_addr
        self.host, self.port = target_addr
        self.sock = socket.create_connection(proxy_addr, timeout)

    def fetch(self):
        request = '''
        GET http://%s/ HTTP/1.1
        Host: %s
        User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:26.0) Gecko/20100101 Firefox/26.0
        Connection: Close 
        ''' % (self.host, self.host)
        self.init_request(request)
        try:
            self.sock.sendall(self.request)
            data = self.get_data()
            print data[-1000:]
        except Exception as e:
            print e

    def get_data(self):
        data = ''
        try:
            while 1:
                temp = self.sock.recv(buf_size) # sometimes blocking even no data left, until timeout, strange
                if not temp:
                    break
                data += temp
        except Exception as e:
            print e
        finally:
            return data

    def connect(self):
        request = '''
        CONNECT %s:%s HTTP/1.1
        User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:26.0) Gecko/20100101 Firefox/26.0
        Proxy-Connection: keep-alive
        Connection: keep-alive
        Host: %s 
        ''' % (self.host, self.port, self.host)
        self.init_request(request)
        try:
            self.sock.sendall(self.request)
            data = self.get_data()
            print data
        except Exception as e:
            print e

    def init_request(self, request):
        line = ''
        for one in request.split('\n'):
            one = one.strip()
            if one:
                line += one + delimiter
        line += delimiter
        self.request = line 

    def close(self):
        try:
            if self.sock:
                self.sock.close()
        except:
            pass

def fetch_test(target_addr):
    browser = Fetcher(target_addr)
    browser.fetch()
    browser.close()

def connect_test(target_addr):
    browser = Fetcher(target_addr)
    browser.connect()
    browser.fetch()
    browser.close()

if __name__ == '__main__':
    fetch_test(baidu)
    #connect_test(twitter)
















