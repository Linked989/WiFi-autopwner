from wifi import Cell, Scheme
import socket, os

verbose = True

def wifiUp():
	cmd = 'ifconfig wlan0 up'
	os.system(cmd)

def banner():
	os.system('cat banner')


def internet(host="8.8.8.8", port=53, timeout=3):
	"""
	Host: 8.8.8.8 (google-public-dns-a.google.com)
	OpenPort: 53/tcp
	Service: domain (DNS/TCP)
	"""
	try:
		socket.setdefaulttimeout(timeout)
		socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
		return True
	except socket.error as ex:
		print(ex)
		return False


def listUn(cells):
	'''
	Scan for open (unencrypted) wireless access points)
	'''
	UnCount = 0
	for cell in cells:
		if cell.encrypted == False:
			UnCount += 1
			print("[+] %s: Unencrypted Network found!" % cell.ssid)
			#joinWifi(cell)
	if UnCount == 0:
		print("[-] None of detected networks were Unencrypted, starting El Chapo AP")



def joinWifi(cell):
	'''
	Join the open wifi and see if we have internet access
	'''
	print("Testing SSID: %s" % (cell.ssid))
	scheme = Add(cell)
	try:
		scheme.activate()
	except wifi.exceptions.ConnectionError:
		Delete(ssid)
		return False

def getSSIDs():
	'''
	Scan for open (unencrypted) wireless access points)
	'''
	TryAgain = 0
	print("[+] Scanning for Access Points")
	while TryAgain <= 4:
		cells = list(Cell.all('wlan0')) # This uses the wifi library to scan for Wireless Access points
		TryAgain += 1
	numCells = len(list(cells))
	print("[+] %s APs detected" % numCells)
	listSSIDs(cells)
	return cells

def listSSIDs(cells):
	print(" " * 3 + "#" * 75)
	for cell in cells:
		print(" " * 5 + "SSID: %s | Encrypted: %s | Signal: %s" % (cell.ssid, cell.encrypted, cell.signal))
	print(" " * 3 + "#" * 75)
	print("")



if __name__ == "__main__":
	wifiUp()
	banner()
	cells = getSSIDs()
	listUn(cells)
	if internet():
		print("Host is online, lets start digging :)")
	else:
		print("Host is not online, lets try to find a way out")

'''
for cell in cells:
...     print cell.ssid
...     print cell.encrypted
...     print cell.signal
'''