# File Transfer Protocols

### File Transfer using Stop-and-Wait (SnW) Protocol

Modified the function *send_snw(sock)* which reads the file “*Bio.txt*” and transfers it by
following the stop-and-wait protocol. Note that each packet has a payload of 512
Bytes, which is defined in PACKET_SIZE.Packet losses are handled using the
timer module.

Implemented the function *receive_snw(sock, pkt)* to handle the acknowledgements in stop-and-wait protocol. If the ACK gets lost, this function retransmits the pkt again.

Modified the function *receive_snw(sock)* which receives all the payloads in correct sequence
and writes them into a file *receiver_bio.txt* at the receiver, reconstructing the sender’s file
*bio.txt*.

### File Transfer using Go-Back-N (GBN) Protocol

Implemented *send_gbn(sock)* function that will read the file “Bio.txt” to transfer it to the GBN
receiver. Its job is to calculate how many packets to send, and then send N packets based
on defined window size. Ensure to implement the actions when packets get lost happens.

Implemented *receive_gbn(sock)* function that checks if the expected ACKs are being received or
not. Based on that the sender should take necessary actions.

Implemented *receive_gbn(sock)* function at the receiver which receives the packets and writes them
into the file “*receiver_bio.txt*”. Ensured that if the expected sequence number is not
received, it sends the last in-ordered packet’s sequence # as ACK

---

**Executing Script:**

Run the following commands in order:
* *python3 receiver.py*
   
   uncomment *receive_gbn(sock)* at main function

* *python3 sender.py*
   
   uncomment *send_gbn(sock)* at main function
> *receiver.py* must be executing before beginning execution of *sender.py* for the file transfer to be demonstrated 
