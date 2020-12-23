import re
from enum import Enum, auto


re_rule_type0 = re.compile('(\d+)\: \"(a|b)\"')
re_rule_type11 = re.compile('(\d+)\: (\d+)')
re_rule_type12 = re.compile('(\d+)\: (\d+) (\d+)')
re_rule_type21 = re.compile('(\d+)\: (\d+) \| (\d+)')
re_rule_type22 = re.compile('(\d+)\: (\d+) (\d+) \| (\d+) (\d+)')


MSGS = []
RULES = {}


class RuleOperand(Enum):
    Key = auto()
    Literal = auto()


class RuleType(Enum):
    Simple = auto()
    Comma = auto()
    Pipe = auto()


def load_input_partial(f, l):
    for fl in f:
        fls = fl.strip()
        if len(fls) == 0:
            return
        l.append(fls)


class Rule:

    def __init__(self, rule_type, rule_data):

        self._type = rule_type

        if rule_type == RuleType.Simple:
            self._data_simple = rule_data
            self._operand_simple = RuleOperand.Literal if isinstance(rule_data, str) else RuleOperand.Key

        else:
            self._data = rule_data
            self._operand = [RuleOperand.Key, RuleOperand.Key]

    @property
    def data_simple(self): return self._data_simple

    @property
    def type(self): return self._type

    @property
    def operand_a(self): return self._operand[0]

    @property
    def operand_b(self): return self._operand[1]

    @property
    def data_a(self): return self._data[0]

    @property
    def data_b(self): return self._data[1]

    def _dump_data_simple(self):
        return self._data_simple if self._operand_simple == RuleOperand.Literal else "%d" % self._data_simple

    def _dump_data(self, i):
        return self._data[i] if self._operand[i] == RuleOperand.Literal else "%d" % self._data[i]

    def dump(self, k):
        if self._type == RuleType.Simple:
            print("%d: %s" % (k, self._dump_data_simple()))
        elif self._type == RuleType.Comma:
            print("%d: %s, %s" % (k, self._dump_data(0), self._dump_data(1)))
        elif self._type == RuleType.Pipe:
            print("%d: %s | %s" % (k, self._dump_data(0), self._dump_data(1)))
        else:
            raise RuntimeError

    def try_substitute_operand(self, k, k_value):

        if self._type == RuleType.Simple: raise RuntimeError

        k_operand = RuleOperand.Literal if isinstance(k_value, str) else RuleOperand.Key

        t = 0
        for i in range(2):
            if self._operand[i] == RuleOperand.Key and self._data[i] == k:
                self._operand[i] = k_operand
                self._data[i] = k_value
                t += 1

        return t > 0

    def try_combine_comma(self):

        if self._type == RuleType.Comma:
            if self._operand[0] == RuleOperand.Literal and self._operand[1] == RuleOperand.Literal:
                self._data_simple = self._data[0] + self._data[1]
                self._operand_simple = RuleOperand.Literal
                del self._data
                del self._operand
                self._type = RuleType.Simple
                return True

        return False


# def find_rules_type0():
#
#     for k in RULES.keys():
#         rk = RULES[k]
#         if rk.type == 0:
#             RULES_TYPE0[k] = rk._data
#
#     for k in RULES_TYPE0.keys():
#         del RULES[k]
#
#
# def find_rules_type11():
#
#     RULES_TYPE11.clear()
#
#     for k in RULES.keys():
#         rk = RULES[k]
#         if rk.type == 11:
#             RULES_TYPE11[k] = rk._data
#
#     for k in RULES_TYPE11.keys():
#         del RULES[k]
#
#     for k in RULES.keys():
#         rk = RULES[k]
#         if rk.type == 12:
#             if rk._data[0] in RULES_TYPE11.keys(): rk._data[0] = RULES_TYPE11[rk._data[0]]
#             if rk._data[1] in RULES_TYPE11.keys(): rk._data[1] = RULES_TYPE11[rk._data[1]]
#         elif rk.type == 21:
#             if rk._data[0] in RULES_TYPE11.keys(): rk._data[0] = RULES_TYPE11[rk._data[0]]
#             if rk._data[1] in RULES_TYPE11.keys(): rk._data[1] = RULES_TYPE11[rk._data[1]]
#         elif rk.type == 22:
#             if rk._data[0][0] in RULES_TYPE11.keys(): rk._data[0][0] = RULES_TYPE11[rk._data[0][0]]
#             if rk._data[0][1] in RULES_TYPE11.keys(): rk._data[0][1] = RULES_TYPE11[rk._data[0][1]]
#             if rk._data[1][0] in RULES_TYPE11.keys(): rk._data[1][0] = RULES_TYPE11[rk._data[1][0]]
#             if rk._data[1][1] in RULES_TYPE11.keys(): rk._data[1][1] = RULES_TYPE11[rk._data[1][1]]
#         else:
#             raise RuntimeError


def patch_simple_rules():

    # find all simple rules
    simple_rules = {}
    for k in RULES.keys():
        rk = RULES[k]
        if rk.type == RuleType.Simple:
            simple_rules[k] = rk

    # remove simple rules from global list
    for k in simple_rules.keys():
        del RULES[k]

    # try to substitute as much as possible
    n = 0
    for k in simple_rules.keys():
        for r in RULES.values():
            ok = r.try_substitute_operand(k, simple_rules[k].data_simple)
            if ok: n += 1

    return n


def combine_comma_rules():

    # try to combine as much as possible
    n = 0
    for r in RULES.values():
        ok = r.try_combine_comma()
        if ok: n += 1

    return n


def dump_rules():
    for k in RULES.keys():
        RULES[k].dump(k)


# def patch_rules_type12():
#
#     n = 0
#     for k in RULES.keys():
#         rk = RULES[k]
#         if rk.type == 12:
#             for z in range(2):
#                 if rk._data[z] in RULES_TYPE0.keys():
#                     rk._data[z] = RULES_TYPE0[rk._data[z]]
#                     n += 1
#             if isinstance(rk._data[0], str) and isinstance(rk._data[1], str):
#                 rk._type = 11
#                 rk._data = rk._data[0] + rk._data[1]
#     return n
#
#
# def patch_rules_type21():
#
#     n = 0
#     for k in RULES.keys():
#         rk = RULES[k]
#         if rk.type == 21:
#             for z in range(2):
#                 if rk._data[z] in RULES_TYPE0.keys():
#                     rk._data[z] = RULES_TYPE0[rk._data[z]]
#                     n += 1
#     return n
#
#
# def patch_rules_type22():
#
#     n = 0
#     for k in RULES.keys():
#         rk = RULES[k]
#         if rk.type == 22:
#             for zz in range(2):
#                 for z in range(2):
#                     if rk._data[zz][z] in RULES_TYPE0.keys():
#                         rk._data[zz][z] = RULES_TYPE0[rk._data[zz][z]]
#                         n += 1
#                 if isinstance(rk._data[zz][0], str) and isinstance(rk._data[zz][1], str):
#                     rk._type = 11
#                     rk._data[zz] = rk._data[zz][0] + rk._data[zz][1]
#     return n


def parse_rules(rules):

    num_total = 0

    for r in rules:
        m = re_rule_type0.fullmatch(r)
        if m is not None:
            num_total += 1
            k = int(m.group(1))
            a = m.group(2)
            RULES[k] = Rule(RuleType.Simple, a)

        m = re_rule_type11.fullmatch(r)
        if m is not None:
            num_total += 1
            k = int(m.group(1))
            a = int(m.group(2))
            RULES[k] = Rule(RuleType.Simple, a)

        m = re_rule_type12.fullmatch(r)
        if m is not None:
            num_total += 1
            k = int(m.group(1))
            a, b = [int(m.group(2)), int(m.group(3))]
            RULES[k] = Rule(RuleType.Comma, [a, b])

        m = re_rule_type21.fullmatch(r)
        if m is not None:
            num_total += 1
            k = int(m.group(1))
            a, b = int(m.group(2)), int(m.group(3))
            RULES[k] = Rule(RuleType.Pipe, [a, b])

        m = re_rule_type22.fullmatch(r)
        if m is not None:
            num_total += 1
            k = int(m.group(1))
            a, b, c, d = int(m.group(2)), int(m.group(3)), int(m.group(4)), int(m.group(5))
            k1 = -1000 * k - 1
            k2 = -1000 * k - 2
            RULES[k1] = Rule(RuleType.Comma, [a, b])
            RULES[k2] = Rule(RuleType.Comma, [c, d])
            RULES[k] = Rule(RuleType.Pipe, [k1, k2])

    if num_total != len(rules):
        raise RuntimeError


def print_depth(m, d):
    pass
    #print("%s%s" % (4*" "*d, m))


def check_match_recursive(msg, rule_index, depth=0):

    rule = RULES[rule_index]

    #print_depth("msg: %s [%d]" % (msg, rule_index), depth)

    if rule.type == RuleType.Comma:

        if len(msg) < 2: return False

        operand_a, operand_b = rule.operand_a, rule.operand_b
        data_a, data_b = rule.data_a, rule.data_b

        if operand_a == RuleOperand.Literal and operand_b == RuleOperand.Literal:
            raise RuntimeError

        if operand_a == RuleOperand.Literal and operand_b != RuleOperand.Literal:
            if not msg.startswith(data_a): return False
            msg_b = msg[len(data_a):]
            return check_match_recursive(msg_b, data_b, depth+1)

        if operand_a != RuleOperand.Literal and operand_b == RuleOperand.Literal:
            if not msg.endswith(data_b): return False
            msg_a = msg[:-len(data_b):]
            return check_match_recursive(msg_a, data_a, depth+1)

        if operand_a != RuleOperand.Literal and operand_b != RuleOperand.Literal:
            for m in range(0, len(msg)-1):
                msg_a = msg[:m+1]
                msg_b = msg[m+1:]
                ok_a = check_match_recursive(msg_a, data_a, depth+1)
                if not ok_a: continue
                ok_b = check_match_recursive(msg_b, data_b, depth+1)
                if ok_b: return True
            return False

    if rule.type == RuleType.Pipe:

        operand_a, operand_b = rule.operand_a, rule.operand_b
        data_a, data_b = rule.data_a, rule.data_b

        if operand_a == RuleOperand.Literal and operand_b == RuleOperand.Literal:
            if msg == data_a: return True
            if msg == data_b: return True
            return False

        if operand_a == RuleOperand.Literal and operand_b != RuleOperand.Literal:
            if msg == data_a: return True
            return check_match_recursive(msg, data_b, depth + 1)

        if operand_a != RuleOperand.Literal and operand_b == RuleOperand.Literal:
            if msg == data_b: return True
            return check_match_recursive(msg, data_a, depth + 1)

        if operand_a != RuleOperand.Literal and operand_b != RuleOperand.Literal:
            ok_a = check_match_recursive(msg, data_a, depth + 1)
            if ok_a: return True
            ok_b = check_match_recursive(msg, data_b, depth + 1)
            return ok_b

    raise RuntimeError
#
#     elif rule_type == 12:
#         sub_rule_x = rule_dict[0]
#         sub_rule_y = rule_dict[1]
#         print_depth("%d -> %d, %d" % (rule_index, sub_rule_x, sub_rule_y), depth)
#         if len(msg) < 2:
#             print_depth("too short", depth)
#             return False
#         if sub_rule_x == RULE_A and not msg.startswith('a'): return False
#         if sub_rule_x == RULE_B and not msg.startswith('b'): return False
#         if sub_rule_y == RULE_A and not msg.endswith('a'): return False
#         if sub_rule_y == RULE_B and not msg.endswith('b'): return False
#
#         for i in range(0, len(msg)-1):
#             sub_msg_x = msg[:i+1]
#             sub_msg_y = msg[i+1:]
#             print_depth("[%s][%s]" % (sub_msg_x, sub_msg_y), depth)
#             ok_x = check_match_recursive(sub_msg_x, sub_rule_y, depth+1)
#             print_depth("X - match" if ok_x else "X - no match", depth)
#             if ok_x:
#                 ok_y = check_match_recursive(sub_msg_y, sub_rule_y, depth+1)
#                 print_depth("Y - match" if ok_y else "Y - no match", depth)
#             else: ok_y = False
#             ok = ok_x and ok_y
#             print_depth("OK" if ok else "no match X & Y", depth)
#             if ok: return True
#         return False
#
#     elif rule_type == 22:
#         sub_rule1_x = rule_dict[0][0]
#         sub_rule1_y = rule_dict[0][1]
#         sub_rule2_x = rule_dict[1][0]
#         sub_rule2_y = rule_dict[1][1]
#         print_depth("%d -> %d, %d or %d, %d" % (rule_index, sub_rule1_x, sub_rule1_y, sub_rule2_x, sub_rule2_y), depth)
#         if len(msg) < 2:
#             print_depth("too short", depth)
#             return False
#
#         need_check1 = True
#         need_check2 = True
#         if sub_rule1_x == RULE_A and not msg.startswith('a'): need_check1 = False
#         if sub_rule1_x == RULE_B and not msg.startswith('b'): need_check1 = False
#         if sub_rule1_y == RULE_A and not msg.endswith('a'): need_check1 = False
#         if sub_rule1_y == RULE_B and not msg.endswith('b'): need_check1 = False
#         if sub_rule2_x == RULE_A and not msg.startswith('a'): need_check2 = False
#         if sub_rule2_x == RULE_B and not msg.startswith('b'): need_check2 = False
#         if sub_rule2_y == RULE_A and not msg.endswith('a'): need_check2 = False
#         if sub_rule2_y == RULE_B and not msg.endswith('b'): need_check2 = False
#
#         for i in range(0, len(msg)-1):
#             sub_msg_a = msg[:i+1]
#             sub_msg_b = msg[i+1:]
    #         print_depth("[%s][%s]" % (sub_msg_a, sub_msg_b), depth)
    #         ok1_a = check_match_recursive(sub_msg_a, sub_rule1_a, depth+1)
    #         print_depth("A1 - match" if ok1_a else "A1 - no match", depth)
    #         if ok1_a:
    #             ok1_b = check_match_recursive(sub_msg_b, sub_rule1_b, depth+1)
    #             print_depth("B1 - match" if ok1_b else "B1 - no match", depth)
    #         else: ok1_b = False
    #         ok = ok1_a and ok1_b
    #         print_depth("OK" if ok else "X - no match A1 & B1", depth)
    #         if ok: return True
    #         #
    #         ok2_a = check_match_recursive(sub_msg_a, sub_rule2_a, depth+1)
    #         print_depth("A2 - match" if ok2_a else "A2 - no match", depth)
    #         if ok2_a:
    #             ok2_b = check_match_recursive(sub_msg_b, sub_rule2_b, depth+1)
    #             print_depth("B2 - match" if ok2_b else "B2 - no match", depth)
    #         else: ok2_b = False
    #         ok = ok2_a and ok2_b
    #         print_depth("OK" if ok else "X - no match A2 & B2", depth)
    #         if ok: return True
    #     return False


    # elif rule_type == 21:
    #     sub_rule1 = rule_dict[0]
    #     sub_rule2 = rule_dict[1]
    #     print_depth("%d -> %d or %d" % (rule_index, sub_rule1, sub_rule2), depth)
    #     print_depth("[%s]" % msg, depth)
    #     ok1 = check_match_recursive(msg, sub_rule1, depth+1)
    #     print_depth("1 - match" if ok1 else "1 - no match", depth)
    #     if not ok1:
    #         ok2 = check_match_recursive(msg, sub_rule2, depth+1)
    #         print_depth("2 - match" if ok2 else "2 - no match", depth)
    #     else: ok2 = True
    #     ok = ok1 or ok2
    #     print_depth("OK" if ok else "X - no match A | B", depth)
    #     return ok


    # elif rule_type == 0:
    #     print_depth("%d -> '%s'" % (rule_index, rule_dict), depth)
    #     print_depth("[%s]" % msg, depth)
    #     ok = msg == rule_dict
    #     print_depth("OK" if ok else "X - no match", depth)
    #     return ok

    #else:
        #raise RuntimeError


def main():

    t = []
    with open('input.txt') as f:
        load_input_partial(f, t)
        load_input_partial(f, MSGS)

    parse_rules(t)
    # dump_rules()

    go = True
    while go:
        print('.')
        n1 = patch_simple_rules()
        n2 = combine_comma_rules()
        go = n1 > 0 and n2 > 0

    dump_rules()

    num = 0
    for i in range(len(MSGS)):
        print("%03d of %3d" % (i+1, len(MSGS)))
        mi = MSGS[i]
        if check_match_recursive(mi, 0):
            num += 1
            print("  Yes (%d)" % num)
        else:
            print("  No")

    print("")
    print("num: %d" % num)


if __name__ == '__main__':
    main()
