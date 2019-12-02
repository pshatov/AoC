lines = list()
with open('input.txt') as f:
    for next_line in f:
        lines.append(next_line.strip())

def calc_fuel(mass):
    return mass // 3 - 2

def calc_total_fuel(module):
    total = 0
    fuel = calc_fuel(module)
    while fuel > 0:
        total += fuel
        fuel = calc_fuel(fuel)
    return total

fuel = 0
total_fuel = 0
for line in lines:
    module = int(line)
    fuel += calc_fuel(module)
    total_fuel += calc_total_fuel(module)

print("fuel = %d" % fuel)
print("total_fuel = %d" % total_fuel)
