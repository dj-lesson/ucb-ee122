# coding=gbk
# the main view of this software including friends list
import Tkinter
from view_chat import ChatView
from socket import *
import time
import thread
import os


# the class of main view
class MainView(Tkinter.Frame):
    # ADDR is the socket address
    # udpCliSock is the udp socket object which input by start.py
    # hostname is the login host name
    def __init__(self, ADDR, udpCliSock, hostname, master):

        Tkinter.Frame.__init__(self, master, padx=10, pady=10)
        self.master.iconbitmap('andj_icon.ico')
        master.title("Sample Application")
        # store the address, udp socket object and hostname
        self.ADDR = ADDR
        self.udpCliSock = udpCliSock
        self.hostname = hostname
        # Set a minimum size through the master object, just to make our UI a little
        # nicer to look at.
        master.minsize(width=250, height=100)

        self.pack()

        # the list of current chatting windows during running
        self.chatwindows = []
        # friends are abstracted to a list of buttons
        self.buttons = []
        # the dictionary of message. the key is friend name. value is a list of messages corresponding friend name
        self.receivemessages = {}
        # create the friends list
        try:
            # if there is no config information of current hostname, create it.
            # the config information file formats like this: *.dj, txt document
            if not os.path.isfile(self.hostname + '.dj'):
                f = open(self.hostname + '.dj', 'w')
                f.close()
            # read this config file
            friendRF = open(self.hostname + '.dj', 'r')
            j = 0
            # read by line and create friends list.
            for line in friendRF.readlines():
                print line,
                line = line[:-1]
                self.receivemessages[line] = []
                button = Tkinter.Button(self.master, text=line)
                button.bind("<Button-1>", self.beginChat)
                self.buttons.append(button)
                self.buttons[j].pack()
                j = j + 1
            # create stranger chat button in the friends list
            self.receivemessages['stranger'] = []
            button = Tkinter.Button(self.master, text='stranger')
            button.bind("<Button-1>", self.beginChat)
            self.buttons.append(button)
            self.buttons[j].pack()

            # close config file
        finally:
            if friendRF:
                friendRF.close()
        # start the thread of receiving from the server
        thread.start_new_thread(self.recvmessage, ())
        # start the thread of sending message to chat window
        thread.start_new_thread(self.sendtochat, ())

    # the binded function of friend button
    def beginChat(self, event):
        friendname = event.widget['text']
        # event.widget['bg'] = '#FF0000'
        isExist = False
        for i in range(len(self.chatwindows)):
            if self.chatwindows[i].friendname == friendname and self.chatwindows[i].isActive:
                print friendname
                print self.chatwindows[i].friendname
                print self.chatwindows[i].isActive

                isExist = True
                break
        if isExist:
            print 'the chat window is exist and active'
        else:
            newchatview = ChatView(friendname, self.hostname)
            if friendname == 'stranger':
                newchatview.text_msg.destroy()
            self.chatwindows.append(newchatview)
            newchatview.mainloop()

    # This method creates a new window (which will be a child of the master of our frame,
    # not of our frame itself).  The quit window will ask the user if they really want to quit.
    # If the user clicks yes, the application will close.  If they say no, the quit window
    # will close.
    def create_quit_window(self):
        # The Toplevel class makes a window.  It's simpler than the Frame class.  We will make
        # it a child of our application's master object, but since it is a Toplevel object, it
        # will create a whole new window rather than one that is part of the application window.
        quit_window = Tkinter.Toplevel(self.master)
        # Give our quit window a title and minimum size.
        quit_window.title("Quit?")
        quit_window.minsize(width=150, height=50)
        # Display a message to the user asking if they want to quit.
        quit_label = Tkinter.Label(quit_window, text="Are you sure you want to quit?")
        quit_label.pack()
        # We give our window a yes and no button.  One quits the application and one quits
        # the window.
        yes_button = Tkinter.Button(quit_window, text="Yes", command=self.quit)
        yes_button.pack()
        no_button = Tkinter.Button(quit_window, text="No", command=quit_window.destroy)
        no_button.pack()

    def recvmessage(self):
        while True:
            data = '08#'
            time.sleep(2)
            print '###############start send to teacher'
            print '###############data :' + data
            self.udpCliSock.sendto(data, self.ADDR)
            print '###############start receive from teacher'
            data, ADDR = self.udpCliSock.recvfrom(1024)
            print '###############receive data :' + data

            data = int(data[3:])

            print data
            if data != 0:
                for i in range(data):
                    message = '09##'
                    self.udpCliSock.sendto(message, self.ADDR)
                    message, ADDR = self.udpCliSock.recvfrom(1024)

                    if str(message[1:2]) == '9':
                        fromname = message[3:14]
                        print '###############from name :' + fromname
                        # self.messages.append(message)
                        print message

                        if self.receivemessages.has_key(fromname):
                            self.receivemessages[fromname].append(message)
                        else:
                            self.receivemessages['stranger'].append(message)
                        # print self.messages
                        print self.receivemessages
            for (k, v) in self.receivemessages.items():
                if len(v) != 0:
                    for button in self.buttons:
                        if button['text'] == k:
                            button['bg'] = '#FF0000'
                else:
                    for button in self.buttons:
                        if button['text'] == k:
                            button['bg'] = '#FFFFFF'

    def sendtochat(self):
        time.sleep(2)
        ADDR = ('', 21567)
        udpSerSock = socket(AF_INET, SOCK_DGRAM)
        udpSerSock.bind(ADDR)
        while True:
            data, addr = udpSerSock.recvfrom(1024)
            print data[0:7]
            if data[0:7] == 'sending':
                print data[8:19]
                print data[21:]
                message = '03#' + data[8:19] + '#' + data[19:] + "#"
                self.udpCliSock.sendto(message, self.ADDR)
                message, ADDR = self.udpCliSock.recvfrom(1024)
                udpSerSock.sendto(message, addr)
                print message
                continue
            print '------------which one is request :' + data
            if len(self.receivemessages[data]) > 0:
                message = self.receivemessages[data].pop(0)
            else:
                message = ''
            udpSerSock.sendto(message, addr)
        udpSerSock.close()
