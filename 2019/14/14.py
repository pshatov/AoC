reactions_str = []

reactions = {}

class ReactionComponent:
    
    def __init__(self, name, count):
        self._name = name
        self._count = count
        
    @property
    def name(self):
        return self._name
        
    @property
    def count(self):
        return self._count
        
    def inc(self, count):
        self.count += count
        
    def dec(self, count):
        self.count -= count
        
    @property
    def format(self):
        return "%d %s" % (self._count, self._name)

    @property
    def format_w_supply(self):
        return "%d %s <%d>" % (self._count, self._name, get_supply(self._name))

class ComponentBank:

    def __init__(self, title):
        self._bank = {}
        self._title = title

    def push(self, name, count):
        if not name in self._bank.keys():
            print("    %s: <<< %d %s" % (self._title, count, name))
            self._bank[name] = count
        else:
            print("    %s: +++ %d %s" % (self._title, count, name))
            self._bank[name] += count
            
    def pop(self, name):
        if name in self._bank.keys():
            print("    %s: xxx %d %s" % (self._title, self._bank[name], name))
            del self._bank[name]
        else:
            raise Exception("ComponentBank.pop() failed: name '%s' not in bank!" % (name))
            
    def peek(self, name):
        if not name in self._bank.keys():
            return 0
        else:
            return self._bank[name]
            
    def clear(self):
        self._bank.clear()
        
    def dump(self):
        print("    %s:" % self._title)
        i = 0
        for c in self._bank.keys():
            i += 1
            print("        %d. %d %s" % (i, self._bank[c], c))
        
    @property
    def keys(self):
        return list(self._bank)
        
    @property
    def empty(self):
        return len(self._bank) == 0

def load_reactions_str():
    with open('input.txt') as f:
        for l in f:
            reactions_str.append(l.strip())

def parse_component_str(s):
    ss = s.split(" ")
    return ReactionComponent(ss[1], int(ss[0]))

def parse_reactions_str():
    for r in reactions_str:
        r_split = r.split("=>")
        r_dst = parse_component_str(r_split[1].strip())
        reactions[r_dst] = []
        r_src_list = r_split[0].strip().split(",")
        for r_src_next in r_src_list:
            r_src = parse_component_str(r_src_next.strip())
            reactions[r_dst].append(r_src)

def find_reaction_by_dst_name(dst_name, reacts):
    for r in reacts.keys():
        if r.name == dst_name: return r

def can_get_dst_name_from_ore(dst_name, reacts):
    r = find_reaction_by_dst_name(dst_name, reacts)
    if r is not None:
        r_src_list = reacts[r]
        if len(r_src_list) == 1:
            r_src = r_src_list[0]
            if r_src.name == "ORE":
                return True
    return False

def dump_reactions(reacts):

    j = 0
    for r in reacts.keys():
        j += 1
        print("%d. " % (j), end='')
        i = 0
        r_dst = r
        r_src_list = reacts[r]
        for r_src in r_src_list:
            i += 1
            if i > 1: print(", ", end='')
            print("%s" % r_src.format, end='')
        print(" => %s" % (r_dst.format))

def dump_reaction_dst_name(dst_name, reacts):

    for r in reacts.keys():
        i = 0
        r_dst = r
        if r_dst.name == dst_name:
            r_src_list = reacts[r]
            for r_src in r_src_list:
                i += 1
                if i > 1: print(", ", end='')
                print("%s" % r_src.format, end='')
            print(" => %s" % (r_dst.format))


load_reactions_str()
parse_reactions_str()


known_components = []
for r in reactions.keys():
    known_components.append(r.name)
    
print("Known components:")
for i in range(len(known_components)):
    print("%d. %s" % (i+1, known_components[i]))

have_components = []

layers = []
print("Looking for final reaction:")
layers.append([])
for r in reactions:
    if r.name == "FUEL":
        layers[0].append(r)
        dump_reaction_dst_name(r.name, reactions)
        have_components.append(r.name)
        break
        
print("Looking for initial reactions:")
layers.insert(0, [])
for r in reactions:
    r_src_list = reactions[r]
    if len(r_src_list) == 1:
        r_src = r_src_list[0]
        if r_src.name == "ORE":
            layers[0].append(r)
            dump_reaction_dst_name(r.name, reactions)
            have_components.append(r.name)

print("Determining order of reactions:")
while len(have_components) < len(known_components):

    print("Have components:")
    for i in range(len(have_components)):
        print("%d. %s" % (i+1, have_components[i]))

    new_components = []
    layers.insert(-1, [])
    
    print("What we can generate:")
    for r in reactions:
        print("%s: " % (r.name), end='')
        if r.name in have_components:
            print("already have")
        else:
            print("don't have, ", end='')
            feasible = True
            r_src_list = reactions[r]
            for r_src in r_src_list:
                if not r_src.name in have_components:
                    feasible = False
                    break
            if not feasible:
                print("and can't generate")
            else:
                print("but can generate")
                dump_reaction_dst_name(r.name, reactions)
                new_components.append(r.name)
                layers[-2].append(r)
    
    have_components += new_components

print("Order of reactions:")
for i in range(len(layers)):
    print("%d." % (i))
    for r in layers[i]:
        dump_reaction_dst_name(r.name, reactions)

depot = {}
for c in known_components: depot[c] = 0
depot["FUEL"] = -1

def print_producing(cc):
    for c in cc:
        print("%s" % (c))
        
def print_missing(cc):
    for c in cc:
        print("%d %s" % (-depot[c], c))

def get_missing_stuff():
    ret = []
    for c in depot.keys():
        if depot[c] < 0:
            ret.append(c)
    return ret

def get_producing_stuff(l):
    ret = []
    for r in layers[l]:
        ret.append(r.name)
    return ret

def run_reaction(d):
    
    total = 0
    
    r = find_reaction_by_dst_name(d, reactions)
    
    depot[r.name] += r.count
    
    r_src_list = reactions[r]
    for r_src in r_src_list:
        if r_src.name == "ORE":
            total += r_src.count
        else:
            depot[r_src.name] -= r_src.count

    return total
    
total_ore = 0
for l in range(len(layers)-1, -1, -1):
    
    print("Layer %d..." % (l))
    
    missing = get_missing_stuff()
    producing = get_producing_stuff(l)
    
    print("Stuff we're missing:")
    print_missing(missing)
    print("Stuff we're producing:")
    print_producing(producing)
    
    for m in missing:
        if m in producing:
            print("Generating %s: " % (m), end='')
            iters = 0
            while depot[m] < 0:
                iters += 1
                total_ore += run_reaction(m)
            print("x%d" % (iters))
    

print("total_ore = %d" % (total_ore))
