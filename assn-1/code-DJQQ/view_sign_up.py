# coding=utf-8
from Tkinter import *
from socket import *
import tkMessageBox


class SignUPApplication(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master, padx=90, pady=60)
        self.pack()
        self.master.iconbitmap('andj_icon.ico')
        self.createWidgets()

    def createWidgets(self):


        self.hint_name_label = Label(self, text='账号：')
        self.hint_name_label.pack()

        self.nameInput = Entry(self)
        self.nameInput.pack()

        self.hint_password_label = Label(self, text='密码：')
        self.hint_password_label.pack()

        self.passwordInput = Entry(self)
        self.passwordInput.pack()

        self.hint_repeatpassword_label = Label(self, text='重复密码：')
        self.hint_repeatpassword_label.pack()

        self.repeatPasswordInput = Entry(self)
        self.repeatPasswordInput.pack()

        self.alertButton = Button(self, text='注册', command=self.sign_up)
        self.alertButton.pack()

    def sign_up(self):
        ADDR = ('202.114.196.97', 21568)
        udpCliSock = socket(AF_INET, SOCK_DGRAM)

        data = '01#'+self.nameInput.get()+'#'+self.passwordInput.get()+'#'
        data=data+self.repeatPasswordInput.get()+'#'
        udpCliSock.sendto(data, ADDR)
        data, ADDR = udpCliSock.recvfrom(1024)
        print data
        if data == '01:01':
            tkMessageBox.showinfo('Message', '注册成功！')
        elif data == '01:02':
            tkMessageBox.showinfo('Message', '两次密码输入不一致！')
        elif data == '01:03':
            tkMessageBox.showinfo('Message', '用户已存在！')
        udpCliSock.close()
