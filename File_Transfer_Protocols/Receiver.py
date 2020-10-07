# receiver.py - The receiver in the reliable data transfer protocol
import sys

import packet
import socket
import udt

RECEIVER_ADDR = ('localhost', 8080)

# Receive packets from the sender w/ GBN protocol
def receive_gbn(sock):
    '''file created to save received packets'''
    try:
        file_out = open('receiver_bio.txt', 'a')
    except IOError:
        print("File not created")
        return

    endStr = ''
    expected_seq = 0
    '''if socket doesnt receive info in 10 seconds, then end communication'''
    sock.settimeout(10)
    while endStr != 'END':
        '''checking if sender continues to transmit data'''
        try:
            pkt, senderaddr = udt.recv(sock)
        except socket.timeout:
            print('Sender seems inactive......')
            print('Shutting down receiver.....')
            break
        seq, data = packet.extract(pkt)
        print("Received Packet: ",seq)
        if seq == expected_seq:
            '''extracting valid packet contents and appending contents to receiver_bio.txt file'''
            endStr = data.decode()
            print("From: ", senderaddr, ", Seq# ", seq, endStr)
            print("Sending ACK:", expected_seq)
            pkt = packet.make(expected_seq)
            udt.send(pkt, sock, senderaddr)
            file_out.write(endStr)
            expected_seq = expected_seq + 1
        else:
            ##Sending last valid ACK
            print("Sending ACK:",expected_seq-1)
            pkt = packet.make(expected_seq-1)
            udt.send(pkt,sock,senderaddr)

    print("End of transmission")
    file_out.close()

# Receive packets from the sender w/ SR protocol
def receive_sr(sock, windowsize):
    # Fill here
    return


# Receive packets from the sender w/ Stop-n-wait protocol
def receive_snw(sock):
   endStr = ''
   while endStr !='END':
       pkt, senderaddr = udt.recv(sock)
       seq, data = packet.extract(pkt)
       endStr = data.decode()
       print("From: ", senderaddr, ", Seq# ", seq, endStr)


# Main function
if __name__ == '__main__':
    # if len(sys.argv) != 2:
    #     print('Expected filename as command line argument')
    #     exit()

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(RECEIVER_ADDR)
    # filename = sys.argv[1]
    receive_gbn(sock)

    # Close the socket
    sock.close()