import util

DAY = 1

@util.timing_wrapper
def star1():
    total = 0
    for num_str in util.get_input_lines(DAY):
        num = int(num_str)
        total += num
    return total

@util.timing_wrapper
def star2():
    lines = [l for l in util.get_input_lines(DAY)]
    seen_frequencies = set()
    total = 0
    while True:
        for num_str in lines:
            if total in seen_frequencies:
                return total
            else:
                seen_frequencies.add(total)
            num = int(num_str)
            total += num

if __name__ == '__main__':
    util.pretty_print(star1, star2)
