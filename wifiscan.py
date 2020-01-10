import wifi #import Cell, Scheme
import socket, os
#scheme=SchemeWPA('wlan0',cell.ssid,{"ssid":xfinitywifi})
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
			print("  - attempting to join")
			print Connect(cell.ssid)
	if UnCount == 0:
		print("[-] None of detected networks were Unencrypted, starting El Chapo AP")


def getSSIDs():
	'''
	Scan for open (unencrypted) wireless access points)
	'''
	TryAgain = 0
	print("[+] Scanning for Access Points")
	while TryAgain <= 4:
		cells = list(wifi.Cell.all('wlan0')) # This uses the wifi library to scan for Wireless Access points
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

def Search():
    wifilist = []
    cells = wifi.Cell.all('wlan0')
    for cell in cells:
        wifilist.append(cell)
    return wifilist


def FindFromSearchList(ssid):
    wifilist = Search()
    for cell in wifilist:
        if cell.ssid == ssid:
            return cell
    return False


def FindFromSavedList(ssid):
    cell = wifi.Scheme.find('wlan0', ssid)
    if cell:
        return cell
    return False


def Connect(ssid, password=None):
    cell = FindFromSearchList(ssid)
    if cell:
        savedcell = FindFromSavedList(cell.ssid)
        # Already Saved from Setting
        if savedcell:
            savedcell.activate()
            return cell
        # First time to conenct
        else:
            if cell.encrypted:
                if password:
                    scheme = Add(cell, password)
                    try:
                        scheme.activate()
                    # Wrong Password
                    except wifi.exceptions.ConnectionError:
                        Delete(ssid)
                        return False
                    return cell
                else:
                    return False
            else:
                scheme = Add(cell)
                try:
                    scheme.activate()
                except wifi.exceptions.ConnectionError:
                    Delete(ssid)
                    return False
                return cell
    return False


def Add(cell, password=None):
    if not cell:
        return False
    scheme = wifi.Scheme.for_cell('wlan0', cell.ssid, cell, password)
    scheme.save()
    return scheme


def Delete(ssid):
    if not ssid:
        return False
    cell = FindFromSavedList(ssid)
    if cell:
        cell.delete()
        return True
    return False

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