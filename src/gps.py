from machine import UART, Pin

gps = UART(1)
gps.init(baudrate=9600, bits=8, tx=17, rx=16)

gps.read()

while(True):
	line = str(gps.readline()).split(',')
	if '$GPGLL' in line[0]:
		if len(line)>5:
			latitude = [line[1], line[2]]
			longitude = [line[3], line[4]]
			time = line[5]
			print('LATITUD={}\nLONGITUD={}\nHORA={}'.format(latitude, longitude, time))
		