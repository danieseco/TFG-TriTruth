from machine import UART, Pin
from time import sleep
gps = UART(1)
gps.init(baudrate=9600, bits=8, tx=17, rx=16)
with open('currGPS.log','w') as gpsFile:
	gpsFile.write('ERROR')
gps.read()

while(True):
	line = str(gps.readline()).split(',')
	if '$GPGLL' in line[0]:
		if len(line)>5:
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
			with open('currGPS.log','w') as gpsFile:
				gpsFile.write('{}#{}#{}'.format(longitude, latitude, time))
			sleep(10)
			gps.read()
		