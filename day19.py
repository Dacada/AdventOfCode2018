import util
from day16 import VirtualMachine

DAY = 19

class VirtualMachineV2(VirtualMachine):
    def __init__(self, ip_reg):
        self.regs = [0,0,0,0,0,0]
        self.ip = 0
        self.reg_bound_to_ip = ip_reg

    def __getattr__(self, instr):
        instr_fun = super().__getattr__(instr)
        def wrapper(a,b,c):
            self.regs[self.reg_bound_to_ip] = self.ip
            #print('ip={0} {1} {2} {3} {4} {5}'.format(self.ip, self.regs, instr, a, b, c), end=' ')
            instr_fun(a,b,c)
            #print(self.regs)
            #input()
            self.ip = self.regs[self.reg_bound_to_ip]
        return wrapper

    def run(self, program):
        while self.ip < len(program):
            instr,a,b,c = program[self.ip]
            getattr(self, instr)(a, b, c)
            self.ip += 1

def get_program(lines):
    program = []
    for instr in lines:
        if instr.startswith('#'):
            ip_reg = int(instr.split()[1])
        else:
            instr,astr,bstr,cstr = instr.split()
            program.append((instr,int(astr),int(bstr),int(cstr)))
    return program,ip_reg

@util.timing_wrapper
def star1():
    lines = util.get_input_lines(DAY)
#    lines = """#ip 0
#seti 5 0 1
#seti 6 0 2
#addi 0 1 0
#addr 1 2 3
#setr 1 0 0
#seti 8 0 4
#seti 9 0 5""".split('\n')

    program,ip_reg = get_program(lines)
    vm = VirtualMachineV2(ip_reg)
    vm.run(program)
    return vm.regs[0]

@util.timing_wrapper
def star2():
    program,ip_reg = get_program(util.get_input_lines(DAY))
    vm = VirtualMachineV2(ip_reg)
    vm.regs[0] = 1
    vm.run(program)
    return vm.regs[0]

if __name__ == '__main__':
    util.pretty_print(star1, star2)
