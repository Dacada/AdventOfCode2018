import util
import collections
import heapq

DAY = 23

Point3D = collections.namedtuple('Point3D', ['x', 'y', 'z'])
Nanobot = collections.namedtuple('Nanobot', ['coords', 'radius'])
Box = collections.namedtuple('Box', ['max', 'min'])

def manhattan(p,q):
    return sum(abs(cp-cq) for cp,cq in zip(p,q))

def parse_nanobot(s):
    return Nanobot(Point3D(*(int(c) for c in s[5:s.index('>')].split(','))),int(s[s.index('r=')+2:]))

def parse_input(lines):
    return [parse_nanobot(l) for l in lines]

def diameter(box):
    return manhattan(box.min, box.max)

def halfway(c1,c2):
    return Point3D((c1.x+c2.x)//2, (c1.y+c2.y)//2, (c1.z+c2.z)//2)

def nanobots_range_in_box(nanobots, box):
    return sum(intersects(bot, box) for bot in nanobots)

def nanobots_range_in_point(nanobots, point):
    return sum(manhattan(bot.coords, point) <= bot.radius for bot in nanobots)

def intersects(sphere, aabb):
    x = max(aabb.min.x, min(sphere.coords.x, aabb.max.x))
    y = max(aabb.min.y, min(sphere.coords.y, aabb.max.y))
    z = max(aabb.min.z, min(sphere.coords.z, aabb.max.z))

    distance = manhattan((x,y,z), sphere.coords)

    return distance <= sphere.radius

def subdivide(b):
    c1 = b.max
    c2 = b.min
    hh = halfway(c1,c2)
    return (
        Box(Point3D(c1.x, c1.y, c1.z),Point3D(hh.x, hh.y, hh.z)),
        Box(Point3D(hh.x, c1.y, c1.z),Point3D(c2.x, hh.y, hh.z)),
        Box(Point3D(c1.x, hh.y, c1.z),Point3D(hh.x, c2.y, hh.z)),
        Box(Point3D(hh.x, hh.y, c1.z),Point3D(c2.x, c2.y, hh.z)),
        Box(Point3D(c1.x, c1.y, hh.z),Point3D(hh.x, hh.y, c2.z)),
        Box(Point3D(hh.x, c1.y, hh.z),Point3D(c2.x, hh.y, c2.z)),
        Box(Point3D(c1.x, hh.y, hh.z),Point3D(hh.x, c2.y, c2.z)),
        Box(Point3D(hh.x, hh.y, hh.z),Point3D(c2.x, c2.y, c2.z))
    )

@util.timing_wrapper
def star1():
    lines = util.get_input_lines(DAY)
    nanobots = parse_input(lines)
    strong= max(nanobots, key=lambda n: n.radius)
    return sum(manhattan(strong.coords, nanobot.coords) <= strong.radius for nanobot in nanobots)

@util.timing_wrapper
def star2():
    lines = util.get_input_lines(DAY)
    nanobots = parse_input(lines)

    # Create a box that contains all points to consider
    maxx = max(c.x for c,r in nanobots)
    maxy = max(c.y for c,r in nanobots)
    maxz = max(c.z for c,r in nanobots)
    minx = min(c.x for c,r in nanobots)
    miny = min(c.y for c,r in nanobots)
    minz = min(c.z for c,r in nanobots)
    box = Box(Point3D(maxx, maxy, maxz), Point3D(minx, miny, minz))

    # Keep a priority queue of boxes, by number of bots that touch them - number of nanobots
    PQElement = collections.namedtuple('PQElement', ['bots_not_in_box', 'count', 'box'])
    pq = [PQElement(0, 1, box)]
    count = 1
    
    # Binary search, sort of:
    # We keep a pq of boxes, and we find the maximum point in the box when it's small enough
    # Then we get the maximum out of all these maximum points (beat ties by distance to origin)
    # We do only a few of these matches, after like 20 it has most likely stabilized to the right answer
    
    best_nanobots_p = 0
    best_p = None
    best_distance_to_origin_p = 9999999999999
    matches_left = 20
            
    while pq and matches_left:
        __,___,box = heapq.heappop(pq)
        d = diameter(box)
        #if count % 10 == 0:
        #    print(d,count,__)
        if d < 10:
            # Our box is now very small, chose the best point out of all the points in the box
            # We will get the maximum out of all these points
            for x in range(min(box.max.x,box.min.x),max(box.max.x,box.min.x)):
                for y in range(min(box.max.y,box.min.y),max(box.max.y,box.min.y)):
                    for z in range(min(box.max.z,box.min.z),max(box.max.z,box.min.z)):
                        p = Point3D(x,y,z)
                        n = nanobots_range_in_point(nanobots, p)
                        #print(p,"has",n,"nanobots")
                        if n > best_nanobots_p:
                            best_distance_to_origin_p = manhattan(p,(0,0,0))
                            best_nanobots_p = n
                            best_p = p
                        elif n == best_nanobots_p:
                            d = manhattan(p,(0,0,0))
                            if d < best_distance_to_origin_p:
                                best_distance_to_origin_p = d
                                best_p = p
                                
            #print("Current best point:",best_p,"with",best_nanobots_p,"nanobots and distance to origin",best_distance_to_origin_p)
            #input()
            matches_left -= 1
        
        #print("Bounding box:",box,"(diameter:",d,")")
        #print("Subdividing into 8.")
        
        best_subboxes = []
        best_nanobots = 0
        for subbox in subdivide(box):
            n = nanobots_range_in_box(nanobots, subbox)
            #print("Bounding box",subbox,"has",n,"nanobot ranges in it")
            if n > best_nanobots:
                best_nanobots = n
                best_subboxes = [subbox]
            elif n == best_nanobots:
                best_subboxes.append(subbox)
        #print("Candidates:",best_subboxes,"with",best_nanobots,"nanobots")
        
        # In case of many subboxes with the same distance, add them all to the pq
        for b in best_subboxes:
            count += 1
            heapq.heappush(pq, PQElement(len(nanobots)-best_nanobots, count, b))

    #print("Chosen point:",best_p,"with",best_nanobots_p,"nanobots")
    return manhattan(best_p,(0,0,0))

if __name__ == '__main__':
    util.pretty_print(star1, star2)
