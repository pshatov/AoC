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

def find_route_to_com(orbs, sat):
    route = [orbs[sat]]
    while route[0] != "COM":
        route.insert(0, orbs[route[0]])
    return route

checksum = 0
for satellite in orbits.keys():
    checksum += calc_distance_to_com(orbits, satellite)
print("checksum = %d" % checksum)    

route_me = find_route_to_com(orbits, "YOU")
route_santa = find_route_to_com(orbits, "SAN")

while route_me[0] == route_santa[0]:
    route_me = route_me[1:]
    route_santa = route_santa[1:]
    
# Now the tricky piece. We need to count the number of transfers between nodes,
# which is N-1 for N nodes. So the total number of transfers to traverse both
# branches is (len(route_me) -1) + (len(route_santa) -1). Our branches don't
# include their common node, which adds two more transfers, that are required
# to switch between branches, thus the total number of transfers is just
# len(route_me) + len(route_santa)

print("transfers = %d" % (len(route_me) + len(route_santa)))
