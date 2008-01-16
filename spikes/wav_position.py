import wave

hrtf = wave.open("in.wav", "rb")

(nchannels, sampwidth, framerate, nframes, comptype, compname) = hrtf.getparams()

print "[*] HRTF File Details"
print "Channels:\t%s" % nchannels
print "Sample width:\t%s" % sampwidth
print "Sample rate:\t%s" % framerate
print "Framecount:\t%s" % nframes
print "Length (s):\t%s" % (nframes / float(framerate))

print "Extracting L/R Channel ..."
lr = hrtf.readframes(nframes)

l = ""
r = ""
for i in range(0, nframes*sampwidth*2, sampwidth*2):
        l += lr[i:i+sampwidth]
        r += lr[i+3:i+sampwidth*2]
