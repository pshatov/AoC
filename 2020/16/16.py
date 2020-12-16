import re

rule_re = re.compile("([a-z]+\s?[a-z]*)\: (\d+)\-(\d+) or (\d+)\-(\d+)")

INPUT = []
with open('input.txt') as f:
    for fl in f:
        fls = fl.strip()
        if fls:
            INPUT.append(fl.strip())

RULES = {}
for l in INPUT:
    m = rule_re.fullmatch(l)
    if m is not None:
        a = m.group(1)
        bcde = int(m.group(2)), int(m.group(3)), int(m.group(4)), int(m.group(5))
        RULES[a] = bcde
        
TICKETS = None
for l in INPUT:
    if TICKETS is None:
        if l == "nearby tickets:":
            TICKETS = []
    else:
        fields = l.split(',')
        TICKETS.append([])
        for f in fields:
            TICKETS[-1].append(int(f))
            
rate = 0
for t in TICKETS:
    for t_field in t:
        valid = False
        for r in RULES.values():
            b, c, d, e = r
            if b <= t_field <= c or d <= t_field <= e:
                valid = True
                break
        if not valid: rate += t_field

print("rate: %d" % rate)
