with open('input.txt') as f:
    input = f.readline()
    
input = input.strip().split('-')
input_min = int(input[0])
input_max = int(input[1])

def pwd_to_digits(pwd):
    digits = []
    pwd_str = str(pwd)
    while len(pwd_str) > 0:
        digits.append(int(pwd_str[0]))
        pwd_str = pwd_str[1:]
    return digits
    
def pwd_is_valid(pwd):
    digits = pwd_to_digits(pwd)
    prev_digit = -1
    has_double = False
    has_decrease = False
    for next_digit in digits:
        if next_digit == prev_digit: has_double = True
        if next_digit < prev_digit: has_decrease = True
        prev_digit = next_digit
    return has_double and not has_decrease

def new_pwd_is_valid(pwd):
    digits = pwd_to_digits(pwd)
    digits.append(-1)
    
    prev_digit = -1
    group_len = 1
    saw_double = False
    print("%d" % pwd)
    for next_digit in digits:
        if next_digit == prev_digit:
            group_len += 1
        else:
            if group_len == 2: saw_double = True
            group_len = 1
        prev_digit = next_digit
        print("    %d: %d" % (next_digit, group_len))
    return saw_double

pwds = []
for i in range(input_min, input_max+1):
    if pwd_is_valid(i): pwds.append(i)
print("count == %d" % len(pwds))

new_pwds = []
for pwd in pwds:
    if new_pwd_is_valid(pwd): new_pwds.append(pwd)
print("new_count == %d" % len(new_pwds))