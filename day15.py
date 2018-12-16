import util
from day6 import manhattan

DAY = 15

class Unit:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.hit_points = 200
        self.attack_power = 3
        self.dead = False
        
    def attack(self, other):
        other.hit_points -= self.attack_power
        if other.hit_points <= 0:
            other.dead = True

    def set_position(self, coord):
        self.x = coord[0]
        self.y = coord[1]

    def coords(self):
        return self.x,self.y

    def __repr__(self):
        if self.dead:
            return "!!!DEAD!!!"
        
        if self.is_elf:
            return 'E({0})'.format(self.hit_points)
        else:
            return 'G({0})'.format(self.hit_points)

    def isenemy(self, other):
        return self.is_elf != other.is_elf
    
class Elf(Unit):
    def __init__(self, x, y, power):
        super().__init__(x, y)
        self.attack_power = power
        self.is_elf = True
        self.is_goblin = False

class Goblin(Unit):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.is_elf = False
        self.is_goblin = True

class Game:
    def __init__(self, text, elfpower):
        rows = text.split('\n')
        self.rounds = 0
        self._walls = set()
        self._units = []
        for y,row in enumerate(rows):
            for x,cell in enumerate(row):
                if cell == '#':
                    self._walls.add((x,y))
                elif cell == 'E':
                    self._units.append(Elf(x,y,elfpower))
                elif cell == 'G':
                    self._units.append(Goblin(x,y))
            self.mapx = x+1
        self.mapy = y+1
                
    def turn(self, ragequit):
        for unit in sorted(self._units, key=lambda u: read_order(u.coords())):
            if unit.dead:
                continue
            living_units = set(u for u in self._units if not u.dead)

            # list of coordinate where there's a living enemy adjacent, including coords with walls and living other units in them
            # the pathing algorithm will never reach walls and units so this is fine, no need to filter twice
            goals = set(
                adj
                for u in living_units
                if unit.isenemy(u)
                for adj in adjacent(u.coords())
            )

            # no enemies left, we end the game
            if len(goals) == 0:
                return False

            current = unit.coords()
            if current not in goals: #if we're not already next to an enemy
                next_movement = pathing(list(adjacent(current)),
                                        goals,
                                        self._walls.union(u.coords() for u in living_units))
                # None is returned if no goals are reachable
                if next_movement is not None:
                    unit.set_position(next_movement)

            target = None
            minhp = 999
            for u in living_units:
                if unit.isenemy(u) and (manhattan(unit.coords(), u.coords()) == 1):
                    if u.hit_points < minhp:
                        minhp = u.hit_points
                        target = u
                    elif u.hit_points == minhp:
                        if read_order(u.coords()) < read_order(target.coords()):
                            target = u
            # target is now the first in read order enemy unit that's adjacent to our current position, or None
            if target is not None:
                unit.attack(target)
                if target.dead and target.is_elf and ragequit:
                    return False

        return True
    
    def play(self, ragequit=False):
        #print(self)
        #input()
        while self.turn(ragequit):
            self.rounds += 1
            #print(self)
            #input()

    def get_outcome(self):
        return self.rounds * sum((u.hit_points for u in self._units if not u.dead))

    def are_any_goblins_alive(self):
        for unit in self._units:
            if unit.is_goblin and not unit.dead:
                return True
        return False

    def __str__(self):
        s = ""
        l = [['.' for __ in range(self.mapx)] for ___ in range(self.mapy)]
        d = {}
        
        for wall in self._walls:
            x,y = wall
            l[y][x] = '#'
            
        for unit in self._units:
            if unit.dead:
                continue
            x,y = unit.coords()
            
            if unit.is_elf:
                l[y][x] = 'E'
            else:
                l[y][x] = 'G'
                
            if y in d:
                d[y].append(unit)
            else:
                d[y] = [unit]

        for y,row in enumerate(l):
            s += ' '.join(row)
            if y in d:
                s += ' '
                s += ','.join((repr(x) for x in sorted(d[y], key=lambda u:u.x)))
            s += '\n'

        return s

def read_order(coord):
    return coord[1]*1000 + coord[0]

def adjacent(coord):
    return [
        (coord[0]+1, coord[1]),
        (coord[0]-1, coord[1]),
        (coord[0], coord[1]+1),
        (coord[0], coord[1]-1)
    ]

def pathing(starts, goals, obstacles):
    min_pathlen = 9999999
    chosen_start = None
    chosen_goal = None

    filtered_goals = [g for g in goals if g not in obstacles]
    filtered_starts = [s for s in starts if s not in obstacles]

    for goal in filtered_goals:
        for start in filtered_starts:
            pathlen = min_path_length(start, goal, obstacles, min_pathlen)
            #print("pathlen( {0} , {1} ) = {2} (min {3})".format(start, goal, pathlen, min_pathlen))
            if pathlen is not None:
                if pathlen < min_pathlen: # minimal length
                    min_pathlen = pathlen
                    chosen_start = start
                    chosen_goal = goal
                elif pathlen == min_pathlen: # if length is equal
                    order_goal = read_order(goal)
                    order_chosen_goal = read_order(chosen_goal)
                    if order_goal < order_chosen_goal: # minimal read order for goal
                        chosen_start = start
                        chosen_goal = goal
                    elif order_goal == order_chosen_goal: # if read order for goal is equal
                        if read_order(start) < read_order(chosen_start): # minimal read order for start
                            chosen_start = start
                            chosen_goal = goal

    #print()
    return chosen_start

def min_path_length(start, goal, obstacles, limit):
    """
    Length of the path between start and goal, without going through obstacles
    Give up and return None if we'd go over limit
    """
    if start == goal:
        return 0

    seen = set()
    breadth = set([start])
    newbreadth = set()
    distance = 0

    while breadth and goal not in breadth:
        for node in breadth:
            seen.add(node)
            for adj in adjacent(node):
                if adj not in seen and adj not in obstacles:
                    newbreadth.add(adj)
        distance += 1
        if distance > limit:
            return distance
        breadth = newbreadth
        newbreadth = set()

    if breadth:
        return distance
    else:
        return None

@util.timing_wrapper
def star1():
    text = util.get_input_text(DAY)
    #text = """
#######
#.G...#
#...EG#
#.#.#G#
#..G#E#
#.....#
#######
#""".strip()
    game = Game(text, 3)
    game.play()
    return game.get_outcome()

@util.timing_wrapper
def star2():
    text = util.get_input_text(DAY)
    power = 4
    # Possible optimization: Advance game until first elf and goblin meet, then start each iteration from there
    while True:
        game = Game(text, power)
        game.play(True)
        if not game.are_any_goblins_alive():
            return game.get_outcome()
        else:
            power += 1

if __name__ == '__main__':
    util.pretty_print(star1, star2)
