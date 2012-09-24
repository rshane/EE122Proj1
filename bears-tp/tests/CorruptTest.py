import random
import BasicSender
import Checksum
from BasicSender import *
from BasicTest import *
DEBUG = 1

"""
This tests random packet corruption and zombie hordes
"""

class CorruptTest(BasicTest):
    def handle_packet(self):
        for p in self.forwarder.in_queue:
            p_type = p.msg_type
            p_no = p.seqno
            if p_type == 'ack':
                if DEBUG:
                    import pdb; pdb.set_trace()                                
                if random.choice([True, True]):
                    p.update_packet(msg_type=p_type, seqno=p_no, data='corrupt', full_packet=None,  update_checksum=False)
                    valid = Checksum.validate_checksum(p)
                    self.forwarder.out_queue.append(p)
            else:
                self.forwarder.out_queue.append(p)
        #empty out in_queue
        self.forwarder.in_queue = []
