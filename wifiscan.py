from wifi import Cell, Scheme
import socket, os

def wifiUp():
	cmd = 'ifconfig wlan0 up'
	os.system(cmd)


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


def listUn():
	'''
	Scan for open (unencrypted) wireless access points)
	'''
	UnCount = 0
	TryAgain = 0
	numCells = 0
	while UnCount == 0 and TryAgain <= 4:
		print("[+] Scanning for Access Points [%s/%s]" % (UnCount, TryAgain))
		cells = Cell.all('wlan0') # This uses the wifi library to scan for Wireless Access points
		numCells = len(list(cells))
		for cell in cells:
			if cell.encrypted == False:
				UnCount += 1
				joinWifi(cell)
			TryAgain += 1
	print(":: %s APs detected ::" % numCells)
	print("However none were Unencrypted, starting El Chapo AP")



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


if __name__ == "__main__":
	wifiUp()
	listUn()
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