import socket
import time

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("localhost", 3000))

def d(dist):
	s.send("cfia 0 0 M%f; cfia 1 0 M%f;\n" % (dist, dist))

def a(ang):
	s.send("cfc 0 \"L%.3d\"; cfc 1 \"R%.3d\";\n" % (ang, ang))

def rotate(delay=0.25):
	ang = 0
	while 1:
		ang += 15
		ang = ang % 360
		a(ang)
		time.sleep(delay)

def voob(delay=0.10):
	dist = 1.0
	factor = -0.01
	while 1:
		dist += factor
		if dist >= 1.0 or dist <= 0.1:
			factor = factor * -1.0
		d(dist)
		time.sleep(delay)
