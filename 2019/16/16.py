import numpy

SIGNAL = []

with open('input.txt') as f:
    s = f.readline().strip()
    for i in range(len(s)):
        SIGNAL.append(int(s[i]))      

def fft(S):
    L = len(S)
    for i in range(L):
        t = 0
        for j in range(i, L, 4*(i+1)):
            for k in range(i+1):
                n = j + k
                if n == L: break
                t += S[n]
                #print("  +[%d]" % n)
        for j in range(3*(i+1)-1, L, 4*(i+1)):
            for k in range(i+1):
                n = j + k
                if n == L: break
                t -= S[n]
                #print("  -[%d]" % n)
        T[i] = abs(t) % 10
        #print("%d -> %d" % (t, abs(t) % 10))
    return T


def fft_cheat():
    LSS = len(SS)
    SIGMA = numpy.sum(SS)
    for n in range(LSS):
        T[n] = SIGMA % 10
        SIGMA -= SS[n]
    if SIGMA != 0:
        raise RuntimeError
    for n in range(LSS):
        SS[n] = T[n]
    

NUM_PHASES = 100

if True:
    S = SIGNAL[:]
    T = S[:]

    print("S")
    for i in range(NUM_PHASES):
        print("Phase %3d: " % (i+1), end='')
        S = fft(S)
    
        for j in range(8):
            print('%d' % S[j], end='')
        print("...")

N = 10000
OFFSET = int(s[0:7])
LS = len(SIGNAL)
LSS = N * LS
REM = LSS - OFFSET

print("OFFSET = %d" % OFFSET)
print("LSS    = %d" % LSS)
print("REM    = %d" % REM)

REM_S = REM // len(SIGNAL)
LEADIN = REM - REM_S * LS

print("REM_S  = %d" % REM_S)
print("LEADIN = %d" % LEADIN)
print("REM_S  = %d" % REM_S)

SS = numpy.zeros(REM, dtype=numpy.int32)

for r in range(LEADIN):
    rr = len(SIGNAL) - LEADIN + r
    SS[r] = SIGNAL[rr]
    
for i in range(REM_S):
    for j in range(len(SIGNAL)):
        r += 1
        SS[r] = SIGNAL[j]

print(SS)

T = numpy.zeros(REM, dtype=numpy.int32)

print("SS")
for i in range(NUM_PHASES):
    print("Phase %3d: " % (i+1), end='')
    fft_cheat()
    for j in range(8):
        print('%d' % SS[j], end='')
    print("...")
