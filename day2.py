import util

DAY = 2

def close_enough(id1, id2):
    first_different_pair_found = False
    
    for i in range(len(id1)):
        if id1[i] != id2[i]:
            if not first_different_pair_found:
                first_different_pair_found = True
            else:
                return False
            
    # Only return true if they are off by one, false if they're equal
    return first_different_pair_found

@util.timing_wrapper
def star1():
    has2 = 0
    has3 = 0
    for id in util.get_input_lines(DAY):
        letters = [0]*26
        for c in id:
            i = ord(c) - ord('a')
            letters[i] += 1
        if letters.count(2) >= 1:
            has2 += 1
        if letters.count(3) >= 1:
            has3 += 1
    return has2 * has3

@util.timing_wrapper
def star2():
    lines = [l for l in util.get_input_lines(DAY)]
    lines.sort() # I get the feeling it'll be faster if I sort it first...?
    for id1 in lines:
        for id2 in lines:
            if close_enough(id1, id2):
                return ''.join([id1[i] for i in range(len(id1)) if id1[i] == id2[i]])

if __name__ == '__main__':
    util.pretty_print(star1, star2)
