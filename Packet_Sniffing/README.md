# Packet Sniffing

Learned how to use a well-known sniffing tool, scapy. Wrote a simple sniffer and filtering programs to gain an in-depth understanding of the technical aspects of packet sniffing tools.

## Environment Setup:

* Install Scapy:
  * *sudo pip3 install scapy*

* Install libcap-dev:       
  * *apt-get install libpcap-dev*

## Executing Sniffers:

* Sniffer.py
  * *python3 sniffer.py
  
* mySniffer.c 
  * Compile C file using:
    * gcc -o [output_file_name] mySniffer.c -lpcap
  
  * Execute C file:
    * ./mySniffer (Substitute mySniffer with output_file_name selected when compiling)
