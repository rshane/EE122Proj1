import sys
import getopt

import Checksum
import BasicSender

TIMEOUT     = 0.5 # in seconds
DEBUG       = 0
MSG_SIZE    = 1472 # in bytes
WINDOW_SIZE = 5
'''
This is a skeleton sender class. Create a fantastic transport protocol here.
'''
# 500ms retransmission timer if no ack
# window size of 5 packets
# should be able to send image file
# Any packets with invalid checksum should be ignored
# don't produce console output
# Make a README.txt file

class Sender(BasicSender.BasicSender):
    # Main sending loop.
    def handle_response(self,response_packet):
        if Checksum.validate_checksum(response_packet):
            if DEBUG:
                print "recv: %s "  % response_packet
            return 1
        else:
            if DEBUG:
                print "recv: %s <--- CHECKSUM FAILED" % response_packet
            return False

    def sws(self, sent_p, seqnum, mess_t, nxt_mess): #sliding window send
        seqno    = seqnum # 0
        sent     = sent_p
        msg_type = mess_t
        next_msg = None
        if nxt_mess == None:
            msg = self.infile.read(MSG_SIZE)
        else:
            msg = nxt_mess
        keep_sending = 0
        if len(sent) == 0:
            while msg_type !='end':
                if DEBUG:
                    print len(sent)

                next_msg  = self.infile.read(MSG_SIZE)
                msg_type  = 'data'
                if seqno == 0:
                    msg_type = 'start'
                elif next_msg == "":
                    msg_type  = 'end'
                        
                packet        = self.make_packet(msg_type,seqno,msg)
                sent[seqno]   = packet 
                self.send(packet)
                seqno         = seqno + 1
                msg = next_msg
                if msg_type == 'end':
                    break
            else:
                while len(sent) > 0:
                    for key in sent:
                        packet = sent[key]
                        self.send(packet)

        return  sent, seqno, msg_type, msg

    def swr(self, sent_p): # sliding window receive
        sent      = sent_p
        sent_size = len(sent) 
        response = None   # COULD THERE BE A CASE WHERE RESPONSE IS NONE?????
        for i in range(sent_size):  
            res = self.receive(TIMEOUT)

            if res != None: 
                valid_packet = self.handle_response(res)
                if valid_packet:
                    response = res
        if response != None:
            res_type, res_no, res_msg, res_chk = self.split_packet(response)
            res_no = int(res_no) 
            if DEBUG:
                print "ReceivedUpTo: " + str(res_no - 1)

            if res_type == 'ack':
                for i in range(res_no):
                    if i in sent:
                        del sent[i]
                
        return sent
                        
    def start(self):
        sent   = {}
        seqno    = 0
        ele      = 0
        msg_type = nxt_msg = None
        
        while msg_type !='end' or len(sent) !=0:
            sent, seqno, msg_type, nxt_msg = self.sws(sent, seqno, msg_type, nxt_msg)
            sent                           = self.swr(sent)
        self.infile.close


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

    for o,a in opts:
        if o in ("-f", "--file="):
            filename = a
        elif o in ("-p", "--port="):
            port = int(a)
        elif o in ("-a", "--address="):
            dest = a
        elif o in ("-d", "--debug="):
            debug = True

    s = Sender(dest,port,filename,debug)
    try:
        s.start()
    except (KeyboardInterrupt, SystemExit):
        exit()
