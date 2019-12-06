orbits = dict()
with open('input.txt') as f:
    for line in f:
        center, satellite = line.strip().split(")")
        orbits[satellite] = center

def calc_distance_to_com(orbs, sat):
    dist = 1
    cent = orbs[sat]
    while cent != "COM":
        cent = orbs[cent]
        dist += 1
    return dist

checksum = 0
for satellite in orbits.keys():
    checksum += calc_distance_to_com(orbits, satellite)
print("checksum = %d" % checksum)    
