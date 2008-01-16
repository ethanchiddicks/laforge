import wave

w = wave.open("in.wav", "rb")

(nchannels, sampwidth, framerate, nframes, comptype, compname) = w.getparams()

print "Channels:\t%s" % nchannels
print "Sample width:\t%s" % sampwidth
print "Sample rate:\t%s" % framerate
print "Framecount:\t%s" % nframes
print "---"
print "Length (s):\t%s" % (nframes / float(framerate))
