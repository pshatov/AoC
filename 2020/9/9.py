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
        print("%d" % PORT[k])
        break
    del WND[0]
    WND.append(PORT[k])
    #print(WND)

