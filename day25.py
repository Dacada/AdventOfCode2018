import util
from day23 import manhattan

import collections

DAY = 25

Point4D = collections.namedtuple('Point4D', ['x','y','z','t'])
Star = collections.namedtuple('Star', ['center','radius'])
AABB = collections.namedtuple('AABB', ['max','min'])

def intersects_sphere_aabb(sphere, aabb):
    coord = (max(c1, min(c2,c3)) for (c1,(c2,c3)) in zip(aabb.min, zip(sphere.center, aabb.max)))
    distance = manhattan(coord, sphere.coords)
    return distance <= sphere.radius

def intersects_sphere_sphere(sphere1, sphere2):
    distance = manhattan(sphere1.center, sphere2.center)
    return distance <= sphere1.radius or distance <= sphere2.radius

def intersects_aabb_aabb(aabb1, aabb2):
    return all(c1 > c2 for c1,c2 in zip(aabb1.max, aabb2.min)) and\
           all(c1 > c2 for c1,c2 in zip(aabb2.max, aabb1.min))

class Constellation:
    def __init__(self, star):
        self.stars = set((star,))
        self.regen_aabb()

    def regen_aabb():
        maxx = max(x for x,y,z,t in self.stars)
        maxy = max(y for x,y,z,t in self.stars)
        maxz = max(z for x,y,z,t in self.stars)
        maxt = max(t for x,y,z,t in self.stars)
        
        minx = min(x for x,y,z,t in self.stars)
        miny = min(y for x,y,z,t in self.stars)
        minz = min(z for x,y,z,t in self.stars)
        mint = min(t for x,y,z,t in self.stars)

        self.aabb = AABB(Point4D(maxx,maxy,maxz,maxt),Point4D(minx,miny,minz,mint))

    def add_star(self, star):
        if not intersects_sphere_aabb(star, self.aabb):
            return False
        
        for s in self.stars:
            if intersects_sphere_sphere(star, s):
                self.stars.add(star)
                self.regen_aabb()
                return True
            
        return False

    def add_constellation(self, other):
        
        
        if any(manhattan(s1,s2) <= 3 for s1 in self.stars for s2 in other.stars):
            self.stars = self.stars.union(other.stars)
            return True
        
        return False

class StarrySky:
    def __init__(self):
        self.constellations = []

    def add_star(self, star: Point4D):
        done = False
        for constellation in self.constellations:
            if constellation.add_star(star):
                done = True
                break
            
        if not done:
            self.constellations.append(Constellation(star))

        self.unify()

    def unify(self):
        current = 0
        while current < len(self.constellations):
            main = self.constellations[current]
            consts_to_remove = [None]
            while consts_to_remove:
                consts_to_remove = []
                for i,const in enumerate(self.constellations):
                    if i != current:
                        if main.add_constellation(const):
                            consts_to_remove.append(i)
                for i in sorted(consts_to_remove, reverse=True):
                    del self.constellations[i]
            current += 1

def parse(lines):
    for line in lines:
        x,y,z,t = line.split(',')
        yield Point4D(int(x),int(y),int(z),int(t))

@util.timing_wrapper
def star1():
    lines = util.get_input_lines(DAY)
#     lines = """
# 1,-1,-1,-2
# -2,-2,0,1
# 0,2,1,3
# -2,3,-2,1
# 0,2,3,-2
# -1,-1,1,-2
# 0,-2,-1,0
# -2,2,3,-1
# 1,2,2,0
# -1,-2,0,-2
#     """.strip().splitlines()

    sk = StarrySky()
    for coord in parse(lines):
        sk.add_star(coord)

    return len(sk.constellations)

@util.timing_wrapper
def star2():
    pass

if __name__ == '__main__':
    util.pretty_print(star1, star2)
