# coding = utf-8
from socket import *

ADDR = ('202.114.196.97', 21568)
udpCliSock = socket(AF_INET, SOCK_DGRAM)
data = '02#20161002885#363787#'
udpCliSock.sendto(data, ADDR)
data, ADDR = udpCliSock.recvfrom(1024)
print data
data = '03#20161002884#hello1#'
udpCliSock.sendto(data, ADDR)
data, ADDR = udpCliSock.recvfrom(1024)
print data
data = '03#20161002884#hello2#'
udpCliSock.sendto(data, ADDR)
data, ADDR = udpCliSock.recvfrom(1024)
print data
data = '03#20161002884#hello3#'
udpCliSock.sendto(data, ADDR)
data, ADDR = udpCliSock.recvfrom(1024)
print data
data = '03#20161002884#hello4#'
udpCliSock.sendto(data, ADDR)
data, ADDR = udpCliSock.recvfrom(1024)
print data
data = '03#20161002884#hello5#'
udpCliSock.sendto(data, ADDR)
data, ADDR = udpCliSock.recvfrom(1024)
print data
data = '03#20161002884#hello6#'
udpCliSock.sendto(data, ADDR)
data, ADDR = udpCliSock.recvfrom(1024)
print data
data = '03#20161002884#hello7#'
udpCliSock.sendto(data, ADDR)
data, ADDR = udpCliSock.recvfrom(1024)
print data
data = '03#20161002884#hello8#'
udpCliSock.sendto(data, ADDR)
data, ADDR = udpCliSock.recvfrom(1024)
print data
data ='03#20161002884#hello9#'
udpCliSock.sendto(data, ADDR)
data, ADDR = udpCliSock.recvfrom(1024)
print data
data = '06#'
udpCliSock.sendto(data, ADDR)
data, ADDR = udpCliSock.recvfrom(1024)
print data
udpCliSock.close()

ADDR = ('202.114.196.97', 21568)
udpCliSock = socket(AF_INET, SOCK_DGRAM)
data = '02#20161002886#363787#'
udpCliSock.sendto(data, ADDR)
data, ADDR = udpCliSock.recvfrom(1024)
print data
data = '03#20161002884#hello1#'
udpCliSock.sendto(data, ADDR)
data, ADDR = udpCliSock.recvfrom(1024)
print data
data = '03#20161002884#hello2#'
udpCliSock.sendto(data, ADDR)
data, ADDR = udpCliSock.recvfrom(1024)
print data
data = '03#20161002884#hello3#'
udpCliSock.sendto(data, ADDR)
data, ADDR = udpCliSock.recvfrom(1024)
print data
data = '03#20161002884#hello4#'
udpCliSock.sendto(data, ADDR)
data, ADDR = udpCliSock.recvfrom(1024)
print data
data = '03#20161002884#hello5#'
udpCliSock.sendto(data, ADDR)
data, ADDR = udpCliSock.recvfrom(1024)
print data
data = '03#20161002884#hello6#'
udpCliSock.sendto(data, ADDR)
data, ADDR = udpCliSock.recvfrom(1024)
print data
data = '03#20161002884#hello7#'
udpCliSock.sendto(data, ADDR)
data, ADDR = udpCliSock.recvfrom(1024)
print data
data = '03#20161002884#hello8#'
udpCliSock.sendto(data, ADDR)
data, ADDR = udpCliSock.recvfrom(1024)
print data
data ='03#20161002884#hello9#'
udpCliSock.sendto(data, ADDR)
data, ADDR = udpCliSock.recvfrom(1024)
print data
data = '06#'
udpCliSock.sendto(data, ADDR)
data, ADDR = udpCliSock.recvfrom(1024)
print data
udpCliSock.close()