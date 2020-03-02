from sim.api import *
from sim.basics import *

'''
Create your RIP router in this file.
'''


class RIPRouter(Entity):
    def __init__(self):
        # table of distances and table of dst ports.
        self.switchTable = {}
        self.switchPort = {}
        pass

    def handle_rx(self, packet, port):
        # case for discovery packet.
        if isinstance(packet, DiscoveryPacket):
            # case for discovery sent by link-break.
            if packet.is_link_up == False and self.switchPort.has_key(packet.src):
                r = RoutingUpdate()
                # set every approach by "packet.src" step to inf.
                # if the minimum is changed, send the routing packet.
                for temp in self.switchTable[packet.src].keys():
                    # old min
                    min = self.switchTable[self.switchTable.keys()[0]][temp]
                    for k in self.switchTable.keys():
                        if self.switchTable[k][temp] < min:
                            min = self.switchTable[k][temp]

                    # set value
                    self.switchTable[packet.src][temp] = float("inf")

                    # new min
                    newmin = self.switchTable[self.switchTable.keys()[0]][temp]
                    for k in self.switchTable.keys():
                        if self.switchTable[k][temp] < newmin:
                            newmin = self.switchTable[k][temp]
                    # judge whether to send routing packet.
                    if min != newmin:
                        r.add_destination(temp, newmin)

                    r.add_destination(packet.src, float("inf"))
                self.send(r, port, True)

                return

            # case for this neighbor is exist.
            if self.switchTable.has_key(packet.src):
                return

            # add this neighbor.
            self.switchPort[packet.src] = port

            if len(self.switchTable) == 0:
                self.switchTable[packet.src] = {}
                l = self.switchTable.keys()[0]
            else:
                l = self.switchTable.keys()[0]
                self.switchTable[packet.src] = {}

            r = RoutingUpdate()

            # expand the table of distance by right and down.(-> and \|/)
            if len(self.switchTable) != 0:
                for key in self.switchTable[l].keys():
                    self.switchTable[packet.src][key] = float("inf")

            for key in self.switchTable.keys():
                self.switchTable[key][packet.src] = float("inf")

            self.switchTable[packet.src][packet.src] = 1

            # the update packet add one which destination is packet.src and distance is 1.
            r.add_destination(packet.src, 1)

            # send to all port.
            for port in range(0, self.get_port_count()):
                self.send(r, port, False)

        # case for routing update packet.
        elif isinstance(packet, RoutingUpdate):

            # isUpdate stores whether self need to send the update packet.
            isUpdate = False
            r = RoutingUpdate()

            # DV algorithms.
            for key in packet.all_dests():
                # not store itself.
                if key.name == self.name:
                    continue

                # case for the dest is a new node.
                if not self.switchTable[self.switchTable.keys()[0]].has_key(key):
                    isUpdate = True
                    for k in self.switchTable.keys():
                        self.switchTable[k][key] = float("inf")
                    self.switchTable[packet.src][key] = self.switchTable[packet.src][packet.src] + packet.get_distance(
                        key)
                    r.add_destination(key, self.switchTable[packet.src][key])
                    continue

                # case for the node is exist.

                # find the minimum distance in approaches which self to key.
                min = self.switchTable[self.switchTable.keys()[0]][key]
                for k in self.switchTable.keys():
                    if self.switchTable[k][key] < min:
                        min = self.switchTable[k][key]

                self.switchTable[packet.src][key] = self.switchTable[packet.src][packet.src] + packet.get_distance(key)

                if self.switchTable[packet.src][key] < min:
                    isUpdate = True
                    r.add_destination(key, self.switchTable[packet.src][key])

            if isUpdate:
                for port in range(0, self.get_port_count()):
                    self.send(r, port, False)
            pass
        else:
            # case for other packet like ping and pong.
            if self.switchTable[self.switchTable.keys()[0]].has_key(packet.dst):
                min = None
                k = None
                # find the valid port to send.
                for key in self.switchTable.keys():
                    if self.switchPort.has_key(key) and min == None:
                        min = self.switchTable[key][packet.dst]
                        k = key

                    if self.switchTable[key][packet.dst] < min and self.switchPort.has_key(key):
                        min = self.switchTable[key][packet.dst]
                        k = key
                self.send(packet, self.switchPort[k])
            pass
