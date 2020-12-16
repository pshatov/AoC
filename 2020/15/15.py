import sys

NUMBERS = [2, 1, 10, 11, 0, 6]

num_numbers = len(NUMBERS)
while num_numbers < 2020:
    last_number = NUMBERS[-1]
    next_number = 0
    for i in range(num_numbers-2, -1, -1):
        if NUMBERS[i] == last_number:
            next_number = num_numbers - (i+1)
            break
    NUMBERS.append(next_number)
    num_numbers += 1

print(NUMBERS[-1])

NUMBERS = [2, 1, 10, 11, 0, 6]

NUM_LIST = []
for i in range(12):
    NUM_LIST.append(-1)

for i in range(len(NUMBERS)-1):
    NUM_LIST[NUMBERS[i]] = i

current_number = NUMBERS[-1]
next_number = 0
num_steps = 5

while num_steps < 30000000-1:
    NUM_LIST[current_number] = num_steps
    if next_number < len(NUM_LIST):
        if NUM_LIST[next_number] < 0:
            next_number_next = 0
        else:
            next_number_next = num_steps - NUM_LIST[next_number] + 1
    else:
        next_number_next = 0
        for i in range(len(NUM_LIST), next_number+1):
            NUM_LIST.append(-1)

    current_number = next_number
    next_number = next_number_next
    num_steps += 1

print(current_number)
