from machine import UART, I2C, Pin, PWM, deepsleep
import time
import ssd1306
import gps
import _thread
import sendInfo

currGPS = 'PASS'

def actGPS():
	global currGPS
	
	for current in gps.run():
		currGPS = current

def userAdvice(seconds):
	myPwm = PWM(Pin(21))
	myPwm.duty(512)
	start = time.time()
	i=0
	while(seconds > time.time()-start):
		if i==0:
			myPwm.freq(500)
			i=1
		else:
			myPwm.freq(2000)
			i=0
		time.sleep(0.01)
	myPwm.freq(0)
	myPwm.duty(0)
	
def setLidar():
	#Configuro la UART
	try:
		Lidar = UART(2, baudrate=115200)
		Lidar.init(baudrate=115200, bits=8, parity=None, tx=14, rx=32)
		return [True, Lidar]
	except Exception as errCod:
		return [False, errCod]


def getLidar(Lidar):
	Lectura = bytearray(3)
	uno=bytearray([0])
	#Vacío lecturas
	Lidar.read()
	#Busco byte inicio
	uno = Lidar.read(1)
	while uno != b'Y':
		uno=Lidar.read(1)
	#Leo los 3 bytes siguientes
	Lectura=Lidar.read(3)
	if Lectura[0]==89:#Si lectura Ok
		#Convierto a metros
		Distancia=Lectura[1] + Lectura[2]*256
		return Distancia
	else:
		return 'Error'

def setScreen():
	try:
		i2c = I2C(scl=Pin(22),sda=Pin(23), freq=100000)
		oled = ssd1306.SSD1306_I2C(width=128, height=32, i2c=i2c)
		oled.init_display()
		oled.poweron()
		oled.fill(0)
		oled.show()
		return [True, oled]
	except Exception as errCod:
		return [False, errCod]
	
def dispMsg(screen, msg):
	screen.fill(0)
	screen.text(msg, 0, 0)
	screen.show()

def run():
	currCheat = 0
	currFree = 0
	totalFree = 0
	totalCheat = 0
	gpsThread = _thread.start_new_thread(actGPS, ())
	sensor = setLidar()
	screen = setScreen()
	led = Pin(33, Pin.OUT)
	led.value(0)
	cheatFile = open('cheat.log','w+')
	if (sensor[0] == True):
		while(currGPS != 'END'):
			distance = getLidar(sensor[1])
			if distance != 'Error':
				dispMsg(screen[1], str(distance))
				
				if distance < 800 : # Si a menor de la distancia
					if currFree != 0:#Limpio el tiempo de liberación y lo acumulo si habia
						totalFree += time.time()-currFree
						currFree = 0
						led.value(1)
					if currGPS != 'PASS' and currCheat == 0: # Si estoy en zona prohibida x primera vez
						currCheat = time.time() #Arranco el aviso
						lon, lat, tiemp = currGPS.split('#') #Guardo donde comienzo
						led.value(1)
						
				elif distance > 800 and currCheat != 0: #Si salgo de zona prohibida en un aviso
					if currFree == 0:
						currFree = time.time()
						led.value(0)
				
				if currCheat != 0: #Si estoy bajo un aviso
					totalCheat = time.time()-currCheat
					if totalCheat > 10 :#Si llevo + de 10" en aviso
						led.value(0)
						if currFree != 0:#Limpio el tiempo de liberación y lo acumulo si habia
							totalFree += time.time()-currFree
							currFree = 0
						if totalFree > 5: # Si he estado mas de la mitad del tiempo infringiendo
							_thread.start_new_thread(userAdvice, [1])
							cheatFile.write(' #{}#{}'.format(lon, lat)) #Guardo el positivo
						totalCheat = 0 #Haya sido una infraccion o not
						totalFree = 0  #reinicio todos los contadores
						currCheat = 0
				else:
					deepsleep(1000)
			print(totalCheat, totalFree, distance)
		gpsThread.exit()
		cheatFile.close()
		checked = 'Unchecked'
		while (checked == 'Unchecked'):
			try:
				checked = sendInfo.run()
			except:
				pass
	else:
		print('Whoops :( something went wrong')

