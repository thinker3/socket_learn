import socket, time

host = 'www.baidu.com'
port = 80
#message = "GET / HTTP/1.1\r\n\r\n" # HTTP/1.1 302 Moved Temporarily
#message = "GET http://www.baidu.com/ HTTP/1.1\r\nHost: www.baidu.com\r\nUser-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:26.0) Gecko/20100101 Firefox/26.0\r\nConnection: keep-alive\r\n\r\n" # socket.error: [Errno 104] Connection reset by peer
message = "GET / HTTP/1.1\r\nHost: www.baidu.com\r\nUser-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:26.0) Gecko/20100101 Firefox/26.0\r\nConnection: keep-alive\r\n\r\n"

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ip = socket.gethostbyname(host)
print ip
s.connect((ip, port))
s.sendall(message)
#time.sleep(1)
reply = s.recv(100 * 1024)
print reply
s.close()


print '-' * 100
s = socket.create_connection((host, port))
s.sendall(message)
time.sleep(1)
reply = s.recv(100 * 1024)
print reply
s.close()
