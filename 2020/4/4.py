import re

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

DOCS_VALID_KEYS = []
for d in DOCS:
    is_valid = True
    for k in REQUIRED_KEYS:
        if not k in d.keys():
            is_valid = False
            break
    if is_valid:
        DOCS_VALID_KEYS.append(d)
    
print("num_valid_keys: %d" % len(DOCS_VALID_KEYS))
   
re_byr = re.compile("(\d{4})")
re_iyr = re.compile("(\d{4})")
re_eyr = re.compile("(\d{4})")
re_hgt_cm = re.compile("(\d{3})cm")
re_hgt_in = re.compile("(\d{2})in")
re_hcl = re.compile("\#([0-9a-f]){6}")
re_ecl = re.compile("(amb|blu|brn|gry|grn|hzl|oth)")
re_pid = re.compile("(\d{9})")

num_bad_byr = 0
num_bad_iyr = 0
num_bad_eyr = 0
num_bad_hgt = 0
num_bad_hgt_cm = 0
num_bad_hgt_in = 0
num_bad_hcl = 0
num_bad_ecl = 0
num_bad_pid = 0

def validate_values(p):
    
    global num_bad_byr
    global num_bad_iyr
    global num_bad_eyr
    #
    global num_bad_hgt
    global num_bad_hgt_cm
    global num_bad_hgt_in
    #
    global num_bad_hcl
    global num_bad_ecl
    global num_bad_pid
    
    m_byr = re.fullmatch(re_byr, p['byr'])
    m_iyr = re.fullmatch(re_iyr, p['iyr'])
    m_eyr = re.fullmatch(re_eyr, p['eyr'])
    #
    m_hgt_cm = re.fullmatch(re_hgt_cm, p['hgt'])
    m_hgt_in = re.fullmatch(re_hgt_in, p['hgt'])
    #
    m_hcl = re.fullmatch(re_hcl, p['hcl'])
    m_ecl = re.fullmatch(re_ecl, p['ecl'])
    m_pid = re.fullmatch(re_pid, p['pid'])
    
    if not m_hcl:
        num_bad_hcl += 1
        #print("Bad 'hcl': %s (%d)" % (p['hcl'], num_bad_hcl))
        return False
    
    if not m_ecl:
        num_bad_ecl += 1
        #print("Bad 'ecl': %s (%d)" % (p['ecl'], num_bad_ecl))
        return False
        
    if not m_pid:
        num_bad_pid += 1
        #print("Bad 'pid': %s (%d)" % (p['pid'], num_bad_pid))
        return False
    
    v_byr = int(m_byr.group(1))
    v_iyr = int(m_iyr.group(1))
    v_eyr = int(m_eyr.group(1))
    #
    v_hgt_cm = int(m_hgt_cm.group(1)) if not m_hgt_cm is None else None
    v_hgt_in = int(m_hgt_in.group(1)) if not m_hgt_in is None else None

    if not (1920 <= v_byr <= 2002):
        num_bad_byr += 1
        #print("Bad 'byr': %d (%d)" % (v_byr, num_bad_byr))
        return False
        
    if not (2010 <= v_iyr <= 2020):
        num_bad_iyr += 1
        #print("Bad 'iyr': %d (%d)" % (v_iyr, num_bad_iyr))
        return False

    if not (2020 <= v_eyr <= 2030):
        num_bad_eyr += 1
        #print("Bad 'eyr': %d (%d)" % (v_eyr, num_bad_eyr))
        return False

    if v_hgt_cm is None and v_hgt_in is None:
        num_bad_hgt += 1
        #print("Bad 'hgt': %s (%d)" % (p['hgt'], num_bad_hgt))
        return False

    if not v_hgt_cm is None and (not (150 <= v_hgt_cm <= 193)):
        num_bad_hgt_cm += 1
        #print("Bad 'hgt' (cm): %d (%d)" % (v_hgt_cm, num_bad_hgt_cm))
        return False
        
    if not v_hgt_in is None and (not ( 59 <= v_hgt_in <=  76)):
        num_bad_hgt_in += 1
        #print("Bad 'hgt' (in): %d (%d)" % (v_hgt_in, num_bad_hgt_in))
        return False

    return True
    

DOCS_VALID_VALUES = []
for d in DOCS_VALID_KEYS:
    if validate_values(d):
        DOCS_VALID_VALUES.append(d)
    
print("num_valid_values: %d" % len(DOCS_VALID_VALUES))


