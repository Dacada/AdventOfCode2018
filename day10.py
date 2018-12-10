import util

DAY = 10

class Point:
    def __init__(self, px, py, vx, vy):
        self.posx = px
        self.posy = py
        self.velx = vx
        self.vely = vy

    def step(self):
        self.posx += self.velx
        self.posy += self.vely

    def __str__(self):
        return "position=<{0}, {1}> velocity=<{2}, {3}>".format(self.posx,self.posy,self.velx,self.vely)

def parse_input(text):
    return int(text[10:16]),int(text[18:24]),int(text[36:38]),int(text[40:42])

def print_grid(points):
    minx = +9999999
    miny = +9999999
    maxx = -9999999
    maxy = -9999999

    for point in points:
        if point.posx < minx:
            minx = point.posx
        if point.posy < miny:
            miny = point.posy
        if point.posx > maxx:
            maxx = point.posx
        if point.posy > maxy:
            maxy = point.posy

    x = abs(maxx - minx) + 1
    y = abs(maxy - miny) + 1

    if y > 10:
        return False

    grid = [[' ']*x for __ in range(y)]

    for point in points:
        grid[point.posy-miny][point.posx-minx] = '#'

    for row in grid:
        print(''.join(row))
        
    return True

@util.timing_wrapper
def star1():
    points = []
    for point_text in util.get_input_lines(DAY):
        px,py,vx,vy = parse_input(point_text)
        point = Point(px,py,vx,vy)
        points.append(point)

    column_alignments = {}
    do_print = False
    seconds = 0
    while True:
        for point in points:
            point.step()
            column_alignments[point.posy] = column_alignments.setdefault(point.posy,0) + 1
        seconds += 1
            
        if any(n >= 10 for n in column_alignments.values()):
            do_print = True
            
        if do_print:
            if print_grid(points):
                return seconds # return number of seconds for star2

star2 = star1

if __name__ == '__main__':
    util.pretty_print(star1, star2)
