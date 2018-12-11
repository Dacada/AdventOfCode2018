import util

DAY = 11

def calc_power(x, y, serial):
    id = x + 10
    power = id * y
    power += serial
    power *= id
    power = power//100 - power//1000*10
    power -= 5
    return power

def compute_table(serial):
    table = []
    for y in range(300):
        row = []
        for x in range(300):
            row.append(calc_power(x+1, y+1, serial))
        table.append(row)
    return table

def compute_summed_area_table(table):
    summed_area_table = [[None]*300 for __ in range(300)]
    for y in range(300):
        for x in range(300):
            sat_element(x,y,table,summed_area_table)
    return summed_area_table

def sat_element(x,y,table,sat):
    if sat[y][x] is not None:
        return sat[y][x]
    else:
        res = table[y][x]
        if y > 0:
            res += sat_element(x, y-1, table, sat)
        if x > 0:
            res += sat_element(x-1, y, table, sat)
        if x > 0 and y > 0:
            res -= sat_element(x-1, y-1, table, sat)
        sat[y][x] = res
        return res

def calc_square_power(x, y, size, sat):
    return sat[y+size][x+size] + sat[y][x] - sat[y][x+size] - sat[y+size][x]

@util.timing_wrapper
def star1():
    serial = int(util.get_input_text(DAY))
    table = compute_table(serial)
    summed_area_table = compute_summed_area_table(table)
    
    maxval = -999999
    maxcoords = None
    
    for x in range(300-3):
        for y in range(300-3):
            power = calc_square_power(x,y,3,summed_area_table)
            if power > maxval:
                maxval = power
                maxcoords = (x,y)
                
    return ','.join(str(c+2) for c in maxcoords)

@util.timing_wrapper
def star2():
    serial = int(util.get_input_text(DAY))
    table = compute_table(serial)
    summed_area_table = compute_summed_area_table(table)
    
    maxval = -999999
    maxcoords = None

    for size in range(3,100):
        for x in range(300-size):
            for y in range(300-size):
                power = calc_square_power(x,y,size,summed_area_table)
                if power > maxval:
                    maxval = power
                    maxcoords = (x,y,size)
                
    return str(maxcoords[0]+2)+','+str(maxcoords[1]+2)+','+str(maxcoords[2])

if __name__ == '__main__':
    util.pretty_print(star1, star2)
