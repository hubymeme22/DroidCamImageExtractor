'''
This is a simple module that will be used for extracting
mjpeg images from RTP packets.

Author: Hubert F. Espinola I
written: Nov. 14, 2023
'''

class PacketImageExtractor:
	def __init__(self, packetInit: bytes, filename: str="yeet.jpeg"):
		self.packetData = packetInit
		self.name = filename
		self.packetSize = 0
		self.startIndex = 0
		self.endIndex = 0

	# get packet info during packet appending (faster)
	def appendPacket(self, packet: bytes):
		if (b"\xff\xd8" in packet): self.startIndex = self.packetSize + packet.rindex(b"\xff\xd8")
		if (b"\xff\xd9" in packet): self.endIndex = self.packetSize + packet.rindex(b"\xff\xd9")
		self.packetSize += len(packet)
		self.packetData += packet

	# retrieves the jpeg image buffer
	def decodeImage(self):
		if (self.endIndex > self.startIndex):
			dataBuffer = self.packetData[self.startIndex:self.endIndex + 2]
			return dataBuffer
		return b""

	# saves image to specified filename
	def extractImage(self):
		open(self.name, 'wb').write(self.decodeImage())

def isFrameStart(packet: bytes):
	return (b"\xff\xd8" in packet)

def isFrameEnd(packet: bytes):
	return (b"\xff\xd9" in packet)
