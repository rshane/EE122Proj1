import sys
import getopt

import Checksum
import BasicSender

import Queue

TIMEOUT     = 0.5 # in seconds
DEBUG       = 0
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
        window = Queue.Queue(5)
        seqno = 0
        msg = self.infile.read(MSG_SIZE)
        msg_type = None
        while not msg_type == 'end':
            next_msg = self.infile.read(MSG_SIZE)

            msg_type = 'data'
            if seqno == 0:
                msg_type = 'start'
            elif next_msg == "":
                msg_type = 'end'
            
            packet = self.make_packet(msg_type,seqno,msg)
            try:
                window.put(packet)
            except Full:
                #need to FINISH THIS
                #making sliding window
                
            self.send(packet)
            if DEBUG:
                print "sent: %s" % packet

            response = self.receive(TIMEOUT)
            if response != None:
                response_type = response[0]
                response_no = response[1]

            valid = self.handle_response(response)

            # Send every TIMEOUT until ACK is received
            # only stop go; CHECK SEQNO OF RESPONSE
            # AND PACKETS IN ORDER
            
            while not valid or response == None:
                if DEBUG:
                    import pdb; pdb.set_trace()
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
