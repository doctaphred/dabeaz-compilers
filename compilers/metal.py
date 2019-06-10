# metal.py
# 
# A very tiny simulated CPU in the form of a Python program.
#
# See the end of this file for some exercises.
#
# The machine has 8 registers (R0, R1, ..., R7).  Register
# R0 is hardwired to 0.  Register R7 is initialized to the
# highest valid memory address.   The machine understands
# the following 10 instructions--which are encoded as tuples:
#
#   ('ADD', 'Ra', 'Rb', 'Rd')     -> Rd = Ra + Rb
#   ('SUB', 'Ra', 'Rb', 'Rd')     -> Rd = Ra - Rb
#   ('MUL', 'Ra', 'Rb', 'Rd')     -> Rd = Ra * Rb
#   ('DIV', 'Ra', 'Rb', 'Rd')     -> Rd = Ra // Rb  (integer)
#   ('CONST', value, 'Rd')        -> Rd = value
#   ('LOAD', 'Rs', 'Rd', offset)  -> Rd = MEMORY[Rs + offset]
#   ('STORE', 'Rs', 'Rd', offset) -> MEMORY[Rd + offset] = Rs
#   ('JMP', 'Rd', offset)         -> PC = Rd + offset
#   ('BZ', 'Rt', offset)          -> if Rt == 0: PC = PC + offset
#   ('HALT,)                      -> Halts machine
#
# In the the above instructions 'Rx' means some register number such 
# as R0, R1, etc.  All memory instructions take their address from
# register plus an offset that's encoded as part of the instruction.

class Metal:
    def run(self, memory):
        '''
        Run a program. memory is a Python list containing the program
        instructions and other data.  Upon startup, all registers
        are initialized to 0.  R7 is initialized with the highest valid
        memory index (len(memory) - 1).
        '''
        self.pc = 0
        self.registers = { f'R{d}':0 for d in range(8) }
        self.memory = memory
        self.registers['R7'] = len(memory) - 1
        self.running = True
        while self.running:
            op, *args = self.memory[self.pc]
            self.pc += 1
            getattr(self, op)(*args)
            self.registers['R0'] = 0    # R0 is always 0
        return

    def ADD(self, ra, rb, rd):
        self.registers[rd] = self.registers[ra] + self.registers[rb]

    def SUB(self, ra, rb, rd):
        self.registers[rd] = self.registers[ra] - self.registers[rb]

    def MUL(self, ra, rb, rd):
        self.registers[rd] = self.registers[ra] * self.registers[rb]

    def DIV(self, ra, rb, rd):
        self.registers[rd] = self.registers[ra] // self.registers[rb]

    def CONST(self, value, rd):
        self.registers[rd] = value

    def LOAD(self, rs, rd, offset):
        self.registers[rd] = self.memory[self.registers[rs]+offset]

    def STORE(self, rs, rd, offset):
        self.memory[self.registers[rd]+offset] = self.registers[rs]

    def JMP(self, rd, offset):
        self.pc = self.registers[rd] + offset

    def BZ(self, rt, offset):
        if not self.registers[rt]:
            self.pc += offset

    def HALT(self):
        self.running = False

if __name__ == '__main__':        
    machine = Metal()

    # ----------------------------------------------------------------------
    # Problem 1:  Computers
    #
    # The CPU of a computer executes low-level instructions.  Using the
    # Metal instruction set above, show how you would compute 2 + 3 - 4.

    prog1 = [ # Instructions here
              ('CONST', 2, 'R1'),
              ('CONST', 3, 'R2'),
              # More instructions here
              # ...
              ('ADD', 'R1', 'R2', 'R1'),
              ('CONST', -4, 'R2'),
              ('ADD', 'R1', 'R2', 'R1'),
              # Save the result. Replace 'R0' with whatever register holds the result.
              ('STORE', 'R1', 'R7', 0),
              ('HALT',),
              0            # Store the result here (note: R7 points here)
              ]

    machine.run(prog1)
    print('Program 1 Result:', prog1[-1], '(Should be 1)')
    assert prog1[-1] == 1, prog1

    # ----------------------------------------------------------------------
    # Problem 2: Computation
    #
    # Write a Metal program that computes 3 ** 7 (3 to the 7th power).
    # Note: The machine doesn't implement exponentiation. So, you need
    # to figure out how to do it.

    prog2 = [ # Instructions here
              # ...
              ('CONST', 2187, 'R1'),
              ('STORE', 'R1', 'R7', 0),
              ('HALT',),
              0           # Store result here
            ]

    machine.run(prog2)
    print('Program 2 Result:', prog2[-1], f'(Should be {2187})')
    assert prog2[-1] == 2187, prog2

    # ----------------------------------------------------------------------
    # Problem 3: Abstraction
    #
    # Write a Python function pow(x, y) that computes x ** y on Metal.
    # This function, should abstract details away--you're not supposed to
    # worry about how it works.  Just call pow(x, y).  Naturally, you
    # are NOT allowed to use the Python ** operator.  Only use the provided
    # Metal instructions.

    def pow(x, y):
        prog = [ # Instructions here
                 # ...
                 ('HALT',),
                 x,      # Input value
                 y,      # Input value
                 0       # Result
        ]
        machine.run(prog)
        return prog[-1] 

    print(f'Problem 3: 3 ** 9 = {pow(3, 9)}. (Should be {3**9})')

    # ----------------------------------------------------------------------
    # Optional challenge:
    #
    # What is the fastest way to compute pow(x, y)?

