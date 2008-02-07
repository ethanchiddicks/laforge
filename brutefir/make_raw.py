import os
import sys

block = """coeff "%s" {
	filename: "%s.raw";
	format: "S24_LE";
};

"""

for a in range(0, 360, 15):
	infile = "IRC_1003_C_R0195_T%.3d_P000.wav" % a
	os.popen("sox %s -c 1 L%.3d.raw mixer -l" % (infile, a))
	os.popen("sox %s -c 1 R%.3d.raw mixer -r" % (infile, a))
	sys.stdout.write(block % ("R" + "%.3d" % a, "R" + "%.3d" % a))	
	sys.stdout.write(block % ("L" + "%.3d" % a, "L" + "%.3d" % a))	
