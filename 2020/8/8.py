CODE = []
with open('input.txt') as f:
    for fl in f:
        CODE.append(tuple(fl.strip().split(' ')))

MARK = []
for i in range(len(CODE)):
    MARK.append(False)
    

def step(code, pc, acc):
    
    if MARK[pc]:
        raise RuntimeError
        
    MARK[pc] = True
    
    op, i_arg = code[pc]
    arg = int(i_arg)
    
    new_pc, new_acc = pc + 1, acc
    
    if op == 'acc': new_acc += arg
    if op == 'jmp': new_pc += arg - 1 #!
    
    return new_pc, new_acc
    
    
pc, acc = 0, 0
while True:

    try:
        pc, acc = step(CODE, pc, acc)
    except RuntimeError:
        print("acc: %d" % acc)
        break

fixed = False    
for i in range(len(CODE)):
    
    #print("i: %d / %d" % (i+1, len(CODE)))
    
    # restore code
    NEW_CODE = CODE[:]
    
    # decode
    op, i_arg = CODE[i]
    
    # don't try to fix 'acc'
    if op == 'acc':
        #print('  acc')
        continue
    
    # try to fix
    if op == 'nop':
        NEW_CODE[i] = 'jmp', i_arg
        #print("  nop -> jmp")
    elif op == 'jmp':
        NEW_CODE[i] = 'nop', i_arg
        #print("  jmp -> nop")
    
    # run fixed code
    pc, acc = 0, 0
    for i in range(len(CODE)):
        MARK[i] = False
    while True:
        
        if pc == len(CODE):
            fixed = True
            break
            
        try:
            pc, acc = step(NEW_CODE, pc, acc)
        except RuntimeError:
            #print("RuntimeError: pc:%d, acc:%d" % (pc, acc))
            break

    if fixed: break
    
print("acc: %d" % acc)
