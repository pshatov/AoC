N = 25
PORT = []
with open('input.txt') as f:
    for fl in f:
        PORT.append(int(fl.strip()))

WND = PORT[0:N]
        
def is_wnd_valid(offset):
    for i in range(N-1):
        for j in range(i+1, N):
            if WND[i] + WND[j] == PORT[offset]:
                return True
    return False

for k in range(N, len(PORT)):
    #print("k = %d" % k)
    v = is_wnd_valid(k)
    if not v:
        print("%d [%d]" % (PORT[k], k))
        break
    del WND[0]
    WND.append(PORT[k])
    #print(WND)

l, found = 2, False
while not found:
    l1 = l - 1
    for p in range(0, len(PORT) - l1):
        k_start, k_stop = p, p + l1
        if k_start <= k <= k_stop:
            continue
        #print("%d, %d" % (k_start, k_stop))
        if sum(PORT[k_start:k_stop+1]) == PORT[k]:
            print("l: %d" % l)
            print("k_start, k_stop: %d, %d" % (k_start, k_stop))
            print("%d" % (min(PORT[k_start:k_stop+1]) + max(PORT[k_start:k_stop+1])))
            found = True
            break
    l += 1
