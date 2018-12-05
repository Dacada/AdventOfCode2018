import util
import string

DAY = 5

def must_remove(a, b):
    return abs(ord(a)-ord(b)) == 32

def go_back(text, i):
    while text[i] == '_':
        i -= 1
    return i

def reactionLength(polimer):
    """Instead of just iterating over and over, hang around the same area
    after replacing a pair. Later I found that using a stack might be
    better.

    """
    text = list(polimer)
    iprev = 0
    icurr = 1
    
    while icurr < len(text):
        cprev = text[iprev]
        ccurr = text[icurr]
        if must_remove(cprev, ccurr):
            text[iprev] = '_'
            text[icurr] = '_'
            if iprev == 0:
                iprev = icurr + 1
                icurr += 2
            else:
                iprev = go_back(text, iprev-1)
                icurr += 1
        else:
            iprev = icurr
            icurr += 1
            
    return len(text) - text.count('_')

@util.timing_wrapper
def star1():
    return reactionLength(util.get_input_text(DAY))

@util.timing_wrapper
def star2():
    polimer = util.get_input_text(DAY)
    bestLength = 99999
    for letter in string.ascii_lowercase:
        length = reactionLength(c for c in polimer if c != letter and c != letter.upper())
        if length < bestLength:
            bestLength = length
    return bestLength

if __name__ == '__main__':
    util.pretty_print(star1, star2)
