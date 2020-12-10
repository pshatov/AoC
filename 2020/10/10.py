A = [] # initial list of adapters
with open('input.txt') as f:
    for fl in f:
        A.append(int(fl.strip()))

J = 0 # outlet output
C = [] # final (sorted) list of adapters

while len(A) > 0:
    
    #print("len(A): %d" % len(A))
    
    AI = [] # indices of suitable adapters
    
    for k in range(len(A)):
        if 1 <= (A[k] - J) <= 3:
            AI.append(k)
    
    min_ai = AI[0]
    min_aj = A[min_ai]
    for k in range(1, len(AI)):
        ai = AI[k]
        aj = A[ai];
        if aj < min_aj:
            min_ai, min_aj = ai, aj
            
    #print("  %d" % min_aj)
    C.append(min_aj)
    del A[min_ai]
    J = min_aj
    
prev_j = 0
delta1, delta3 = 0, 0
for k in range(len(C)):
    d = C[k] - prev_j
    if d == 1: delta1 += 1
    if d == 3: delta3 += 1
    prev_j = C[k]
    
delta3 += 1

print("delta1: %d" % delta1)
print("delta3: %d" % delta3)
print("%d" % (delta1 * delta3))


G = []
G.append([0])

for k in range(len(C)):
    if (C[k] - G[-1][-1]) == 3:
        G.append([])
    G[-1].append(C[k])
    
N = None
Z = None

def try_remove(g, i):
    global N, Z
    if 1 <= (g[i+1] - g[i-1]) <= 3:
        LL = g[:]
        del LL[i]
        if LL not in Z:
            N += 1
            Z.append(LL)
            print("LL: ", LL)
            for ii in range(1, len(LL)-1):
                try_remove(LL, ii)

def calc_vars(g):
    global N, Z
    N = 0
    Z = []
    for k in range(1, len(g)-1):
        try_remove(g, k)
    return N

    


V = []
for grp in G:
    print("G: ", grp)
    if len(grp) > 2:
        n = calc_vars(grp)
        print("  %d" % n)
        V.append(n)
    else:
        print("  X")
        
T = 1
for v in V:
    T *= (v + 1)
#T += 1

print("T: %d" % T)


