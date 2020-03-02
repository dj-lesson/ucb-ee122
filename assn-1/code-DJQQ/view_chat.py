# coding=gbk
from Tkinter import *
from socket import *
import thread
import time


class ChatView(Frame):
    def changeActive(self):
        self.isActive=False
        self.master.destroy()
    def sendmessage(self):
        # 在聊天内容上方加一行 显示发送人及发送时间
        #  [8:19] name  [20:] message
        data='sending:'+self.friendname+':'+self.text_msg.get('0.0', END)
        chat_ADDR = ('localhost', 21567)
        chatudpCliSock = socket(AF_INET, SOCK_DGRAM)
        if data:
            chatudpCliSock.sendto(data, chat_ADDR)
            data, ADDR = chatudpCliSock.recvfrom(1024)

        if data == '03:01' or data == '03:02':
            msgcontent = unicode('我:', 'eucgb2312_cn') + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + '\n '
            self.text_msglist.insert(END, msgcontent, 'green')
            self.text_msglist.insert(END, self.text_msg.get('0.0', END))
            self.text_msg.delete('0.0', END)
        if data == '03:01':
            self.text_isActive.delete('0.0',END)
            self.text_isActive.insert(1.0, 'on line!')
        elif data == '03:02':
            self.text_isActive.insert(1.0, 'not on line!')

    def recvmessage(self):
        chat_ADDR = ('localhost', 21567)
        chatudpCliSock = socket(AF_INET, SOCK_DGRAM)
        while True:
            time.sleep(2)
            data = self.friendname
            chatudpCliSock.sendto(data, chat_ADDR)
            data, ADDR = chatudpCliSock.recvfrom(1024)
            print '----receive from localhost:'+data
            if data:
                msgcontent =unicode(data[3:35], 'eucgb2312_cn') + '\n '
                self.text_msglist.insert(END, msgcontent, 'green')
                self.text_msglist.insert(END, data[36:] + '\n')

    def __init__(self, friendname, hostname, master=None):
        self.friendname = friendname
        self.hostname=hostname
        self.isActive = True


        root = Tk()
        self.frame_left_top = Frame(root,width=380, height=300, bg='white')
        self.frame_left_center = Frame(root,width=380, height=100, bg='white')
        self.frame_left_bottom = Frame(root,width=380, height=30)
        self.frame_right = Frame(root,width=170, height=400, bg='white')
        # # 创建需要的几个元素
        self.text_isActive = Text(self.frame_right)
        self.text_msglist = Text(self.frame_left_top)
        self.text_msg = Text(self.frame_left_center)
        self.button_sendmsg = Button(self.frame_left_bottom, text=unicode('发送', 'eucgb2312_cn'),
                                     command=self.sendmessage)
        # 创建一个绿色的tag
        self.text_msglist.tag_config('green', foreground='#008B00')
        # 使用grid设置各个容器位置
        self.frame_left_top.grid(row=0, column=0, padx=2, pady=5)
        self.frame_left_center.grid(row=1, column=0, padx=2, pady=5)
        self.frame_left_bottom.grid(row=2, column=0)
        self.frame_right.grid(row=0, column=1, rowspan=3, padx=4, pady=5)
        self.frame_left_top.grid_propagate(0)
        self.frame_left_center.grid_propagate(0)
        self.frame_left_bottom.grid_propagate(0)
        self.frame_right.grid_propagate(0)
        # 把元素填充进frame
        self.text_isActive.grid()
        self.text_isActive.insert(1.0,'not sure')

        self.text_msglist.grid()
        self.text_msg.grid()
        self.button_sendmsg.grid(sticky=E)
        Frame.__init__(self, root, padx=90, pady=60)
        self.master.iconbitmap('andj_icon.ico')
        self.master.title(unicode('与', 'eucgb2312_cn') + self.friendname + unicode('聊天中', 'eucgb2312_cn'))
        self.master.protocol('WM_DELETE_WINDOW', self.changeActive)
        thread.start_new_thread(self.recvmessage, ())