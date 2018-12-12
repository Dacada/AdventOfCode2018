import util

DAY = 12

class PotRoom:
    def __init__(self, initial, rules):
        self.state = initial[:]
        self.state_neg = []
        self.rules = rules

    def step(self):
        self.state.extend(('.','.','.','.','.'))
        self.state_neg.extend(('.','.','.','.','.'))
        
        newstate = self.state[:]
        newstate_neg = self.state_neg[:]
        
        for i in range(-(len(self.state_neg)-2),len(self.state)-2):
            neighborhood = []
            for j in range(-2,3):
                ij = i+j
                if ij < 0:
                    neighborhood.append(self.state_neg[-ij-1])
                else:
                    neighborhood.append(self.state[ij])
            n = ''.join(neighborhood)
            #print(i,n)
            if n in self.rules:
                #print("matches rule: " + str(n) + " => " + str(self.rules[n]))
                if i < 0:
                    newstate_neg[-i-1] = self.rules[n]
                else:
                    newstate[i] = self.rules[n]
            else:
                print("matches no rules, empty (should only happen for example input)")
                if i < 0:
                    newstate_neg[-i-1] = '.'
                else:
                    newstate[i] = '.'

        #trim empty pots
        for i in reversed(range(len(newstate))):
            if newstate[i] == '#':
                break
        self.state = newstate[:i+1]

        for i in reversed(range(len(newstate_neg))):
            if newstate_neg[i] == '#':
                break
        self.state_neg = newstate_neg[:i+1]

    def sum_planted_indexs(self):
        return sum(-i-1 for i in range(len(self.state_neg)) if self.state_neg[i] == '#') +\
               sum(i for i in range(len(self.state)) if self.state[i] == '#')

def parse_input(input):
    initial = next(input)
    initial_state = list(initial.split()[2])
    next(input)
    rules = {a:b for a,b in (r.split(' => ') for r in input)}
    return initial_state,rules

@util.timing_wrapper
def star1():
    initial_state,rules = parse_input(util.get_input_lines(DAY))
#    initial_state,rules = parse_input(iter("""initial state: #..#.#..##......###...###
#
#...## => #
#..#.. => #
#.#... => #
#.#.#. => #
#.#.## => #
#.##.. => #
#.#### => #
##.#.# => #
##.### => #
###.#. => #
###.## => #
####.. => #
####.# => #
#####. => #""".split('\n')))
    room = PotRoom(initial_state, rules)
    for generation in range(20):
        #print(' '*(len(room.state_neg)+4)+'0')
        #print(str(generation).rjust(2)+': '+''.join(reversed(room.state_neg))+''.join(room.state))
        #input()
        room.step()
    return room.sum_planted_indexs()

@util.timing_wrapper
def star2():
    """Running it for a few thousands results in a number that increases
    by an exact amount every 1000. gg ez

    """
    initial_state,rules = parse_input(util.get_input_lines(DAY))
    room = PotRoom(initial_state, rules)
    for generation in range(1000):
        room.step()
        thousand = room.sum_planted_indexs()
    for generation in range(1000):
        room.step()
        twothousand = room.sum_planted_indexs()

    # for example inputs:
    # thousand = 1230045
    # twothousand = 2460045
    # etc, keeps increasing by 1230000
    # so:
    # 2*thousand-twothousand = 45
    # twothousand-thousand = 1230000
    # 5 billion//1000 how many thousands in a billion
    # so we just need to multiply 1230000 by how many thousands in a billion
    # and add the 45
    #
    # improvement: calculate only up to the bare minimum instead of the arbitrary 1000
    return 2*thousand-twothousand + (twothousand-thousand)*(50000000000//1000)

if __name__ == '__main__':
    util.pretty_print(star1, star2)
