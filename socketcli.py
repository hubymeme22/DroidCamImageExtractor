from modules import RTPSExtractor
from socket import socket, AF_INET, SOCK_STREAM
import sys

camIP = sys.argv[1]
camPort = sys.argv[2]

cliSock = socket(AF_INET, SOCK_STREAM)
cliSock.connect((camIP, eval(camPort)))

cliSock.send(f"""
GET /video HTTP/1.1
Host: {camIP}:{camPort}
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.6045.123 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
Accept-Encoding: gzip, deflate, br
Accept-Language: en-US,en;q=0.9
Connection: close\r\n\r\n""".encode())

fps = 0
imageCount = 0
newPacket = False

while True:
	recieved = cliSock.recv(4096)

	# a new packet with jpeg is recieved
	if (RTPSExtractor.isFrameStart(recieved)):
		ImageExtractor = RTPSExtractor.PacketImageExtractor(b'', f"images/image{imageCount}.jpeg")
		ImageExtractor.appendPacket(recieved)
		newPacket = True
		continue

	if (newPacket): ImageExtractor.appendPacket(recieved)
	if (RTPSExtractor.isFrameEnd(recieved)):
		# extract image values
		ImageExtractor.extractImage()
		imageCount += 1
		print(f"[+] Image frame saved: {imageCount}")

		# reset the image extractor
		ImageExtractor = RTPSExtractor.PacketImageExtractor(b'', f"images/image{imageCount}.jpeg")
		newPacket = False