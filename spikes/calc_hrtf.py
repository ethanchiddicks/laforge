import wave

# Configuration variables.  You might need to change these.
global_config = {
            'HRIR_DIR' : 'h:\laforge\hrirs\\',
            'NUM_TAPS' : 128,
            'ANGLE_STEP' : 5,
            }

class SoundSourceFilter():
    def __init__(self):
            # State variables
            self._angle = 0.0
            
            # Initialize HRIR tables
            self._hrirs = {}
            for angle in range(0, 360, global_config['ANGLE_STEP']):
                self._hrirs[angle] = self.read_hrir_from_wav(
                        global_config['HRIR_DIR'] + 'L0e%.3da.wav' % angle)

            # Initialize initial filter references
            self._filter_refs = [0]*global_config['NUM_TAPS']
            

    def tick(self):
        '''
        Modify the filter references to represent the next tick.
        '''

        # TODO: this will most likely be implemented on the hardware as a
        # circular buffer.
        
        # Remove the last filter reference
        self._filter_refs.pop(len(self._filter_refs)-1)

        # Insert a new filter reference at the front
        self._filter_refs.insert(0, self.get_angle())

    def get_angle(self):
        '''
        Returns a quantized version of the angle.
        '''

        # TODO: this is where you left off




    @classmethod
    def read_hrir_from_wav(self, filename):
        '''
        Processes only the first channel of the file.
        '''
        w = wave.open(filename, "rb")
        
        (nchannels, sampwidth, framerate, 
            nframes, comptype, compname) = w.getparams()
        
        r = []
    
        data = w.readframes(nframes)
    
        for i in range(0, nframes*sampwidth, sampwidth):
            v = 0
            for j in range(0, sampwidth):
               v += ord(data[i+j]) << 8*(sampwidth-j-1)
            r.append(v)
    
        return r


def make_delay(d, taps):
    F = [0.0]*taps
    F[d] = 1.0
    return F

def make_ramp(l, p):
    r = [None]*l
    for i in range(0, l):
        r[i] = (i%p)/(float(p)-1.0)
    return r

def make_firs(num_fir, num_tap):
    # Generate FIRs with all possible delays
    f = [None]*num_fir
    for i in range(0, num_fir):
        f[i] = make_delay(i, num_tap)
    return f

if __name__ == '__main__':
    num_fir = 4
    num_tap = 4

    f = make_firs(num_fir, num_tap)
    s = make_ramp(10, 5)

    fr = [0]*num_tap

    fr[3] = 1

    F = [None]*num_fir

    for i in range(0, num_tap):
        F[i] = f[fr[i]][i]

    print F
