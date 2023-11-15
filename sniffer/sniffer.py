'''
Sniffs the incomming packets with specified ip address
and extracts all the images retrieved from the RTPS packet.
'''
from scapy.all import *
import time
import sys

sys.path.append('../')
from modules import RTPSExtractor

if (len(sys.argv) < 4):
	print ("[!] Invalid argument values")
	print ("Usage: proxy.py <camera-ip-address> <camera-port> <interface>")
	exit()

# argument details
cameraIP = sys.argv[1]
cameraPort = sys.argv[2]
interface = sys.argv[3]

ImageExtractor: RTPSExtractor.PacketImageExtractor = None
newPacket = False
imageCount = 1

# sample callback implementation
def callback(packet):
	if (Raw not in packet): return

	global newPacket
	global imageCount
	global ImageExtractor

	dataBuffer: bytes = packet[Raw].load

	if (RTPSExtractor.isFrameStart(dataBuffer)):
		ImageExtractor = RTPSExtractor.PacketImageExtractor(dataBuffer, f'images/image_{imageCount}.jpeg')
		newPacket = True
		return

	if (newPacket): ImageExtractor.appendPacket(dataBuffer)
	if (RTPSExtractor.isFrameEnd(dataBuffer)):
		ImageExtractor.extractImage()
		imageCount += 1

		print(f"[+] New image packet sniffed (count: {imageCount})")
		newPacket = False


# proceed to process the requests
print("[+] Network sniffer started")
sniff(filter=f"src host {cameraIP} and src port {cameraPort}", iface=interface, prn=callback)
