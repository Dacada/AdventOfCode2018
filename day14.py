import util

DAY = 14

def print_recipes(recipes, i1, i2):
    for i,c in enumerate(recipes):
        if i == i1:
            print('('+str(recipes[i])+')',end='')
        elif i == i2:
            print('['+str(recipes[i])+']',end='')
        else:
            print(' '+str(recipes[i])+' ',end='')
    print()

@util.timing_wrapper
def star1():
    num = int(util.get_input_text(DAY))
    
    recipes = [3,7]
    i1 = 0
    i2 = 1
    
    while len(recipes) < num+10:
        #print_recipes(recipes, i1, i2)
        for c in str(recipes[i1] + recipes[i2]):
            recipes.append(int(c))
        i1 = (i1 + int(recipes[i1]) + 1) % len(recipes)
        i2 = (i2 + int(recipes[i2]) + 1) % len(recipes)
    #print_recipes(recipes, i1, i2)

    return ''.join(str(x) for x in recipes[num:num+10])

@util.timing_wrapper
def star2():
    num = util.get_input_text(DAY)
    #num = '51589'
    #num = '01245'
    #num = '92510'
    #num = '59414'
    
    recipes = [3,7]
    i1 = 0
    i2 = 1

    found = 0

    n = 0
    while found < len(num):
        for c in str(recipes[i1] + recipes[i2]):
            if c == num[found]:
                found += 1
                if found >= len(num):
                    break
            else:
                found = 0
                if c == num[found]:
                    found = 1
            recipes.append(int(c))
            n += 1
            
        i1 = (i1 + int(recipes[i1]) + 1) % len(recipes)
        i2 = (i2 + int(recipes[i2]) + 1) % len(recipes)

    return n - len(num) + 3

if __name__ == '__main__':
    util.pretty_print(star1, star2)
