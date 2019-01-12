import re


def file_to_input_list(file_name):
    with open(file_name) as file:
        for line in file:
            yield line.strip()


def parse_input(source):
    guard_pattern = re.compile(r'^\[\d{4}-\d{2}-\d{2} \d{2}:\d{2}\] Guard \#(\d+) begins shift')
    sleep_report_pattern = re.compile(r'^\[\d{4}-\d{2}-\d{2} \d{2}:(\d{2})\] (.+)')

    actual_guard_id = None
    for line in source:
        match = guard_pattern.match(line)
        if match:
            actual_guard_id = int(match[1])
        else:
            match = sleep_report_pattern.match(line)
            yield actual_guard_id, match[2] == 'wakes up', int(match[1])


def build_guard_table(activities_logs):
    guards_table = {}
    fall_asleep_on = None

    for guard_id, isWakeUp, minute in activities_logs:
        if not guard_id in guards_table:
            guards_table[guard_id] = [0] * 60

        if isWakeUp:
            for i in range(minute - fall_asleep_on):
                guards_table[guard_id][i + fall_asleep_on] += 1
        else:
            fall_asleep_on = minute

    return guards_table


def find_the_most_sleepy_guard(guard_table: {}):
    g_id, _ = max(
        [(g_id, sum(g_sleep)) for g_id, g_sleep in guard_table.items()],
        key = lambda t: t[1]
    )

    return g_id


def find_the_most_sleepy_minute_for_guard(guard_table: {}, guard_id: int):
    activities_table = guard_table[guard_id]

    return activities_table.index(max(activities_table))


def find_the_frequently_sleepy_guard(guard_table: {}):
    g_id, _ = max(
        [(g_id, max(g_sleep)) for g_id, g_sleep in guard_table.items()],
        key = lambda t: t[1]
    )

    return g_id


test_input = ['[1518-11-01 00:00] Guard #10 begins shift',
'[1518-11-01 00:05] falls asleep',
'[1518-11-01 00:25] wakes up',
'[1518-11-01 00:30] falls asleep',
'[1518-11-01 00:55] wakes up',
'[1518-11-01 23:58] Guard #99 begins shift',
'[1518-11-02 00:40] falls asleep',
'[1518-11-02 00:50] wakes up',
'[1518-11-03 00:05] Guard #10 begins shift',
'[1518-11-03 00:24] falls asleep',
'[1518-11-03 00:29] wakes up',
'[1518-11-04 00:02] Guard #99 begins shift',
'[1518-11-04 00:36] falls asleep',
'[1518-11-04 00:46] wakes up',
'[1518-11-05 00:03] Guard #99 begins shift',
'[1518-11-05 00:45] falls asleep',
'[1518-11-05 00:55] wakes up']


test_result_guard_table = build_guard_table(parse_input(test_input))
test_result_first_strategy_guard_id = find_the_most_sleepy_guard(test_result_guard_table)
test_result_second_strategy_guard_id = find_the_frequently_sleepy_guard(test_result_guard_table)

assert test_result_first_strategy_guard_id == 10
assert test_result_second_strategy_guard_id == 99
assert find_the_most_sleepy_minute_for_guard(test_result_guard_table, test_result_first_strategy_guard_id) == 24
assert find_the_most_sleepy_minute_for_guard(test_result_guard_table, test_result_second_strategy_guard_id) == 45

# The input.04.txt file contain *sorted* input from https://adventofcode.com/2018/day/4/input
guard_table = build_guard_table(parse_input(file_to_input_list('input.04.txt')))

first_strategy_guard_id = find_the_most_sleepy_guard(guard_table)
first_strategy_minute = find_the_most_sleepy_minute_for_guard(guard_table, first_strategy_guard_id)

second_strategy_guard_id = find_the_frequently_sleepy_guard(guard_table)
second_strategy_minute = find_the_most_sleepy_minute_for_guard(guard_table, second_strategy_guard_id)

print("Solution for first part:", first_strategy_guard_id * first_strategy_minute)
print("Solution for second part:", second_strategy_guard_id * second_strategy_minute)
