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

	def appendPacket(self, packet: bytes):
		self.packetData += packet

	# retrieves the jpeg image buffer
	def decodeImage(self):
		startIndex = self.packetData.rindex(b"\xff\xd8")
		endIndex = self.packetData.rindex(b"\xff\xd9")
		dataBuffer = self.packetData[startIndex:endIndex + 2]
		return dataBuffer

	# saves image to specified filename
	def extractImage(self):
		open(self.name, 'wb').write(self.decodeImage())

def isFrameStart(packet: bytes):
	return (b"\xff\xd8" in packet)

def isFrameEnd(packet: bytes):
	return (b"\xff\xd9" in packet)
