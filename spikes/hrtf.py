import time

i = 0
d = 1
while 1:
	i += d
	if i > 29 or i < 1:
		d = d * -1
	print "boo"+'o'*i+"bs"
	time.sleep(0.2)
