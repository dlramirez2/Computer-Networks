#include <pcap.h>
#include <stdlib.h>
#include <string.h>
#include <stdio.h>
#include <netinet/in.h>
#include <arpa/inet.h>


//Parts of this code were gathered from https://www.tcpdump.org/pcap.html
#define SIZE_ETHERNET 14
/* Ethernet addresses are 6 bytes */
#define ETHER_ADDR_LEN	6

	/* Ethernet header */
	struct sniff_ethernet {
		u_char ether_dhost[ETHER_ADDR_LEN]; /* Destination host address */
		u_char ether_shost[ETHER_ADDR_LEN]; /* Source host address */
		u_short ether_type; /* IP? ARP? RARP? etc */
	};

	/* IP header */
	struct sniff_ip {
		u_char ip_vhl;		/* version << 4 | header length >> 2 */
		u_char ip_tos;		/* type of service */
		u_short ip_len;		/* total length */
		u_short ip_id;		/* identification */
		u_short ip_off;		/* fragment offset field */
	#define IP_RF 0x8000		/* reserved fragment flag */
	#define IP_DF 0x4000		/* don't fragment flag */
	#define IP_MF 0x2000		/* more fragments flag */
	#define IP_OFFMASK 0x1fff	/* mask for fragmenting bits */
		u_char ip_ttl;		/* time to live */
		u_char ip_p;		/* protocol */
		u_short ip_sum;		/* checksum */
		struct in_addr ip_src,ip_dst; /* source and dest address */
	};
	#define IP_HL(ip)		(((ip)->ip_vhl) & 0x0f)
	#define IP_V(ip)		(((ip)->ip_vhl) >> 4)

	/* TCP header */
	typedef u_int tcp_seq;

	struct sniff_tcp {
		u_short th_sport;	/* source port */
		u_short th_dport;	/* destination port */
		tcp_seq th_seq;		/* sequence number */
		tcp_seq th_ack;		/* acknowledgement number */
		u_char th_offx2;	/* data offset, rsvd */
	#define TH_OFF(th)	(((th)->th_offx2 & 0xf0) >> 4)
		u_char th_flags;
	#define TH_FIN 0x01
	#define TH_SYN 0x02
	#define TH_RST 0x04
	#define TH_PUSH 0x08
	#define TH_ACK 0x10
	#define TH_URG 0x20
	#define TH_ECE 0x40
	#define TH_CWR 0x80
	#define TH_FLAGS (TH_FIN|TH_SYN|TH_RST|TH_ACK|TH_URG|TH_ECE|TH_CWR)
		u_short th_win;		/* window */
		u_short th_sum;		/* checksum */
		u_short th_urp;		/* urgent pointer */
};

/* This function will be invoked by pcap for each captured packet.
We can process each packet inside the function.
*/
void got_packet(u_char *args, const struct pcap_pkthdr *header, const u_char *packet){
	const struct sniff_ethernet *ethernet; /* The ethernet header */
	const struct sniff_ip *ip; /* The IP header */
	const struct sniff_tcp *tcp; /* The TCP header */
	const char *payload; /* Packet payload */

	u_int size_ip;
	u_int size_tcp;
	int size_payload;

   	
   	
   	ip = (struct ip_addr*)(packet + SIZE_ETHERNET);
   	ethernet = (struct sniff_ethernet*)(packet);
   	size_ip = IP_HL(ip)*4;
   
   		
	if (size_ip < 20) {
		printf("   * Invalid IP header length: %u bytes\n", size_ip);
		return;
	}
   	printf("Got a packet\n");
   	
   
   	printf("Source IP: %s:\n",inet_ntoa(ip->ip_src));
   	printf("Destination IP: %s:\n",inet_ntoa(ip->ip_dst));
	//checking protocol type for TCP and ICMP only since these are the focus of the assignment
	if(ip->ip_p == IPPROTO_TCP){
   		printf("GOT TCP Packet\n");
  	}else if (ip->ip_p == IPPROTO_ICMP){
  		printf("GOT ICMP Packer\n");
  	}else{
  		printf("Packet's Protocol is unknown,UDP or IP");
  	}
 
	
	tcp = (struct sniff_tcp*)(packet + SIZE_ETHERNET + size_ip);
	size_tcp = TH_OFF(tcp)*4;
	//The following instructions inside the if statements are only executed if the packet used TCP protocol
	if (size_tcp < 20 && ip->ip_p == IPPROTO_TCP) {
		printf("   * Invalid TCP header length: %u bytes\n", size_tcp);
		return;
	}
	if(ip->ip_p == IPPROTO_TCP){
		payload = (u_char *)(packet + SIZE_ETHERNET + size_ip + size_tcp);
   		size_payload = ntohs(ip->ip_len) - (size_ip+size_tcp);
   		//printing data part of captured TCP packet
   		int i =0;
   		while(i<size_payload){
   			printf("%c",*payload);
   			i++;
   			*payload++;
   		}
   	}	
	return;
}

int main(){
   pcap_t *handle;
   //setting the size for the erro buffer
   char errbuf[1024];
   struct bpf_program fp;
   //Variable to save the filters based on user selection
   char filter_exp[] = "";
   bpf_u_int32 net = 0;
   //Pointer to string of the device name.
   char *device = "eth0";
   //variable used to save user choice
   int selection;

   //menu for user
   printf("Welcome to my Sniffer\n");
   printf("Press 1 to Capture all packets\n");
   printf("Press 2 to capture ICMP packets\n");
   printf("Press 3 to capture TCP Packets from ports x to y\n");
   printf("Press Ctrl+C to exit anytime\n");
   scanf("%d",&selection);

   
   if(selection == 2){
   	//I used my localhost IP, change to match localhost
   	printf("Capturing ICMP from localhost\n");
   	strcpy(filter_exp, "icmp and src host 10.0.2.15");
   }else if(selection == 3){
   	//variables to save lower and upper limit for port range
   	int low_limit;
   	int high_limit;
   	
   	printf("Input Port Lower Limit:\n");
   	scanf("%d",&low_limit);
   	printf("Input Port Upper Limit:\n");
   	scanf("%d",&high_limit);
   	if(low_limit < high_limit || low_limit == high_limit){
   		printf("Valid port range\n");
   	}else{
   		printf("Invalid port range. Exiting \n");
   		exit(EXIT_FAILURE);
   	}
   	printf("Selected port range %d-%d \n",low_limit,high_limit);

   	sprintf(filter_exp, "tcp and dst portrange %d-%d",low_limit,high_limit);

   }else{
   	printf("Capturing all packets\n");
   	strcpy(filter_exp, "");
   }
   
   // Step 1: Open live pcap session on NIC with name ethx
   // you need to change "eth3" to the name
   // found on their own machines (using ifconfig).
   handle = pcap_open_live(device, 1518, 1, 1000, errbuf);
   if (handle == NULL){
   	printf("Device not found ",device);
   	exit(EXIT_FAILURE);
   }

   // Step 2: Compile filter_exp into BPF psuedo-code
   if(pcap_compile(handle, &fp, filter_exp, 0, net) == -1){
   	printf("Failure in filter compile");
   	exit(EXIT_FAILURE);
   }
   pcap_setfilter(handle, &fp);
   // Step 3: Capture packets
   pcap_loop(handle, -1, got_packet, NULL);
   pcap_freecode(&fp);
   pcap_close(handle); //Close the handle
   return 0;
}
// Note: don’t forget to add "-lpcap" to the compilation command.
// For example: gcc -o sniff sniff.c -lpcap
