import socket, time

host = 'www.baidu.com'
port = 80
message = "GET / HTTP/1.1\r\n\r\n"

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ip = socket.gethostbyname(host)
print ip
s.connect((ip, port))
s.sendall(message)
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
