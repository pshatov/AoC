import re

RULES = {}
EMPTY = []

COLOR = "shiny gold"

key_regexp = re.compile("([a-z]+ [a-z]+) bags contain (.+)\.")
value_regexp = re.compile("(\d+) ([a-z]+ [a-z]+) bags?")

def load_rules():
    with open('input.txt') as f:
        for fl in f:
            parse_rule(fl.strip())
            
def parse_rule(rule):
    m = key_regexp.fullmatch(rule)
    if m is None: raise RuntimeError
    
    key = m.group(1)
    values = m.group(2)
    
    RULES[key] = {}
    
    values_list = values.split(', ')
    for next_value in values_list:
        if next_value == "no other bags":
            EMPTY.append(next_value)
            continue
        m = value_regexp.fullmatch(next_value)
        m_count = int(m.group(1))
        m_color = m.group(2)
        RULES[key][m_color] = m_count

        if m is None: raise RuntimeError
        #RULES[key][
    
    

def main():
    load_rules()

    C = []

    round = 0
    for k in RULES.keys():
        if COLOR in RULES[k].keys():
            #print("%d: %s" % (round, k))
            C.append(k)
    
    keep_adding = True
    while keep_adding:
        added = 0
        round += 1
        for k in RULES.keys():
            for c in C:
                if c in RULES[k].keys() and k not in C:
                    #print("%d: %s" % (round, k))
                    C.append(k)
                    added += 1

        keep_adding = added > 0
        #print("round: %d, added: %d" % (round, added))

    print("len(C): %d" % len(C))

if __name__ == '__main__':
    main()
