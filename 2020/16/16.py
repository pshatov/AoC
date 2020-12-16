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
VALID_TICKETS = []
for t in TICKETS:
    ticket_valid = True
    for t_field in t:
        field_valid = False
        for r in RULES.values():
            b, c, d, e = r
            if b <= t_field <= c or d <= t_field <= e:
                field_valid = True
                break
        if not field_valid:
            rate += t_field
            ticket_valid = False
    if ticket_valid:
        VALID_TICKETS.append(t)

print("rate: %d" % rate)

OPTIONS = []
for i in range(len(RULES.keys())):
    OPTIONS.append(list(RULES.keys()))

for ticket_index in range(len(VALID_TICKETS)):
    ticket = VALID_TICKETS[ticket_index]
    print("Ticket %3d of %3d:" % (ticket_index+1, len(VALID_TICKETS)))
    for ticket_field_index in range(len(ticket)):
        ticket_field = ticket[ticket_field_index]
        print("  Field %d of %d: %d" % (ticket_field_index+1, len(ticket), ticket_field))
        for rule_key in RULES.keys():
            a, b, c, d = RULES[rule_key]
            if not (a <= ticket_field <= b or c <= ticket_field <= d):
                OPTIONS[ticket_field_index].remove(rule_key)

KNOWN_OPTIONS = []
for i in range(len(OPTIONS)):
    KNOWN_OPTIONS.append(None)

while True:
    removed = False
    for i in range(len(OPTIONS)):
        opt = OPTIONS[i]
        if len(opt) == 0: continue
        if len(opt) == 1:
            KNOWN_OPTIONS[i] = opt[0]
            for j in range(len(OPTIONS)):
                if j == i: continue
                try:
                    OPTIONS[j].remove(opt[0])
                except ValueError:
                        pass
            opt.remove(opt[0])
            removed = True

    if not removed: break

for li in range(len(INPUT)):
    if INPUT[li] == "your ticket:":
        your_ticket = INPUT[li+1]
your_ticket_parts = your_ticket.split(',')

result = 1
for koi in range(len(KNOWN_OPTIONS)):
    if KNOWN_OPTIONS[koi].startswith('departure'):
        result *= int(your_ticket_parts[koi])

print("result: %d" % result)


