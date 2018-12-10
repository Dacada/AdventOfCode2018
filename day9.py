import util

DAY = 9

class CircularLinkedListNode:
    def __init__(self, value):
        self.value = value
        self.prev_node = None
        self.next_node = None
            
class CircularLinkedList:
    def __init__(self, iterable):
        self.root = None
        
        iterator = iter(iterable)
        try:
            self.root = CircularLinkedListNode(next(iterator))
        except StopIteration:
            return
        node = self.root

        for element in iterator:
            new_node = CircularLinkedListNode(element)
            node.next_node = new_node
            new_node.prev_node = node
            node = newNode

        node.next_node = self.root
        self.root.prev_node = node

    def insert(self, node, value):
        """Insert new node with value after given node. Return inserted node."""
        new_node = CircularLinkedListNode(value)
        next = node.next_node
        node.next_node = new_node
        new_node.next_node = next
        new_node.prev_node = node
        next.prev_node = new_node
        return new_node

    def remove(self, node):
        """Remove given node from list. Return node after given node."""
        prev = node.prev_node
        next = node.next_node
        prev.next_node = next
        next.prev_node = prev
        if node is self.root:
            self.root = next
        return next

    def tostr(self, node):
        if self.root is node:
            s = '('+str(self.root.value) + ') '
        else:
            s = str(self.root.value) + ' '
        n = self.root.next_node
        while n is not self.root:
            if n is node:
                s += '('+str(n.value)+') '
            else:
                s += str(n.value) + ' '
            n = n.next_node
        return s

class Game:
    def __init__(self, players, last):
        self.players = players # number of players
        self.scores = [0]*players # keep track of scores
        self.marbles = [n for n in range(last,0,-1)] # marbles yet to place in reverse order
        self.circle = CircularLinkedList([0]) # placed marbles
        self.current = self.circle.root # node of the 'current' marble
        #print("[-] (0)")

    def play(self):
        while self.marbles:
            for player in range(self.players):
                if not self.marbles:
                    break
                next_marble = self.marbles.pop()
                if next_marble % 23 == 0:
                    self.scores[player] += next_marble
                    to_remove = self.current
                    for __ in range(7):
                        to_remove = to_remove.prev_node
                    self.scores[player] += to_remove.value
                    self.current = self.circle.remove(to_remove)
                else:
                    self.current = self.circle.insert(self.current.next_node, next_marble)
                #print('['+str(player+1)+']  '+self.circle.tostr(self.current))

    def winning_score(self):
        return max(self.scores)

def get_parameters(text):
    words = text.split()
    return int(words[0]),int(words[6])

@util.timing_wrapper
def star1():
    players,last = get_parameters(util.get_input_text(DAY))
    game = Game(players, last)
    #game = Game(9, 25)
    game.play()
    return game.winning_score()

@util.timing_wrapper
def star2():
    players,last = get_parameters(util.get_input_text(DAY))
    game = Game(players, last*100)
    game.play()
    return game.winning_score()

if __name__ == '__main__':
    util.pretty_print(star1, star2)
