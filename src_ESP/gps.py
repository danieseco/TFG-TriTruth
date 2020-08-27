from machine import UART, Pin, deepsleep
from time import sleep

def loadSafeZone():
	safeZone = []
	connZone = []
	try:
		with open('safeZone.conf','r') as zoneFile:
			for line in zoneFile:
				if line[0] != '#':
					safeZone.append(line.split('#'))
	except:
		pass
	try:
		with open('connZone.conf','r') as connFile:
			for line in connFile:
				if line[0] != '#':
					connZone = line.split('#')
	except:
		pass
	return [safeZone, connZone]
	
def run():
	gps = UART(1)
	gps.init(baudrate=9600, bits=8, tx=17, rx=16)
	safeZone, connZone = loadSafeZone()
	while(True):
		try:
			inSafe = False
			line = str(gps.readline()).split(',')
			if '$GPGLL' in line[0]:
				if len(line)>5: #Si tengo señal
					if len(line[1]) > 9 and len(line[3]) > 10:
						dgLat = int(line[1][0] + line[1][1])				#Calculo latitud
						minLat = float(line[1][2] + line[1][3] + line[1][4] + line[1][5] + line[1][6] + line[1][7] + line[1][8] + line[1][9] )
						latitude = dgLat+minLat/60
						if line[2] == 'S':
							latitude = -latitude
						
						dgLon = int(line[3][0] + line[3][1] + line[3][2])	#Calculo longitud
						minLon = float(line[3][3] + line[3][4] + line[3][5] + line[3][6] + line[3][7] + line[3][8] + line[3][9] + line[3][10])
						longitude = dgLon+minLon/60
						if line[4] == 'W':
							longitude = -longitude
					
						time = line[5]
					for zone in safeZone: #Si tengo q detectar
						if (zone[0] < latitude < zone[2]) and (zone[1] < longitude < zone[3]):
							yield('PASS')
							inSafe = True
					if  len(connZone)==4 and (connZone[1] < latitude < connZone[3]) and (connZone[2] < longitude < connZone[4]):
						if (time > connZone[0]):
							yield('END')
							break
						else:
							yield('PASS')
							break
					
					if inSafe == False:
						yield('{}#{}#{}'.format(longitude, latitude, time))
					else:
						sleep(10) #Si estoy en zona segura, duermo todo el micro 10s
				else:
					yield('PASS')
		except Exception as e:
			print(e)
			pass
			