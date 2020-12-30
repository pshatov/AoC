modulus = 20201227
subject_number = 7


def hack_private_key(pubkey):
    t = 1
    for i in range(100000000):
        t *= subject_number
        t %= modulus
        if t == pubkey:
            return i+1
    raise RuntimeError


def generate_shared_key(subject, loop_size):
    t = 1
    for i in range(loop_size):
        t *= subject
        t %= modulus
    return t


def main():

    with open('input.txt') as f:
        card_pubkey = int(f.readline().strip())
        door_pubkey = int(f.readline().strip())

    # card_pubkey = 5764801
    # door_pubkey = 17807724

    card_loop_size = hack_private_key(card_pubkey)
    door_loop_size = hack_private_key(door_pubkey)

    print("card_loop_size: %d" % card_loop_size)
    print("door_loop_size: %d" % door_loop_size)

    card_shared_key = generate_shared_key(door_pubkey, card_loop_size)
    door_shared_key = generate_shared_key(card_pubkey, door_loop_size)

    print("card_shared_key: %d" % card_shared_key)
    print("door_shared_key: %d" % door_shared_key)




















if __name__ == '__main__':
    main()
