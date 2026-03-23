from openai import OpenAI
from scapy.all import sniff
import datetime

client = OpenAI()

# Simple threat rules
SUSPICIOUS_PORTS = [22, 23, 3389]  # SSH, Telnet, RDP
REQUEST_THRESHOLD = 20

traffic_log = []

# Analyze packet 
def analyze_packets(packet):
    if packet.haslayer("IP"):
        src = packet["IP"].src
        dst = packet["IP"].dst
        
        port = None


        port = None
        if packet.haslayer("TCP"):
            port = packet["TCP"].dport
        elif packet.haslayer("UDP"):
            port = packet["UDP"].dport

        entry = {
            "time": str(datetime.datetime.now()),
            "src": src,
            "dst": dst,
            "port": port
        }

        traffic_log.append(entry)

        # Detect suspicious activity
        if port in SUSPICIOUS_PORTS:
            handle_threat(entry)