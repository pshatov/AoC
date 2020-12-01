N = []

with open('input.txt') as f:
   for fl in f:
    N.append(int(fl))

found = False
for i in range(len(N)-1): # i = 1, 2, ..., N-1
    if found: break
    for j in range(i+1, len(N)): # j = i+1, i+2, ..., N
        if N[i] + N[j] == 2020:
            print("i = %d" % i)
            print("j = %d" % j)
            print("N[i] = %d" % N[i])
            print("N[j] = %d" % N[j])
            print("N[i] * N[j] = %d" % (N[i] * N[j]))
            found = True
            break

found = False
for i in range(len(N)-2): # i = 1, 2, ..., N-2
    if found: break
    for j in range(i+1, len(N)-1): # j = i+1, i+2, ..., N-1
        if found: break
        for k in range(j+1, len(N)): # k = j+1, j+2, ..., N
            if N[i] + N[j] + N[k] == 2020:
                print("i = %d" % i)
                print("j = %d" % j)
                print("k = %d" % k)
                print("N[i] = %d" % N[i])
                print("N[j] = %d" % N[j])
                print("N[k] = %d" % N[k])
                print("N[i] * N[j] * N[j] = %d" % (N[i] * N[j] * N[k]))
                found = True
                break
