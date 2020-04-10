from machine import UART, Pin
from time import sleep

def run():
	gps = UART(1)
	gps.init(baudrate=9600, bits=8, tx=17, rx=16)
	
	while(True):
		try:
			line = str(gps.readline()).split(',')
			if '$GPGLL' in line[0]:
				if len(line)>5:
					if len(line[1]) > 9 and len(line[3]) > 10:
						dgLat = int(line[1][0] + line[1][1])
						minLat = float(line[1][2] + line[1][3] + line[1][4] + line[1][5] + line[1][6] + line[1][7] + line[1][8] + line[1][9] )
						latitude = dgLat+minLat/60
						if line[2] == 'S':
							latitude = -latitude
						
						dgLon = int(line[3][0] + line[3][1] + line[3][2])
						minLon = float(line[3][3] + line[3][4] + line[3][5] + line[3][6] + line[3][7] + line[3][8] + line[3][9] + line[3][10])
						longitude = dgLon+minLon/60
						if line[4] == 'W':
							longitude = -longitude
					
						time = line[5]
						
					yield ('{}#{}#{}'.format(longitude, latitude, time))
	
				else:
					yield('PASS')
		except:
			pass
			