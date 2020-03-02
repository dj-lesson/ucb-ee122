import random

from BasicTest import *

"""
This tests random packet drops and random cause packet checksum error.
"""


class AllCaseTest(BasicTest):
    def handle_packet(self):
        for p in self.forwarder.in_queue:
            if random.choice([True, False]):
                # print "AnDJ-AllCaseTest: drop this packet"
                if random.choice([True, False]):
                    p.checksum = str(int(p.checksum) - 1)
                    # print 'AnDJ-AllCaseTest: change packet checksum',
                # else:
                # print 'AnDJ-AllCaseTest: not change packet checksum',
                self.forwarder.out_queue.append(p)

        # empty out the in_queue
        self.forwarder.in_queue = []
