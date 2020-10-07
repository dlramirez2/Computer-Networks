import socket
import _thread
import time
import string
import packet
import udt
import random
from timer import Timer

# Some already defined parameters
PACKET_SIZE = 512
RECEIVER_ADDR = ('localhost', 8080)
SENDER_ADDR = ('localhost', 9090)
SLEEP_INTERVAL = 0.05 # (In seconds)
TIMEOUT_INTERVAL = 0.5
WINDOW_SIZE = 4

# You can use some shared resources over the two threads
base = 0
mutex = _thread.allocate_lock()
timer = Timer(TIMEOUT_INTERVAL)

# Need to have two threads: one for sending and another for receiving ACKs

# Generate random payload of any length
def generate_payload(length=10):
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))

    return result_str


# Send using Stop_n_wait protocol
def send_snw(sock):
	# Fill out the code here
    seq = 0
    while(seq < 20):
        data = generate_payload(40).encode()
        pkt = packet.make(seq, data)
        print("Sending seq#", seq, "\n")
        udt.send(pkt, sock, RECEIVER_ADDR)
        seq = seq+1
        time.sleep(TIMEOUT_INTERVAL)
    pkt = packet.make(seq, "END".encode())
    udt.send(pkt, sock, RECEIVER_ADDR)

# Send using GBN protocol
def send_gbn(sock):
    global base, timer, mutex
    pck_store = []
    pkt_seq = 0

    filePath = 'Bio.txt'  #this can be any desired file path or file name
    file = open(filePath,'rb')
    data = " "

    '''making the packets and storing them in a list'''
    while data:
        data = file.read(PACKET_SIZE)
        pck_store.append(packet.make(pkt_seq, data))
        pkt_seq= pkt_seq + 1

    #reseting packet sequence number
    pkt_seq = 0
    '''setting up a variable to store the values within the base of
    the window and its top'''
    window = WINDOW_SIZE
    base = 0

    '''starting thread'''
    _thread.start_new_thread(receive_gbn,(sock,))
    print("Starting....")
    while base < len(pck_store):
        mutex.acquire()
        '''Starting timer.......'''''
        if not timer.running():
            timer.start()

        '''Sending the packets in window and checking that the current pkt sequence 
        is less than the packets stored in buffer'''
        while pkt_seq < (base + window) and pkt_seq < len(pck_store):
            udt.send(pck_store[pkt_seq], sock, RECEIVER_ADDR)
            print("Sending seq#", pkt_seq, "\n")
            pkt_seq = pkt_seq + 1

        '''checking for a timer timeout, updating window if no timeout has occurred'''
        if timer.timeout():
            timer.stop()
            print("Timeout occurred, resetting.......")
            pkt_seq = base
        else:
            '''updating window'''''
            window = min((len(pck_store)-base),WINDOW_SIZE)

        while timer.running() and not timer.timeout():
            mutex.release()
            time.sleep(SLEEP_INTERVAL)
            print("Sleeping......")
            mutex.acquire()
        mutex.release()

    '''sending last packet with the content END'''
    pkt = packet.make(pkt_seq, "END".encode())
    udt.send(pkt, sock, RECEIVER_ADDR)
    file.close()

# Receive thread for stop-n-wait
def receive_snw(sock, pkt):
    endStr = ''
    while endStr != 'END':
        pkt, senderaddr = udt.recv(sock)
        seq, data = packet.extract(pkt)
        endStr = data.decode()
        print("From: ", senderaddr, ", Seq# ", seq, endStr)
    return seq

# Receive thread for GBN
def receive_gbn(sock):
    # Fill here to handle acks
    global base, timer, mutex
    end = ''
    while end != 'END':
        pkt, senderaddr = udt.recv(sock)
        seq, data = packet.extract(pkt)
        end = data.decode()
        print("From: ", senderaddr, ", Seq# ", seq, end)
        if seq >= base:
            mutex.acquire()
            base = seq + 1
            timer.stop()
            mutex.release()

# Main function
if __name__ == '__main__':
    # if len(sys.argv) != 2:
    #     print('Expected filename as command line argument')
    #     exit()

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(SENDER_ADDR)

    # filename = sys.argv[1]

    send_gbn(sock)
    sock.close()


