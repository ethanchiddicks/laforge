import socket
import time
from select import select
import sys


# Controller Initialization
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("localhost", 3000))

# Sensor Initialization
f = open("/dev/ttyUSB0", "rb")

# Controller Functions
def d(dist):
	mult = 1.0-dist  # We actually specify a multiplier, instead of dist
	s.send("cfia 0 0 M%f; cfia 1 0 M%f;\n" % (mult, mult))

def a(ang):
	s.send("cfc 0 \"L%.3d\"; cfc 1 \"R%.3d\";\n" % (ang, ang))

# Sensor Functions
def getValue(s):
	if s[2] != '\n':
		raise Exception("Data string doesn't end with \n: %s" % repr(s))
	v2 = ord(s[0])
	v1 = ord(s[1])

	v2 = v2 & 0x1F
	v1 = v1 & 0x1F

	v = v1 + (v2 << 5) 

	return v

def sample():
	s = ""
	while s != '\n':
		s = f.readline()  # Realign read
	return [getValue(f.readline()), getValue(f.readline())]

def continuous():
	# State vars
	dist_avg_buff = [0]*3
	gyro_acc = 0.0	
	
	while 1:
		# Keyboard input to re-zero gyro_acc
		b = select([sys.stdin.fileno()], [], [], 0)
		if sys.stdin.fileno() in b[0]:
			sys.stdin.read(1)
			gyro_acc = 0.0

		[gyro_s, dist_s] = sample()
		
		# Distance processing
		## Scale and clamp
		dist_p = dist_s/1024.0*2.0  # 0 to 2.5 volts is range
		dist_p = min(dist_p, 1.0) # Clamp at 1.0
		dist_p = max(dist_p, 0.0) # Clamp at 0.0
		## Moving average
		dist_avg_buff.pop(0)
		dist_avg_buff.append(dist_p)
		dist_avg = sum(dist_avg_buff)/len(dist_avg_buff)

		# Gyro processing
		## Scale and invert
		gyro_p = (gyro_s-475)/1024.0*5.0/0.006 # Now in degrees / second
		gyro_p = gyro_p * -1.0
		## Integrate
		gyro_acc += (gyro_p/20.0)  # 20.0Hz is the sampling rate
		## Quantize and re-range
		gyro_q = int((gyro_acc % 360.0)/15)*15

		# Console Output
		print "gyro_s: %.4d\tgyro_p: %.3f\tgyro_acc: %.3f\tgyro_q: %.3d" % (gyro_s, gyro_p, gyro_acc, gyro_q)
		print "dist_s: %.4d\tdist_p: %.3f\tdist_avg: %.3f" % (dist_s, dist_p, dist_avg)
		
		# Control output
		d(dist_avg)
		#a(gyro_q)
		

# Run
a(0)
d(1.0)
continuous()
