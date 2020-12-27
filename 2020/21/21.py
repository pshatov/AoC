INGREDIENT_LISTS = []
ALLERGENS_LISTS = []

INGREDIENTS = {}
ALLERGENS = {}

def load_input():
    with open('input.txt') as f:
        for fl in f:
            fls = fl.strip()
            fls_ingredients, fls_allergens = tuple(fls.split(' (contains '))
            ingredients = fls_ingredients.split(' ')
            if not fls_allergens.endswith(')'): raise RuntimeError
            fls_allergens = fls_allergens[:-1]
            allergens = fls_allergens.split(', ')
            INGREDIENT_LISTS.append(ingredients)
            ALLERGENS_LISTS.append(allergens)


def generate_dicts():
    for il in INGREDIENT_LISTS:
        for i in il:
            if i not in INGREDIENTS: INGREDIENTS[i] = []
    for al in ALLERGENS_LISTS:
        for a in al:
            if a not in ALLERGENS: ALLERGENS[a] = []


def main():
    load_input()
    generate_dicts()

    for n in range(len(INGREDIENT_LISTS)):
        i_list = INGREDIENT_LISTS[n]
        a_list = ALLERGENS_LISTS[n]
        for i in i_list:
            for a in a_list:
                if a not in INGREDIENTS[i]:
                    INGREDIENTS[i].append(a)

    for n in range(len(INGREDIENT_LISTS)):
        i_list = INGREDIENT_LISTS[n]
        a_list = ALLERGENS_LISTS[n]
        for i in INGREDIENTS:
            a_impossible = []
            for ia in INGREDIENTS[i]:
                if i not in i_list and ia in a_list:
                    a_impossible.append(ia)
            for a in a_impossible:
                INGREDIENTS[i].remove(a)

    cnt = 0
    for n in range(len(INGREDIENT_LISTS)):
        i_list = INGREDIENT_LISTS[n]
        for i in i_list:
            if len(INGREDIENTS[i]) == 0: cnt += 1
    print("cnt: %d" % cnt)


if __name__ == '__main__':
    main()
