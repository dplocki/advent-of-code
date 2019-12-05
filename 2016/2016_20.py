def load_input_file(file_name):
    with open(file_name) as file:
        for line in file:
            yield tuple(map(int, line.strip().split('-')))


def solution_for_first_part(input_list: (int, int)) -> int:

    def get_blocking_rule_for(ip, blocked_ips_list):
        for ip_range in blocked_ips_list:
            if ip >= ip_range[0] and ip <= ip_range[1]:
                return ip_range

        return None

    blocked_ips_list = list(input_list)
    ip = 0

    while True:
        rule = get_blocking_rule_for(ip, blocked_ips_list)
        if rule == None:
            return ip

        ip = rule[1] + 1

# The input is taken from: https://adventofcode.com/2016/day/20/input
input_list = load_input_file('input.20.txt')
print("Solution for the first part:", solution_for_first_part(input_list))
