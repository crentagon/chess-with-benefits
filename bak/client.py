from socket import *
HOST = 'localhost'
PORT = 28888
BUFSIZE = 1024
ADDR = (HOST, PORT)
tcpTimeClientSock = socket(AF_INET, SOCK_STREAM)
tcpTimeClientSock.connect(ADDR)
while True:
  data = raw_input('> ')
  if not data:
      break
  tcpTimeClientSock.send(data)
  data = tcpTimeClientSock.recv(BUFSIZE)
  print data
  if not data:
      break
tcpTimeClientSock.close()