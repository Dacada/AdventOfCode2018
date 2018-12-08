import util

DAY = 8

class Node:
    def __init__(self):
        self.children = []
        self.metadata = []
        self.value = None
        
    def parse(self, numbers, i):
        children_len = numbers[i]
        i += 1
        metadata_len = numbers[i]
        i += 1
        
        for __ in range(children_len):
            child = Node()
            i = child.parse(numbers, i)
            self.children.append(child)

        for __ in range(metadata_len):
            self.metadata.append(numbers[i])
            i += 1

        return i

    def get_metadata_sum(self):
        s = sum(self.metadata)
        for node in self.children:
            s += node.get_metadata_sum()
        return s

    def get_value(self):
        if self.value is None:
            if self.children:
                self.value = 0
                for i in self.metadata:
                    i -= 1
                    if i >= 0 and i < len(self.children):
                        self.value += self.children[i].get_value()
            else:
                self.value = sum(self.metadata)
        
        return self.value

@util.timing_wrapper
def star1():
    root = Node()
    root.parse(list(int(n) for n in util.get_input_words(DAY)), 0)
    return root.get_metadata_sum()

@util.timing_wrapper
def star2():
    root = Node()
    root.parse(list(int(n) for n in util.get_input_words(DAY)), 0)
    return root.get_value()

if __name__ == '__main__':
    util.pretty_print(star1, star2)
