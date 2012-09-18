import sys
import getopt

import Checksum
import BasicSender

TIMEOUT     = 0.5 # in seconds
DEBUG       = 1
MSG_SIZE    = 500 # in bytes
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
            print "recv: %s" % response_packet
            return 1
        else:
            print "recv: %s <--- CHECKSUM FAILED" % response_packet
            return 0
    
    def start(self):
        window = {}
        ele = 0
        response = None
        seqno = 0
        msg = self.infile.read(MSG_SIZE)
        msg_type = None
        while ele < WINDOW_SIZE:
            if  msg_type != 'end':
                next_msg = self.infile.read(MSG_SIZE)
                msg_type = 'data'
                if seqno == 0:
                    msg_type = 'start'
                elif next_msg == "":
                    msg_type = 'end'

                if DEBUG:
                    import pdb; pdb.set_trace()
                                
                packet = self.make_packet(msg_type,seqno,msg)
                window[seqno] = packet
                seqno         = seqno + 1
                ele             = ele + 1
                self.send(packet)
                                    
                res = self.receive(TIMEOUT)
                msg = next_msg

                if res != None: 
                    response = res
                    res_type, res_no, res_msg, res_chk = self.split_packet(response)
                    res_no = int(res_no)
                    if res_type == 'ack':
                        for i in range(res_no):
                            if i in window:
                                del window[i]
                                ele = ele - 1
                        if msg_type == 'end':
                          break


        
                #Need take care when window full and packets not received
                #maybe proper way to check the diff between when finish receiving all the packets vs. when window is full would be
                #to check if ele == window_size
        
                # if DEBUG:
                #     print "sent: %s" % packet


            #for array append any new packet set while loop limit to window size, then remove any proper acks
            #recv: ack|12|1621908066            

#----------Need to figure out how receiver accept many packets-----------        
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
                

        self.infile.close()


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
