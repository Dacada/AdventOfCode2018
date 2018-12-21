import util
import itertools
from day19 import VirtualMachineV2,get_program

DAY = 21

class VirtualMachineV3(VirtualMachineV2):
    def __init__(self, program, ip_reg):
        super().__init__(ip_reg)
        self.program = program

    def reset(self):
        self.regs = [0,0,0,0,0,0]
        self.ip = 0
        
    def run_step(self):
        if self.ip >= len(self.program):
            return False
        else:
            instr,a,b,c = self.program[self.ip]
            getattr(self, instr)(a,b,c)
            self.ip += 1
            return True

    def run(self, maxinstr=None, stop_ip=None):
        instrcnt = 0
        while self.run_step():
            instrcnt += 1
            if maxinstr is not None and instrcnt >= maxinstr:
                break
            if stop_ip is not None and self.ip == stop_ip:
                break
        return instrcnt

@util.timing_wrapper
def star1():
    vm = VirtualMachineV3(*get_program(util.get_input_lines(DAY)))
    vm.run(stop_ip=28)
    magic = vm.regs[vm.program[vm.ip][1]]

    # checking it does actually work...
    vm.reset()
    vm.regs[0] = magic
    vm.run()

    return magic

@util.timing_wrapper
def star2():
    vm = VirtualMachineV3(*get_program(util.get_input_lines(DAY)))
    
    seen_magics = set()
    magic = 1
    prev_magic = 2
    prev_prev_magic = 3
    while magic != prev_magic: # I have to go, just brute force it and let it run for hours c:
        vm.run(stop_ip=28)
        prev_prev_magic = prev_magic
        prev_magic = magic
        magic = vm.regs[vm.program[vm.ip][1]]
        #print(vm.program[vm.ip], vm.regs)
        vm.run_step()
    
    print(vm.program[vm.ip], vm.regs)

    # This time I'm not checking...

    return prev_prev_magic

if __name__ == '__main__':
    util.pretty_print(star1, star2)
