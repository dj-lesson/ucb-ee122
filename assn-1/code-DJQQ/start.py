# coding=utf-8
# the start of this software
from Tkinter import *
from socket import *

from view_main import MainView
from view_sign_in import SignINApplication

# main address and main udp socket object
ADDR = ('202.114.196.97', 21568)
udpCliSock = socket(AF_INET, SOCK_DGRAM)
# login view
root = Tk()
app = SignINApplication(ADDR, udpCliSock, root)
app.mainloop()
# get the status of signing. is signed or not.
isSigned = app.isSigned

root = Tk()
if isSigned:
    # open the main view
    print 'sign successful'
    # app.hostname is the name of logging in
    print app.hostname
    mainview = MainView(ADDR, udpCliSock, app.hostname, root)
    mainview.mainloop()
else:
    # signed in failed
    print 'sign failed'
# unbind the current hostname.
data = '06#'
udpCliSock.sendto(data, ADDR)
data, ADDR = udpCliSock.recvfrom(1024)
print data
udpCliSock.close()
print 'all stop'
