import util
import operator

DAY = 16

class VirtualMachine:
    def __init__(self):
        self.regs = [0,0,0,0]

    def __getattr__(self, instr):
        if len(instr) != 4:
            raise AttributeError(instr)

        arithmetic_instruction = True
        assignment_instruction = False
        if instr.startswith('add'):
            op = operator.add
        elif instr.startswith('mul'):
            op = operator.mul
        elif instr.startswith('ban'):
            op = operator.and_
        elif instr.startswith('bor'):
            op = operator.or_
        elif instr.startswith('set'):
            assignment_instruction = True
            op = lambda a,b: a
        else:
            arithmetic_instruction = False
            if instr.startswith('gt'):
                op = lambda a,b: 1 if a > b else 0
            elif instr.startswith('eq'):
                op = lambda a,b: 1 if a == b else 0
            else:
                raise AttributeError(instr)

            if instr.endswith('ir'):
                geta = lambda a: a
                getb = lambda b: self.regs[b]
            elif instr.endswith('ri'):
                geta = lambda a: self.regs[a]
                getb = lambda b: b
            elif instr.endswith('rr'):
                geta = lambda a: self.regs[a]
                getb = lambda b: self.regs[b]
            else:
                raise AttributeError(instr)

        if arithmetic_instruction:
            geta = lambda a: self.regs[a]
            if instr.endswith('r'):
                getb = lambda b: self.regs[b]
            else:
                getb = lambda b: b

        if assignment_instruction:
            getb = lambda b: None
            if instr.endswith('r'):
                geta = lambda a: self.regs[a]
            else:
                geta = lambda a: a

        def instr(a,b,c):
            self.regs[c] = op(geta(a),getb(b))

        return instr

class TestCase:
    def __init__(self, vm, before, instruction, after):
        self.vm = vm
        self.regs_bf = before
        self.regs_af = after
        self.opcode,self.instr_a,self.instr_b,self.instr_c = instruction

    def __getattr__(self, name):
        if name.startswith('chk_'):
            def chk_fun():
                original_regs = self.vm.regs
                try:
                    self.vm.regs = self.regs_bf[::]
                    getattr(self.vm, name[4:])(self.instr_a,self.instr_b,self.instr_c)
                    return self.vm.regs == self.regs_af
                finally:
                    self.vm.regs = original_regs
            return chk_fun
        else:
            raise AttributeError(instr)

    def possible_opcodes(self):
        return sum(getattr(self, 'chk_'+instr_name)() for instr_name in (
            'addr', 'addi',
            'mulr', 'muli',
            'banr', 'bani',
            'borr', 'bori',
            'setr', 'seti',
            'gtir', 'gtri', 'gtrr',
            'eqir', 'eqri', 'eqrr'
        ))

class Decoder:
    def __init__(self):
        self.opcode_map = {
            i:['addr', 'addi',
               'mulr', 'muli',
               'banr', 'bani',
               'borr', 'bori',
               'setr', 'seti',
               'gtir', 'gtri', 'gtrr',
               'eqir', 'eqri', 'eqrr']
            for i in range(16)
        }

    def add_tc_info(self, test_case):
        self.opcode_map[test_case.opcode] = [
            possible_instr
            for possible_instr in self.opcode_map[test_case.opcode]
            if getattr(test_case, 'chk_'+possible_instr)()
        ]

    def be_a_smart_boy(self):
        opcodes_we_know_for_sure = set()
        last_length = -1
        while last_length < len(opcodes_we_know_for_sure):
            last_length = len(opcodes_we_know_for_sure)
            for opcode,possibilities in self.opcode_map.items():
                if len(possibilities) == 1:
                    opcodes_we_know_for_sure.add(possibilities[0])
            for opcode,possibilities in self.opcode_map.items():
                if len(possibilities) != 1:
                    self.opcode_map[opcode] = [pos for pos in possibilities if pos not in opcodes_we_know_for_sure]

    def run(self, instr, vm):
        opcodes = self.opcode_map[instr[0]]
        if len(opcodes) != 1:
            raise Exception("Oops, this isn't good....")
        getattr(vm, opcodes[0])(instr[1], instr[2], instr[3])

def parse_instruction(l):
    return ([int(x) for x in l[0].replace('Before: ','').replace('[','').replace(']','').split(',')],
            [int(x) for x in l[1].split()],
            [int(x) for x in l[2].replace('After:  ','').replace('[','').replace(']','').split(',')])

def parse_input(vm):
    split_input = util.get_input_text(DAY).split('\n\n');
    test_cases = []
    for tc_str in split_input[:-2]:
        tc = TestCase(vm, *parse_instruction(tc_str.split('\n')))
        test_cases.append(tc)
    return test_cases, [[int(x) for x in instr.split()] for instr in split_input[-1].split('\n')]

@util.timing_wrapper
def star1():
    vm = VirtualMachine()
    test_cases,test_program = parse_input(vm)
    return sum(test_case.possible_opcodes() >= 3 for test_case in test_cases)

@util.timing_wrapper
def star2():
    vm = VirtualMachine()
    dc = Decoder()
    test_cases,test_program = parse_input(vm)
    
    for tc in test_cases:
        dc.add_tc_info(tc)

    dc.be_a_smart_boy()

    for instr in test_program:
        dc.run(instr, vm)

    return vm.regs[0]

if __name__ == '__main__':
    util.pretty_print(star1, star2)
