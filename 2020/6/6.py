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
            
GROUPS_YES = []
for grp in GROUPS:
    yes = []
    for grp_line in grp:
        for line_ans in grp_line:
            if not line_ans in yes:
                yes.append(line_ans)
    GROUPS_YES.append(yes)
    
sum = 0
for grp_yes in GROUPS_YES:
    sum += len(grp_yes)
    
print("sum: %d" % sum)
            
        