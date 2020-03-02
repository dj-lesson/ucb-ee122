import random
import sys
import getopt
import socket

import Checksum
import time
import BasicSender

'''
This is a skeleton sender class. Create a fantastic transport protocol here.
'''


class Sender:

    # Waits until packet is received to return.
    def receive(self, timeout=None):
        self.sock.settimeout(timeout)
        return self.sock.recv(4096)

    # Sends a packet to the destination address.
    def send(self, message, address=None):
        if address is None:
            address = (self.dest, self.dport)
        self.sock.sendto(message, address)

    # Prepares a packet
    def make_packet(self, msg_type, seqno, msg):
        body = "%s|%d|%s|" % (msg_type, seqno, msg)
        checksum = Checksum.generate_checksum(body)
        packet = "%s%s" % (body, checksum)
        return packet

    # Split the given packet
    def split_packet(self, message):
        pieces = message.split('|')
        msg_type, seqno = pieces[0:2]  # first two elements always treated as msg type and seqno
        checksum = pieces[-1]  # last is always treated as checksum
        data = '|'.join(pieces[2:-1])  # everything in between is considered data
        return msg_type, seqno, data, checksum

    # Handles a response from the receiver.
    def handle_response(self, response_packet):
        if Checksum.validate_checksum(response_packet):
            print "AnDJ-Sender: %s" % response_packet
        else:
            print "recv: %s <--- CHECKSUM FAILED" % response_packet

    def __init__(self, dest, port, filename, debug=False):
        self.debug = debug
        self.dest = dest
        self.dport = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.settimeout(None)  # blocking
        self.sock.bind(('', random.randint(10000, 40000)))
        if filename == None:
            self.infile = sys.stdin
        else:
            ###############################################################################
            # choice the read mode.
            # if the file which will be sent is just a text, you can choose the mode ("r")
            # if the file is not a text file, you have to choose the mode ("rb")
            ###############################################################################
            self.infile = open(filename, "r")
            # self.infile = open(filename, "rb")
            ###############################################################################

        self.sock.settimeout(0.5)
        self.istimeout = False
        # (Author: AnDJ) The unResponded packets. Size must be no more than 5.
        self.window = []
        # isreadall is stand for whether the file is read all.
        self.isreadall = False
        # reseadpacketno is stand for the packet number which will be sent again.
        self.resendpacketno = 0

    # handle the case which need read a packet from file to the window
    def handle_new_ack(self, ack):
        # print 'AnDJ-Sender: handle_new_ack'
        if self.isreadall:
            return
        if len(self.window) == 0:
            return
        msg_type, seqno, data, checksum = self.split_packet(self.window[len(self.window) - 1])

        msg = self.infile.read(4000)
        # print 'AnDJ-Sender: ----------read the file'
        msg_type = 'data'

        if msg == "":
            msg_type = 'end'
            packet = self.make_packet(msg_type, int(seqno) + 1, msg)
            self.window.append(packet)
            # print 'AnDJ-Sender: will send packet: %s|%d' % (msg_type, int(seqno) + 1)
            # print 'AnDJ-Sender: %s'% msg
            self.send(packet)
            self.resendpacketno = int(seqno) + 1
            self.isreadall = True

        else:
            packet = self.make_packet(msg_type, int(seqno) + 1, msg)
            self.window.append(packet)
            # print 'AnDJ-Sender: will send packet: %s|%d' % (msg_type, int(seqno) + 1)
            # print 'AnDJ-Sender: %s'% msg
            self.resendpacketno = int(seqno) + 1
            self.send(packet)

    # handle the duplicate case.
    def handle_dup_ack(self, ack):
        # print 'AnDJ-Sender: handle_dup_ack'
        msg_type, seqno, data, checksum = self.split_packet(self.window[0])

        length = int(ack) - int(seqno)

        for a in range(0, length):
            del self.window[0]
            self.handle_new_ack(a)

        packet = self.window[0]
        # print 'AnDJ-Sender: will RESEND packet: %s|%d' % (msg_type, int(seqno))
        self.send(packet)

    # Main sending loop.
    def start(self):
        # print "AnDJ-Sender: dport = ",
        # print self.dport

        # send 5 packets and store these 5 packets to window.
        frequent = 0
        while frequent != 5:
            msg = self.infile.read(4000)
            # print 'AnDJ-Sender: ----------read the file'
            msg_type = 'data'

            if msg == "":
                msg_type = 'end'
                packet = self.make_packet(msg_type, frequent, msg)
                self.window.append(packet)
                # print 'AnDJ-Sender: will send packet: %s|%d' % (msg_type, frequent)
                self.send(packet)
                self.isreadall = True
                break

            else:
                if frequent == 0:
                    msg_type = 'start'
                packet = self.make_packet(msg_type, frequent, msg)
                self.window.append(packet)
                # print 'AnDJ-Sender: will send packet: %s|%d' % (msg_type, frequent)
                self.send(packet)

            frequent = frequent + 1
        time.sleep(2)

        while len(self.window) != 0:
            try:
                response = self.receive(0.5)
                # print 'AnDJ-Sender: receive successful: message = ',
                # print response
                # self.handle_response(response)
                if not Checksum.validate_checksum(response):
                    print "AnDJ-Sender: %s" % 'checksum error'
                    continue
                expectno, checksum = self.split_ack_packet(response)[1:]
                if checksum:
                    # print 'AnDJ-Sender: start to handle the ack. new_ack or dup_ack'

                    msg_type, seqno, data, checksum = self.split_packet(self.window[0])

                    if int(expectno) - int(seqno) > 0:
                        # print '1'
                        self.skip_window(int(expectno) - int(seqno))
                    else:
                        # print '2'
                        self.handle_dup_ack(expectno)
                # print '--------------------------------------------------------'

            except socket.timeout:
                self.handle_timeout()

        self.infile.close()

    # skip the window from left to right by length step.
    def skip_window(self, length):
        for a in range(0, length):
            del self.window[0]
            self.handle_new_ack(a)

    # handle the timeout case which may be caused by packet loss or circle rote.
    def handle_timeout(self):

        # print 'AnDJ-Sender: timeout! resend packet!'

        msg_type, seqno, data, checksum = self.split_packet(self.window[0])
        if self.resendpacketno < int(seqno) or self.resendpacketno >= int(seqno) + len(self.window):
            self.resendpacketno = int(seqno)

        packet = self.window[int(self.resendpacketno) - int(seqno)]
        # print 'AnDJ-Sender: will RESEND packet: %s|%d' % (msg_type, int(self.resendpacketno))
        self.send(packet)

        # print '--------------------------------------------------------'
        pass

    # split the ack.
    def split_ack_packet(self, message):
        pieces = message.split('|')
        msg_type, expectno = pieces[0:2]  # first two elements always treated as msg type and seqno
        checksum = pieces[-1]  # last is always treated as checksum
        return msg_type, expectno, checksum

    def log(self, msg):
        if self.debug:
            print msg


'''
This will be run if you run this script from the command line. You should not
change any of this; the grader may rely on the behavior here to test your
submission.
'''
if __name__ == "__main__":
    def usage():
        print "BEARS-TP Sender"
        print "-f FILE | --file=FILE The file to transfer; if empty reads from STDIN"
        print "-p PORT | --port=PORT The destination port, defaults to 33122"
        print "-a ADDRESS | --address=ADDRESS The receiver address or hostname, defaults to localhost"
        print "-d | --debug Print debug messages"
        print "-h | --help Print this usage message"


    try:
        opts, args = getopt.getopt(sys.argv[1:],
                                   "f:p:a:d", ["file=", "port=", "address=", "debug="])
    except:
        usage()
        exit()

    port = 33122
    dest = "localhost"
    filename = None
    debug = False

    for o, a in opts:
        if o in ("-f", "--file="):
            filename = a
        elif o in ("-p", "--port="):
            port = int(a)
        elif o in ("-a", "--address="):
            dest = a
        elif o in ("-d", "--debug="):
            debug = True

    s = Sender(dest, port, filename, debug)
    try:
        s.start()
    except (KeyboardInterrupt, SystemExit):
        exit()
