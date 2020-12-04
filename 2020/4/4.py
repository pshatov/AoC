BATCH = []
with open('input.txt') as f:
    for fl in f:
        BATCH.append(fl.strip())
 
RECS = []
for batch_line in BATCH:
    if not batch_line:
        RECS.append([])
    else:
        if len(RECS) == 0:
            RECS.append([])
        RECS[-1].append(batch_line)
        
DOCS = []
for rec in RECS:
    DOCS.append({})
    for rec_part in rec:
        rec_part_items = rec_part.split(' ')
        for rec_item in rec_part_items:
            rec_key, rec_value = rec_item.split(':')
            DOCS[-1][rec_key] = rec_value

REQUIRED_KEYS = ['byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid']
            
num_valid = 0
for d in DOCS:
    is_valid = True
    for k in REQUIRED_KEYS:
        if not k in d.keys():
            is_valid = False
            break
    if is_valid:
        num_valid += 1
    
print("num_valid: %d" % num_valid)
    
    