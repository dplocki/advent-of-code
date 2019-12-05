MINIMUM_IP = 0
MAXIMUM_IP = 4294967295


def load_input_file(file_name):
    with open(file_name) as file:
        for line in file:
            yield tuple(map(int, line.strip().split('-')))


def find_first_allow_ip(blocked_ips_list: [int], from_ip: int) -> int:

    def get_blocking_rule_for(ip, blocked_ips_sublist):
        for ip_range in blocked_ips_sublist:
            if ip >= ip_range[0] and ip <= ip_range[1]:
                return ip_range

        return None

    rules = blocked_ips_list
    ip = from_ip
    while ip <= MAXIMUM_IP:
        rule = get_blocking_rule_for(ip, rules)
        if rule == None:
            return ip

        ip = rule[1] + 1
        rules = list(filter(lambda x: ip <= x[1], rules))

    return None


def solution_for_first_part(blocked_ips_list: (int, int)) -> int:
    return find_first_allow_ip(blocked_ips_list[:], MINIMUM_IP)


# The input is taken from: https://adventofcode.com/2016/day/20/input
blocked_ips_list = list(load_input_file('input.20.txt'))
print("Solution for the first part:", solution_for_first_part(blocked_ips_list))


def solution_for_second_part(blocked_ips_list: (int, int)) -> int:
    result = 0
    ip = find_first_allow_ip(blocked_ips_list, MINIMUM_IP)
    rules = blocked_ips_list

    while ip != None:
        rules = sorted(filter(lambda x: ip < x[1], rules), key=lambda x: x[0])
        first_matching_rule = rules[0]
        result += first_matching_rule[0] - ip
        ip = find_first_allow_ip(rules, first_matching_rule[1] + 1)

    return result


print("Solution for the second part:", solution_for_second_part(blocked_ips_list))
