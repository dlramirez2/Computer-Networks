from scapy.all import *

def print_pkt(pkt):
	pkt.show()

'''
Sniffer for ICMP Packets.
'''
#pkts = sniff(filter = "icmp",prn=print_pkt)

'''
Sniffer for TCP Packets. The Packet should come from a predefined host and be destined for the defined Port
filter = "[protocol] and host [IP_host] and port [X]"
'''
pkts = sniff(filter = "tcp and host 173.222.252.188 and port 53180",prn=print_pkt)

