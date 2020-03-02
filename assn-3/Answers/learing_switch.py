from sim.api import *
from sim.basics import *

'''
Create your RIP router in this file.
'''


class LearningSwitch(Entity):
    def __init__(self):
        # Add your code here!
        self.switchTable = {}
        pass

    def handle_rx(self, packet, port):
        if packet.__class__.__name__ == 'DiscoveryPacket':
            self.switchTable[packet.src] = port
            self.send(packet, port, flood=True)
        else:
            if self.switchTable.has_key(packet.dst):
                if self.switchTable[packet.dst] == port:
                    pass
                else:
                    self.send(packet, self.switchTable[packet.dst])
            else:
                self.send(packet, port, flood=True)
#        raise NotImplementedError
