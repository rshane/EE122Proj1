import random
import BasicSender
from BasicSender import *
from BasicTest import *

"""
This tests random packet corruption and zombie hordes
"""

class CorruptTest(BasicTest):
    def handle_packet(self):
        for p in self.forwarder.in_queue:
            p_type = p.msg_type
            p_no = p.seqno
            
            if random.choice([True, True]):
                p.update_packet(msg_type=p_type, seqno=p_no, data='corrupt', full_packet=p,  update_checksum=False)
                self.forwarder.out_queue.append(p)
            else:
                self.forwarder.out_queue.append(p)
        #empty out in_queue
        self.forwarder.in_queue = []
