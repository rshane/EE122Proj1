import random
import BasicSender
from BasicTest import *

"""
This tests random packet corruption and zombie hordes
"""

class CorruptTest(BasicTest):
    def handle_packets(self):
        for p in self.forwarder.in_queue:
            if random.choice([True, False]):
                p.update_packet(data="Sweet Baby Ray's", update_checksum=False)
            else:
                self.forwarder.out_queue.append(p)
        #empty out in_queue
        self.forwarder.in_queue = []
