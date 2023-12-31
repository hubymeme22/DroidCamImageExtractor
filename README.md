# DroidCamImageExtractor
These programs extract JPEG images from Droid cam by direct connection or by using a packet sniffer. The difference between these two scripts is that direct connection spawns a connection session, and sniffing does not. Since the droid cam only allows one session of client/browser for their app, then a user wanting to extract images while using the app would be a pain in the ..., if doing so, sniffing will be a better option.

### Extraction by direct connection
This directly connects through the specified ip and port of the droid camera app and extracts the images to the `images` folder:
`python3 socketcli.py <camera-ip-address> <camera-port>`

### Extraction by sniffing packets
Change directory by: `cd sniffer`
Install the required before using sniffer by: `pip3 install -r requirements.txt`
This retrieves the images by listening to specified ip, port, and interface. Note: this **requires root** permission.:
`sudo python3 sniffer.py <camera-ip-address> <camera-port> <interface>`
