# coding=utf-8
from view_sign_up import SignUPApplication
from Tkinter import *
from socket import *
import tkMessageBox


class SignINApplication(Frame):
    def __init__(self, ADDR, udpCliSock, master=None):
        self.ADDR = ADDR
        self.udpCliSock = udpCliSock
        self.isSigned = False
        Frame.__init__(self, master, padx=90, pady=60)
        self.pack()
        self.master.iconbitmap('andj_icon.ico')
        self.createWidgets()

        self.master.title('Sign in')

    def createWidgets(self):
        self.hostname = ''

        self.hint_name_label = Label(self, text='账号：')
        self.hint_name_label.pack()

        self.nameInput = Entry(self)
        self.nameInput.pack()

        self.nameInput.insert(0, '20161002884')

        self.hint_password_label = Label(self, text='密码：')
        self.hint_password_label.pack()

        self.passwordInput = Entry(self)
        self.passwordInput.pack()

        self.passwordInput.insert(0, '363787')

        self.alertButton = Button(self, text='登录', command=self.sign_in)
        self.alertButton.pack()

        self.alertButton = Button(self, text='注册', command=self.sign_up)
        self.alertButton.pack()

        self.destoryButton = Button(self, text='关闭', command=self.master.destroy)
        self.destoryButton.pack()

    def sign_in(self):
        name = self.nameInput.get()
        print name
        password = self.passwordInput.get()
        print password
        data = '02#' + name + '#' + password + '#'
        print data
        self.udpCliSock.sendto(data, self.ADDR)
        data, ADDR = self.udpCliSock.recvfrom(1024)
        print data

        if data == '02:01':
            tkMessageBox.showinfo('Message', '登录成功！')
            self.hostname=self.nameInput.get()
            self.isSigned = True

        elif data == '02:02':
            tkMessageBox.showinfo('Message', '密码错误！')
        elif data == '02:03':
            tkMessageBox.showinfo('Message', '用户不存在！')
        elif data == '02:04':
            tkMessageBox.showinfo('Message', '用户已登录！')
            self.hostname=self.nameInput.get()
            self.isSigned = True
        if self.isSigned:
            self.master.destroy()

    def sign_up(self):
        root = Tk()

        s = SignUPApplication(root)

        s.master.title('sign up')
        s.mainloop()
