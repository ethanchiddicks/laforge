import socket
import time
from select import select
import sys
import math

# Global distance
global dist_global
dist_global = 1.0

# Controller Initialization
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("localhost", 3000))

# Sensor Initialization
f = open("/dev/ttyUSB0", "rb")

class BadPacket(Exception):
	pass

# Controller Functions
def d(dist):
	mult = 1.0-dist  # We actually specify a multiplier, instead of dist
	# FIXME: distance temporarily disabled to debug direction
	#s.send("cfia 0 0 M%f; cfia 1 0 M%f;\n" % (mult, mult))
	global dist_global
	dist_global = mult

def a(ang):
	## Calculate HRIR interpolation
	# Lowest angle
	al = math.floor(ang/15.0)*15
	# Highest angle
	ah = math.ceil(ang/15.0)*15
	# Make sure we don't double up on one angle
	if al == ah:
		ah = al + 15
	# Lowest angle filter attenuation
	alfa = (ang-al)/15.0
	# Highest angle filter attenuation
	ahfa = (ah-ang)/15.0
	# Re-range
	al = al%360
	ah = ah%360

	# Attenuate by global distance
	global dist_global
	ahfa = ahfa * dist_global
	alfa = alfa * dist_global
	
	cmd_string = ""
	## Lowest angle (not left channel!) filters
	# Select filters
	cmd_string += "cfc 0 \"L%.3d\"; cfc 1 \"R%.3d\"; " % (al, al)
	# Set attenuation
	cmd_string += "cfia 0 0 M%.2f; cfia 1 0 M%.2f; " % (alfa, alfa)

	## Highest angle (not right channel!) filters
	# Select filters
	cmd_string += "cfc 2 \"L%.3d\"; cfc 3 \"R%.3d\"; " % (ah, ah)
	# Set attenuation
	cmd_string += "cfia 2 0 M%.2f; cfia 3 0 M%.2f;\n" % (ahfa, ahfa)

	print "%s %s %s %s" % (al, ah, alfa, ahfa)	
	s.send(cmd_string)
	print cmd_string

# Sensor Functions
def getValue(s):
	if len(s) < 3 or s[2] != '\n':
		raise BadPacket("Data string doesn't end with \n: %s" % repr(s))
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
	return [getValue(f.readline()), getValue(f.readline()), getValue(f.readline())]

def continuous():
	# State vars
	dist_avg_buff = [0]*3
	gyro_acc = 0.0	
	last_gyro = 0.0
	last_switch = 0

	# Log file
	flog = open("log_%s.tsv" % int(time.time()), "w")
	
	while 1:
		# Keyboard input to re-zero gyro_acc
		b = select([sys.stdin.fileno()], [], [], 0)
		if sys.stdin.fileno() in b[0]:
			sys.stdin.read(1)
			gyro_acc = 0.0

		try:
			[gyro_s, dist_s, switches] = sample()
		except BadPacket:
			print("Bad packet, ignoring...")
			continue		

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
		## Offset, scale and invert
		gyro_p = (gyro_s-495)/1024.0*5.0/0.006 # Now in degrees / second
		gyro_p = gyro_p * -1.0
		## Integrate
		gyro_acc += (gyro_p/20.0) + ((gyro_p-last_gyro) / 40.0)  # 20.0Hz is the sampling rate
		last_gyro = gyro_p

		## Quantize and re-range
		# Note: No longer quantizing
		#gyro_q = int((gyro_acc % 360.0)/15)*15
		gyro_q = gyro_acc%360.0

		# Mute button processing
		if last_switch == 0x3ff and switches == 0x3fe:
			s.send("tmi 0;\n")
		last_switch = switches
		
		# Console Output
		print "gyro_s: %.4d\tgyro_p: %.3f\tgyro_acc: %.3f\tgyro_q: %.3d" % (gyro_s, gyro_p, gyro_acc, gyro_q)
		print "dist_s: %.4d\tdist_p: %.3f\tdist_avg: %.3f" % (dist_s, dist_p, dist_avg)
		print "%x" % switches

		# Log file output
		# Time, dist_s, gyro_s
		flog.write("%s\t%s\t%s\n" % (time.time(), dist_s, gyro_s))

		## Distance ranging processing
		dmin = 0.0
		dmax = 0.250
		dist_avg = max(dist_avg, dmin)
		dist_avg = min(dist_avg, dmax)
		dist_avg = 1.0-(dist_avg - dmin)/(dmax-dmin)
		
		# Control output
		d(dist_avg)
		a(gyro_q)

def rotate(delay):
	angle = 0.0
	while 1:
		angle += 1
		angle = angle % 360
		print angle
		a(angle)
		time.sleep(delay)
		

# Run
a(0)
d(1.0)
#continuous()
