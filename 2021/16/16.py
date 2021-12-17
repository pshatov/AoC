# ---------------------------------------------------------------------------------------------------------------------
# AoC 2021
# ---------------------------------------------------------------------------------------------------------------------
# 16.py
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
# More Imports
# ---------------------------------------------------------------------------------------------------------------------
from enum import IntEnum
from typing import Tuple, List, Optional


# ---------------------------------------------------------------------------------------------------------------------
class PacketTypeEnum(IntEnum):
    Literal = 4
    Operator = -1
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
class OperatorLengthTypeEnum(IntEnum):
    Length = 0
    Number = 1
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
class OperatorTypeEnum(IntEnum):
    Sum = 0
    Product = 1
    Minimum = 2
    Maximum = 3
    GreaterThan = 5
    LessThan = 6
    EqualTo = 7
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
class PacketClass:

    packet_version: int
    packet_type: Optional[PacketTypeEnum]
    literal_value: Optional[int]
    operator_sub_packets: List['PacketClass']
    operator_type: Optional[OperatorTypeEnum]

    # -----------------------------------------------------------------------------------------------------------------
    def __init__(self, literal_value: int = None):
        self.packet_version = -1
        self.packet_type = None if literal_value is None else PacketTypeEnum.Literal
        self.literal_value = literal_value
        self.operator_sub_packets = list()
        self.operator_type = None
    # -----------------------------------------------------------------------------------------------------------------

    # -----------------------------------------------------------------------------------------------------------------
    def parse(self, packet_bin: str, level: int = 0) -> str:

        level_str = " " * 4 * level

        if len(packet_bin) < 6:
            raise RuntimeError

        self.packet_version, packet_bin = self.chew_bits(packet_bin, 3)
        packet_type_int, packet_bin = self.chew_bits(packet_bin, 3)

        if packet_type_int == PacketTypeEnum.Literal:
            self.packet_type = PacketTypeEnum.Literal
        else:
            self.packet_type = PacketTypeEnum.Operator
            self.operator_type = OperatorTypeEnum(packet_type_int)

        # print("%spacket v%d, type=%d" % (level_str, self.packet_version, packet_type_int))

        if self.packet_type == PacketTypeEnum.Literal:
            self.literal_value, packet_bin = self.parse_literal(packet_bin)
            # print("%s  literal: %d" % (level_str, self.literal_value))
        else:
            packet_bin = self.parse_operator(packet_bin, level)

        return packet_bin
    # -----------------------------------------------------------------------------------------------------------------

    # -----------------------------------------------------------------------------------------------------------------
    def parse_literal(self, packet_bin: str) -> Tuple[int, str]:

        value, flag = 0, 1
        while flag > 0:
            if len(packet_bin) < 5:
                raise RuntimeError
            flag, packet_bin = self.chew_bits(packet_bin, 1)
            data, packet_bin = self.chew_bits(packet_bin, 4)
            value <<= 4
            value += data

        return value, packet_bin
    # -----------------------------------------------------------------------------------------------------------------

    # -----------------------------------------------------------------------------------------------------------------
    def parse_operator(self, packet_bin: str, level: int) -> str:

        if len(packet_bin) < 1:
            raise RuntimeError

        length_type, packet_bin = self.chew_bits(packet_bin, 1)

        if length_type == OperatorLengthTypeEnum.Length:
            if len(packet_bin) < 15:
                raise RuntimeError

            length_sub_packets, packet_bin = self.chew_bits(packet_bin, 15)
            if len(packet_bin) < length_sub_packets:
                raise RuntimeError

            sub_packets_bin, packet_bin = self.chop_bits(packet_bin, length_sub_packets)
            while len(sub_packets_bin) > 0:
                sub_packet = PacketClass()
                sub_packets_bin = sub_packet.parse(sub_packets_bin, level + 1)
                self.operator_sub_packets.append(sub_packet)

        elif length_type == OperatorLengthTypeEnum.Number:
            if len(packet_bin) < 11:
                raise RuntimeError

            number_sub_packets, packet_bin = self.chew_bits(packet_bin, 11)
            while number_sub_packets > 0:
                sub_packet = PacketClass()
                packet_bin = sub_packet.parse(packet_bin, level + 1)
                number_sub_packets -= 1
                self.operator_sub_packets.append(sub_packet)

        return packet_bin
    # -----------------------------------------------------------------------------------------------------------------

    # -----------------------------------------------------------------------------------------------------------------
    @staticmethod
    def chew_bits(packet: str, count: int) -> Tuple[int, str]:
        piece_bin = packet[0: count]
        return int(piece_bin, 2), packet[count:]
    # -----------------------------------------------------------------------------------------------------------------

    # -----------------------------------------------------------------------------------------------------------------
    @staticmethod
    def chop_bits(packet_bin: str, count: int) -> Tuple[str, str]:
        piece_bin = packet_bin[0: count]
        return piece_bin, packet_bin[count:]
    # -----------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
def calc_checksum_recursive(packets: List[PacketClass]) -> int:
    sub_sum = 0
    for p in packets:
        sub_sum += p.packet_version
        if p.packet_type == PacketTypeEnum.Operator:
            sub_sum += calc_checksum_recursive(p.operator_sub_packets)
    return sub_sum
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
def evaluate_all_sub_packets_literal(sub_packet: List[PacketClass]) -> bool:
    for p in sub_packet:
        if p.packet_type != PacketTypeEnum.Literal:
            return False
    return True
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
def evaluate_operator_handler(packet: PacketClass) -> int:

    t: PacketClass

    if packet.operator_type == OperatorTypeEnum.Sum:
        return sum([t.literal_value for t in packet.operator_sub_packets])
    elif packet.operator_type == OperatorTypeEnum.Maximum:
        return max([t.literal_value for t in packet.operator_sub_packets])
    elif packet.operator_type == OperatorTypeEnum.Minimum:
        return min([t.literal_value for t in packet.operator_sub_packets])
    elif packet.operator_type == OperatorTypeEnum.GreaterThan:
        assert len(packet.operator_sub_packets) == 2
        return 1 if packet.operator_sub_packets[0].literal_value > packet.operator_sub_packets[1].literal_value else 0
    elif packet.operator_type == OperatorTypeEnum.LessThan:
        assert len(packet.operator_sub_packets) == 2
        return 1 if packet.operator_sub_packets[0].literal_value < packet.operator_sub_packets[1].literal_value else 0
    elif packet.operator_type == OperatorTypeEnum.EqualTo:
        assert len(packet.operator_sub_packets) == 2
        return 1 if packet.operator_sub_packets[0].literal_value == packet.operator_sub_packets[1].literal_value else 0
    elif packet.operator_type == OperatorTypeEnum.Product:
        p = 1
        for sub_packet in packet.operator_sub_packets:
            p *= sub_packet.literal_value
        return p
    else:
        raise RuntimeError(packet.operator_type)
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
def evaluate_recursive(packets: List[PacketClass]) -> Optional[int]:

    if len(packets) == 1 and packets[0].packet_type == PacketTypeEnum.Literal:
        return packets[0].literal_value

    replace_packets = {}
    for i in range(len(packets)):
        pi = packets[i]
        if pi.packet_type == PacketTypeEnum.Operator:
            if evaluate_all_sub_packets_literal(pi.operator_sub_packets):
                result = evaluate_operator_handler(pi)
            else:
                result = evaluate_recursive(pi.operator_sub_packets)
            if result is not None:
                replace_packets[i] = PacketClass(result)

    for i in replace_packets:
        packets[i] = replace_packets[i]

    return None
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
def main() -> None:

    # read hex from file
    with open('input.txt') as f:
        packets_hex = [int(t, 16) for t in f.readline().strip()]

    # convert hex to binary
    packets_bin = ''.join([format(t, "04b") for t in packets_hex])

    # strip trailing zeroes
    while packets_bin.endswith('0'):
        packets_bin = packets_bin[:-1]

    # parse packets
    packets_list = list()
    while len(packets_bin) > 0:
        new_packet = PacketClass()
        packets_bin = new_packet.parse(packets_bin)
        packets_list.append(new_packet)

    print("part 1: %d" % calc_checksum_recursive(packets_list))

    result = None
    while result is None:
        result = evaluate_recursive(packets_list)

    print("part 2: %d" % result)
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    main()
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
# End of File
# ---------------------------------------------------------------------------------------------------------------------
