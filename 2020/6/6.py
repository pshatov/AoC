GROUPS = []
with open('input.txt') as f:
    for fl in f:
        fls = fl.strip()
        if not fls:
            GROUPS.append([])
        else:
            if len(GROUPS) == 0:
                GROUPS.append([])
            GROUPS[-1].append(fls)
            
GROUPS_ANY = []
for grp in GROUPS:
    yes = []
    for grp_line in grp:
        for line_ans in grp_line:
            if not line_ans in yes:
                yes.append(line_ans)
    GROUPS_ANY.append(yes)
    
sum = 0
for grp_yes in GROUPS_ANY:
    sum += len(grp_yes)
    
print("sum: %d" % sum)
            
GROUPS_ALL = []
for grp in GROUPS:
    GROUPS_ALL.append([])
    for i in range(ord('a'), ord('z')+1):
        c = chr(i)
        all = True
        for grp_line in grp:
            if not c in grp_line:
                all = False
                break
        if all:
            GROUPS_ALL.append(c)

sum = 0
for grp_all in GROUPS_ALL:
    sum += len(grp_all)
    
print("sum: %d" % sum)
