import os
import sys

sys.path.append(os.getcwd() + "\..")

from vt100 import wait_key
from IntcodeClass import Intcode


N = 50
GW = 0
BCAST = 255
NAT = []
NICS = []
QUEUE_FROM = {}
QUEUE_TO = {}

def main():

    opcodes = Intcode.load_opcodes('input.txt')
    
    for n in range(N):
        NICS.append(Intcode())
        NICS[n].reset(opcodes)
        NICS[n].push_input(n)
        NICS[n].run()
        QUEUE_FROM[n] = []
        QUEUE_TO[n] = []
    
    cycle = 0
    seen_first_nat = False
    seen_last_nat_y = -1
    while True:

        print("cycle = %d" % cycle)

        for n in range(N):
            nic = NICS[n]
            if nic.is_stopped():
                raise RuntimeError
        
        for n in range(N):
            nic = NICS[n]
            while nic.can_pop_output():
                byte = nic.pop_output()
                QUEUE_FROM[n].append(byte)
                print("#%02d >> %d" % (n, byte))

        for n in range(N):
            qf = QUEUE_FROM[n]
            while len(qf) >= 3:
                z = qf.pop(0)
                x = qf.pop(0)
                y = qf.pop(0)
                if z == BCAST:
                    NAT.clear()
                    NAT.append(x)
                    NAT.append(y)
                    print("%d, %d >> NAT" % (x, y))
                    if not seen_first_nat:
                        print("seen_first_nat == %s" % seen_first_nat)
                        print("Press space to continue...")
                        sys.stdout.flush()
                        wait_key()
                        seen_first_nat = True
                else:
                    qt = QUEUE_TO[z]
                    qt.append(x)
                    qt.append(y)
                    print("%d, %d >> #%02d" % (x, y, z))

        net_is_idle = True
        for n in range(N):
            nic = NICS[n]
            if nic.is_waiting_input():
                q = QUEUE_TO[n]
                if len(q) > 0: net_is_idle = False
                if len(q) < 2:
                    nic.push_input(-1)
                    nic.run()
                else:
                    x = q.pop(0)
                    y = q.pop(0)
                    nic.push_input(x)
                    nic.push_input(y)
                    nic.run()
            else:
                raise RuntimeError
        
        if cycle > 0 and net_is_idle:
            print("network is idle...")
            qt = QUEUE_TO[GW]
            x = NAT[0]
            y = NAT[1]
            qt.append(x)
            qt.append(y)
            print("%d, %d >> GW" % (x, y))
            
            if y == seen_last_nat_y:
                print("seen_last_nat_y == %d" % seen_last_nat_y)
                print("Press space to finish...")
                sys.stdout.flush()
                wait_key()
                return
                
            seen_last_nat_y = y
            
        cycle += 1
                  
if __name__ == "__main__":
    main()
