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
            print "recv: %s "  % response_packet
            return 1
        else:
            print "recv: %s <--- CHECKSUM FAILED" % response_packet
            return False
    def sws(self, win, seqnum, mess_t, nxt_mess): #sliding window send
        window   = win
        seqno    = seqnum # 0
        msg_type = mess_t
        next_msg = None
        if nxt_mess == None:
            msg = self.infile.read(MSG_SIZE)
        else:
            msg = nxt_mess
        while len(window) < WINDOW_SIZE and msg_type !='end':
           
            next_msg  = self.infile.read(MSG_SIZE)
            msg_type  = 'data'
            if seqno == 0:
                msg_type = 'start'
            elif next_msg == "":
                msg_type  = 'end'

            packet        = self.make_packet(msg_type,seqno,msg)
            window[seqno] = packet
            if DEBUG:
                print "windowkeys: " + str(window.keys())
                print "seqno: "       + str(seqno)
                print "msg_type: "    + msg_type
                     
                #import pdb; pdb.set_trace()                                

            seqno         = seqno + 1
            msg = next_msg
            if msg_type == 'end':
                break
                
        for key in window:
            packet = window[key]
            if DEBUG:
                print "SENDING"
                print "packet_num:" + str(key)

            self.send(packet)

        return window, seqno, msg_type, msg


    def swr(self, win): # sliding window receive
        window   = win
        uncorr_pac = 0    

        response = None   # COULD THERE BE A CASE WHERE RESPONSE IS NONE?????
        for i in range(WINDOW_SIZE):  
            res = self.receive(TIMEOUT)

            if res != None and not uncorr_pac: 
                valid_packet = self.handle_response(res)
                if valid_packet:
                    response = res
                else:
                    uncorr_pac = 1
                    break
        if response != None:
            res_type, res_no, res_msg, res_chk = self.split_packet(response)
            res_no = int(res_no) 
            if DEBUG:
                print "ReceivedUpTo: " + str(res_no - 1)

            if res_type == 'ack':
                for i in range(res_no):
                    if i in window:
                        packet = window[i]
                        del window[i]
                
        return window
                        
        
    

    def start(self):
        window   = {}
        seqno    = 0
        ele      = 0
        msg_type = nxt_msg = None
        
        while msg_type !='end' or len(window) !=0:
            window, seqno, msg_type, nxt_msg = self.sws(window, seqno, msg_type, nxt_msg)
            window                           = self.swr(window)
        self.infile.close()
                # if DEBUG:
                #     print "sent: %s" % packet


            #for array append any new packet set while loop limit to window size, then remove any proper acks
            #recv: ack|12|1621908066            

#----------Need to figure out how receiver accept many packets-----------        
'''
        if response != None:
            response_type = response[0]
            response_no = response[1]

        valid = self.handle_response(response)

        # Send every TIMEOUT until ACK is received
        # only stop go; CHECK SEQNO OF RESPONSE
        # AND PACKETS IN ORDER
        
        while not valid or response == None:
            self.send(packet)
            response = self.receive(TIMEOUT)
            valid = self.handle_response(response)
            
        msg = next_msg
        seqno += 1
'''                




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
