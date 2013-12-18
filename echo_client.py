import socket, sys

HOST = '192.168.0.35' # sshqn sshdb
PORT = 8000 
buf_size = 1

def get_reply(soc):
    reply = ''
    while 1:
        temp = soc.recv(buf_size)
        if not temp:
            break
        reply += temp
    return reply

soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
soc.bind(('', 6060)) # without this, random port will be assigned
soc.connect((HOST, PORT))
msg = sys.argv[1]
soc.sendall(msg)
#reply = soc.recv(buf_size) # socket.error: [Errno 104] Connection reset by peer
reply = get_reply(soc)
print '%s=%s' % (msg, reply[:1])
soc.close()

