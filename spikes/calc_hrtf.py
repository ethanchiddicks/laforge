import wave
import ctypes

# Configuration variables.  You might need to change these.
global_config = {
            'HRIR_DIR' : '/Users/paulwalker/laforge/hrirs/',
            'NUM_TAPS' : 128,
            'ANGLE_STEP' : 5,
            }

class SoundSourceFilter():
    def __init__(self, channel):
            # Initialize HRIR tables
            self._hrirs = {}
            for angle in range(0, 360, global_config['ANGLE_STEP']):
                self._hrirs[angle] = self.read_hrir_from_wav(
                        global_config['HRIR_DIR'] + '%s0e%.3da.wav' % (channel, angle))

            # Initialize initial filter references
            self._filter_refs = [0]*global_config['NUM_TAPS']

            # Initialize the initial signal buffer
            self._signal_buff = [0]*global_config['NUM_TAPS']

    def process_signal(self, signal, angle):
        r = []
        for i in range(0, len(signal)):
            a = float(i)/len(signal)*180.0+angle
            o = self.tick(signal[i], a)
            r.append(o)
        return r

    def tick(self, next_sample, angle):
        self._ref_tick(angle)

        self._buff_tick(next_sample)

        return self._calc_output()

    def _calc_output(self):

        f = self._calc_filter()

        # Multiply accumulate
        a = 0
        for i in range(0, global_config['NUM_TAPS']):
            s = f[i] * self._signal_buff[i]
	    a += s

        return a
            
    def _calc_filter(self):
        f = []
        for i in range(0, global_config['NUM_TAPS']):
            f.append(self._hrirs[self._filter_refs[i]][i])
        return f

    def _buff_tick(self, next_sample):
        '''
        Modify the signal buffer to represent the next tick.
        '''

        # Note: this will most likely be implemented on the hardware as a
        # circular buffer.
        
        # Remove the last sample
        self._signal_buff.pop(len(self._signal_buff)-1)

        # Insert a new sample at the front
        self._signal_buff.insert(0, next_sample)

    def _ref_tick(self, angle):
        '''
        Modify the filter references to represent the next tick.
        '''

        # Note: this will most likely be implemented on the hardware as a
        # circular buffer.
        
        # Remove the last filter reference
        self._filter_refs.pop(len(self._filter_refs)-1)

        # Insert a new filter reference at the front
        self._filter_refs.insert(0, self.quantize_angle(angle))

    def quantize_angle(self, angle):
        '''
        Returns a floor-quantized version of the angle in the range of 0-360.
        '''
        
        angle = angle % 360
        r = int(int(angle / global_config['ANGLE_STEP']) * global_config['ANGLE_STEP'])
        return r

    @classmethod
    def read_hrir_from_wav(self, filename):
        '''
        Processes only the first channel of the file.
        '''
        w = wave.open(filename, "rb")
        
        (nchannels, sampwidth, framerate, 
            nframes, comptype, compname) = w.getparams()

        if sampwidth != 2:
            raise Exception("Can only handle 16 bit wav files.")
        
        r = []
    
        data = w.readframes(nframes)
    
        for i in range(0, nframes*sampwidth, sampwidth):
            v = 0
            v += ord(data[i]) 
            v += ord(data[i+1]) << 8
	    v = ctypes.c_short(v).value
            r.append(v)
    
        return r

    @classmethod
    def write_to_wav(self, filename, o, gain):
        # Normalize signal to -(2**15) to (2**15)-1 range. 
        peak = max(max(o), min(o)*-1)
        o = [int(float(sample)*gain*(2**15-1)) for sample in o]
    
        w = wave.open(filename, "wb")

        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(44100)

        # Turn into string
        o2 = ""
        for s in o:
            o2 += chr(s&0x00FF)
            o2 += chr((s&0xFF00)>>8)

        w.writeframes(o2)

if __name__ == '__main__':
    a = 270.0

    s = SoundSourceFilter('R')
    i = s.read_hrir_from_wav("/Users/paulwalker/laforge/sources/whitenoise.wav")
    o_right = s.process_signal(i, a)
    
    s = SoundSourceFilter('L')
    i = s.read_hrir_from_wav("/Users/paulwalker/laforge/sources/whitenoise.wav")
    o_left = s.process_signal(i, a)
    
    peak_right = max(max(o_right), min(o_right)*-1)
    peak_left = max(max(o_left), min(o_left)*-1)
    peak = max(peak_left, peak_right)
    gain = 1.0/peak
    s.write_to_wav("blahL.wav", o_left, gain)
    s.write_to_wav("blahR.wav", o_right, gain)
