import random

from BasicTest import *

"""
This tests random cause packet checksum error.
"""


class PacketCheckErrTest(BasicTest):
    def handle_packet(self):
        for p in self.forwarder.in_queue:
            if random.choice([True, False]):
                p.checksum = str(int(p.checksum)-1)
                # print 'AnDJ-PacketCheckErrTest: change packet checksum',
            # else:
                # print 'AnDJ-PacketCheckErrTest: not change packet checksum',

            self.forwarder.out_queue.append(p)
        # empty out the in_queue
        self.forwarder.in_queue = []
