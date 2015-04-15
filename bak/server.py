from socket import *
# from time import ctime
import time
HOST = 'localhost'
PORT = 28888
BUFSIZE = 1024
ADDR = (HOST, PORT)

tcpTimeSrvrSock = socket(AF_INET,SOCK_STREAM)
tcpTimeSrvrSock.bind(ADDR)
tcpTimeSrvrSock.listen(50)

while True:
  print 'waiting for connection...'
  tcpTimeClientSock, addr = tcpTimeSrvrSock.accept()
  print '...connected from:', addr
  time.sleep(2)
  tcpTimeClientSock.send('test')

  # while True:
  #   data = tcpTimeClientSock.recv(BUFSIZE)
  #   if not data:
  #     break
  #   tcpTimeClientSock.send('test')
  #   print 'test'
    
  tcpTimeClientSock.close()
tcpTimeSrvrSock.close() 