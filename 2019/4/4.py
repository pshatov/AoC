with open('input.txt') as f:
    input = f.readline()
    
input = input.strip().split('-')
input_min = int(input[0])
input_max = int(input[1])

def pwd_is_valid(pwd):
    digits = []
    pwd_str = str(pwd)
    while len(pwd_str) > 0:
        digits.append(int(pwd_str[0]))
        pwd_str = pwd_str[1:]
    prev_digit = -1
    has_double = False
    has_decrease = False
    for next_digit in digits:
        if next_digit == prev_digit: has_double = True
        if next_digit < prev_digit: has_decrease = True
        prev_digit = next_digit
    return has_double and not has_decrease

count = 0
for i in range(input_min, input_max+1):
    if pwd_is_valid(i): count += 1
    
print("count == %d" % count)
