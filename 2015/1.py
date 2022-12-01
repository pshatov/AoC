def main():

    with open('input_1.txt') as f:
        f_line = f.readline().strip()

    cnt_up = f_line.count('(')
    cnt_down = f_line.count(')')

    print("part 1: %d" % (cnt_up - cnt_down))

    floor = 0
    for i in range(len(f_line)):

        if f_line[i] == '(':
            floor += 1
        else:
            floor -= 1

        if floor == -1:
            print("part 2: %d" % (i + 1))
            break


if __name__ == '__main__':
    main()
