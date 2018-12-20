import util

DAY = 20

def invert(direction):
    if direction == 'N':
        return 'S'
    elif direction == 'E':
        return 'W'
    elif direction == 'W':
        return 'E'
    elif direction == 'S':
        return 'N'

def Room:
    def __init__(self):
        self.neighbors = {}

    def add_neighbor(self, direction):
        if direction in self.neighbors:
            return self.neighbors[direction]
        else:
            other = Room()
            self.neighbors[direction] = other
            other.neighbors[invert(direction)] = self
            return other

@util.timing_wrapper
def star1():
    origin = Room()

    stack = []
    room = root
    for c in util.get_input_text(DAY)[1:-1]:
        if c in 'NEWS':
            room = room.add_neighbor(c)
        elif c == '(':
            stack.append((room,[]))
        elif c == '|':
            stack[-1][1].append(room)
            room = stack[-1][0]
        elif c == ')':
            stack[-1][1].append(room)
            # now we have to treat all the rooms in stack[-1][1] as the "room"
            # this calls for recursivity... ugh...

@util.timing_wrapper
def star2():
    pass

if __name__ == '__main__':
    util.pretty_print(star1, star2)
