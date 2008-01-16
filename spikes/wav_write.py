import wave
import random

def itos(i):
    b0 = i & 0xFF00 >> 8
    b1 = i & 0x00FF

    c0 = chr(b0)
    c1 = chr(b1)

    return(c0+c1)

w = wave.open("out.wav", "wb")

w.setnchannels(2)
w.setsampwidth(2)
w.setframerate(44100)

# (2 bytes left channel)(2 bytes right channel)

def white_noise():

    r0 = 0 # every 2 samples
    r1 = 0 # every 3 samples
    r2 = 0 # every 5 samples
    r3 = 0 # every 9 samples
    r4 = 0 # every 17 samples
    r5 = 0 # every 33 samples
    r6 = 0 # every 65 samples

    s = ""
    for i in range(0,44100):
        # Generate white noise
        if i % 2 == 0:
            r0 = random.randint(0, 65535/7)
        if i % 3 == 0:
            r1 = random.randint(0, 65535/7)
        if i % 5 == 0:
            r2 = random.randint(0, 65535/7)
        if i % 9 == 0:
            r3 = random.randint(0, 65535/7)
        if i % 17 == 0:
            r4 = random.randint(0, 65535/7)
        if i % 33 == 0:
            r4 = random.randint(0, 65535/7)
        if i % 65 == 0:
            r4 = random.randint(0, 65535/7)
       
        o = (r0 + r1 + r2 + r3 + r4) % 65535  # Clamp at 65535

        #print("%i + %i + %i + %i + %i at %i = %i" % (r0, r1, r2, r3, r4, i, o))

        s += itos(o) + itos(0)
    return s

def pink_noise():
    s = ""
    for i in range(0, 44100):
        # Generate pink noise
        pass

w.writeframes(white_noise())
w.close()
