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
