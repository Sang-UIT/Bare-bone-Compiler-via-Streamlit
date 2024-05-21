import re

class SyntaxError(Exception):
    def __init__(self, message, line):
        super().__init__(message)
        self.line = line

class BareBoneParser:
    def __init__(self):
        self.instructions = []
        self.errors = []

    def parse(self, code):
        lines = code.strip().split('\n')
        self.instructions = []
        self.errors = []

        self._parse_lines(lines)

        if not self.errors:
            return self.instructions
        else:
            return self.errors

    def _parse_lines(self, lines):
        line_num = 0
        while line_num < len(lines):
            stripped_line = lines[line_num].strip()
            if stripped_line:
                try:
                    line_num = self._parse_line(stripped_line, lines, line_num)
                except SyntaxError as e:
                    self.errors.append((e.line, str(e)))
            line_num += 1

    def _parse_line(self, line, lines, line_num):
        if re.match(r'^clear \w+$', line):
            self.instructions.append(('clear', line.split()[1]))
        elif re.match(r'^incr \w+$', line):
            self.instructions.append(('incr', line.split()[1]))
        elif re.match(r'^decr \w+$', line):
            self.instructions.append(('decr', line.split()[1]))
        elif re.match(r'^while \w+ not 0 do$', line):
            var = line.split()[1]
            block = []
            line_num += 1
            nested_line_num = line_num
            while line_num < len(lines) and not re.match(r'^end$', lines[line_num].strip()):
                nested_line = lines[line_num].strip()
                if not nested_line:
                    line_num += 1
                    continue
                try:
                    line_num = self._parse_nested_line(nested_line, lines, line_num, block)
                except SyntaxError as e:
                    self.errors.append((e.line, str(e)))
                nested_line_num += 1
                line_num += 1
            if line_num == len(lines) or not re.match(r'^end$', lines[line_num].strip()):
                raise SyntaxError(f"Missing 'end' for 'while' starting at line {line_num + 1}", line_num + 1)
            self.instructions.append(('while', var, block))
        elif re.match(r'^end$', line):
            raise SyntaxError(f"Unexpected 'end' at line {line_num + 1}", line_num + 1)
        elif re.match(r'^init \w+ \d+$', line):
            parts = line.split()
            var = parts[1]
            value = int(parts[2])
            self.instructions.append(('clear', var))
            for _ in range(value):
                self.instructions.append(('incr', var))
        else:
            raise SyntaxError(f"Syntax error: {line}", line_num + 1)
        return line_num

    def _parse_nested_line(self, line, lines, line_num, block):
        if re.match(r'^clear \w+$', line):
            block.append(('clear', line.split()[1]))
        elif re.match(r'^incr \w+$', line):
            block.append(('incr', line.split()[1]))
        elif re.match(r'^decr \w+$', line):
            block.append(('decr', line.split()[1]))
        elif re.match(r'^while \w+ not 0 do$', line):
            var = line.split()[1]
            nested_block = []
            line_num += 1
            nested_line_num = line_num
            while line_num < len(lines) and not re.match(r'^end$', lines[line_num].strip()):
                nested_line = lines[line_num].strip()
                if not nested_line:
                    line_num += 1
                    continue
                try:
                    line_num = self._parse_nested_line(nested_line, lines, line_num, nested_block)
                except SyntaxError as e:
                    self.errors.append((e.line, str(e)))
                nested_line_num += 1
                line_num += 1
            if line_num == len(lines) or not re.match(r'^end$', lines[line_num].strip()):
                raise SyntaxError(f"Missing 'end' for 'while' starting at line {nested_line_num}", nested_line_num)
            block.append(('while', var, nested_block))
        elif re.match(r'^end$', line):
            raise SyntaxError(f"Unexpected 'end' at line {line_num + 1}", line_num + 1)
        elif re.match(r'^init \w+ \d+$', line):
            parts = line.split()
            var = parts[1]
            value = int(parts[2])
            block.append(('clear', var))
            for _ in range(value):
                block.append(('incr', var))
        else:
            raise SyntaxError(f"Syntax error: {line}", line_num + 1)
        return line_num

    def get_errors(self):
        return self.errors
