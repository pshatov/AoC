N = []

with open('input.txt') as f:
   for fl in f:
    N.append(int(fl))
    
for i in range(len(N)-1): # i = 1, 2, ..., N-1
    for j in range(i+1, len(N)): # j = i+1, i+2, ..., N
        if N[i] + N[j] == 2020:
            print("i = %d" % i)
            print("j = %d" % j)
            print("N[i] = %d" % N[i])
            print("N[j] = %d" % N[j])
            print("N[i] * N[j] = %d" % (N[i] * N[j]))
            
