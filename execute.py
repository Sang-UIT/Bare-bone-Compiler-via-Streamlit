class BareBoneCompiler:
    def __init__(self, instructions):
        self.instructions = instructions
        self.variables = {}

    def execute(self):
        self._execute_instructions(self.instructions)
        return self.variables

    def _execute_instructions(self, instructions):
        i = 0
        while i < len(instructions):
            instr = instructions[i]
            if instr[0] == 'clear':
                self.variables[instr[1]] = 0
            elif instr[0] == 'incr':
                self.variables[instr[1]] = self.variables.get(instr[1], 0) + 1
            elif instr[0] == 'decr':
                if self.variables.get(instr[1], 0) > 0:
                    self.variables[instr[1]] -= 1
            elif instr[0] == 'while':
                var = instr[1]
                while self.variables.get(var, 0) != 0:
                    self._execute_instructions(instr[2])
            i += 1

# Ví dụ sử dụng
"""
clear X
incr X
incr X
while X not 0 do
    decr X
    incr Y
    while Y not 0 do
        decr Y
        incr Z
    end
end
init W 3
"""
