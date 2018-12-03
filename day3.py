import util

DAY = 3

def parse_spec(spec):
    poundid,atsign,start,dims = spec.split()
    id = poundid[1:]
    startx,startycolon = start.split(',')
    lenx,leny = dims.split('x')
    starty = startycolon.replace(':','')
    return id,int(startx),int(starty),int(lenx),int(leny)

@util.timing_wrapper
def star1():
    fabric = [[0 for i in range(1000)] for j in range(1000)]
    for spec in util.get_input_lines(DAY):
        id,startx,starty,lenx,leny = parse_spec(spec)
        for j in range(startx, startx+lenx):
            for i in range(starty, starty+leny):
                fabric[j][i] += 1
    return sum(sum(x >= 2 for x in l) for l in fabric)

@util.timing_wrapper
def star2():
    fabric = [[[] for i in range(1000)] for j in range(1000)]
    all_ids = set()
    
    for spec in util.get_input_lines(DAY):
        id,startx,starty,lenx,leny = parse_spec(spec)
        all_ids.add(id)
        for j in range(startx, startx+lenx):
            for i in range(starty, starty+leny):
                fabric[j][i].append(id)
                
    overlapping_ids = set()
    for row in fabric:
        for ids in row:
            if len(ids) > 1:
                for id in ids:
                    overlapping_ids.add(id)
    
    return (all_ids - overlapping_ids).pop()
                

if __name__ == '__main__':
    util.pretty_print(star1, star2)
