# Generates azimuth and distance measurements from a listener to a source
# with the source moving at a certain speed, at 44.1 kHz

import math

# Listener starts at (0m,0m)

ldx = 0.0
ldy = 1.5 # 1.5 m/s is approximate typical male walking speed

sx = 3.0
sy = 5.0

length = 5.0 # In seconds
rate = 44100 # 44.1 kHz to correspond to sound generation rate

for tstep in range(0, rate*length+1):
        t = tstep/float(rate)

        lx = t*ldx
        ly = t*ldy

        # Distance
        dx = sx - lx
        dy = sy - ly
        d = math.sqrt(dx**2 + dy**2)

        az = math.sinh(1/d*dy) / math.pi * 180.0

        # Put in standard angular coordinate system for psychoacoustics
        az = az * -1.0 + 90.0

        # Put into 5 degree chunks
        az = int(az/5)*5

        # Guarantee in range 0-360
        az = az % 360

        # Encode as byte
        az_c = chr(az)

        # Distance in range of 0..6 m

        #print "%s: (%s, %s), d = %s, theta = %s" % (t, lx, ly, d, theta)
        print "%s,%s" % (az_c, d)
