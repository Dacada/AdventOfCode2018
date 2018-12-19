import util
import subprocess
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

    def run(self, program, maxinstr=None):
        instrcnt = 0
        while self.ip < len(program):
            instr,a,b,c = program[self.ip]
            getattr(self, instr)(a, b, c)
            self.ip += 1
            instrcnt += 1
            if maxinstr is not None and instrcnt >= maxinstr:
                break

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
    """After a lot of reverse engineering (see 2017,day23) this program
    calculates an enormous number at r5, then adds up its divisors into
    r0.

    So just run the vm for something like 1000 cycles, then stop it
    and get the value of r5.  Then get the factors of that number, add
    them up, return that.

    """
    program,ip_reg = get_program(util.get_input_lines(DAY))
    vm = VirtualMachineV2(ip_reg)
    vm.regs[0] = 1

    vm.run(program, 1000)
    n = max(vm.regs)
    cp = subprocess.run(['factor', str(n)], capture_output=True, text=True) #not cheating

    sum_divisors = 1
    factors_list = [int(x) for x in cp.stdout.split(':')[1].split() if not x.isspace()]
    factors = {factor:factors_list.count(factor) for factor in factors_list}
    for factor in factors:
        sum_divisors *= (factor ** (factors[factor] + 1) - 1) / (factor - 1)
    return int(sum_divisors)

if __name__ == '__main__':
    util.pretty_print(star1, star2)
