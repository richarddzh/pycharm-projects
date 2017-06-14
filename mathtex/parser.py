import re
from mathtex.astree import MathTexAST
from mathtex.util import last_index
from mathtex.texcharset import TEX_CHARSET


RE_CMD = re.compile(r"\\([A-Za-z]+|.)", re.DOTALL)
RE_BEGIN_ENV = re.compile(r"\\begin\{([A-Za-z]+)\}")
RE_END_ENV = re.compile(r"\\end\{([A-Za-z]+)\}")
RE_WHITESPACE = re.compile(r"\s+")
RE_COMMENT = re.compile(r"%.*")

ROOT_ENV = "ROOT_ENV"

BEGIN_CELL = 1
BEGIN_LINE = 2
BEGIN_BLOCK = 3
BEGIN_ENV = 4

TEX_CMD_ARG_NUMBER = {
    "frac": 2,
    "sqrt": 1,
    "boldsymbol": 1,
    "left": 1,
    "right": 1,
}


class MathTexParser:
    def __init__(self):
        self.stack = []

    def parse_line(self, line):
        m = None  # type: re.__Match
        line_len = len(line)
        start_pos = 0
        while start_pos < line_len:
            if m is not None:
                start_pos = m.end()
            if start_pos >= line_len:
                break
            m = RE_WHITESPACE.match(line, start_pos)
            if m is not None:
                continue
            m = RE_COMMENT.match(line, start_pos)
            if m is not None:
                continue
            m = RE_BEGIN_ENV.match(line, start_pos)
            if m is not None:
                self.begin_env(m.group(1))
                continue
            m = RE_END_ENV.match(line, start_pos)
            if m is not None:
                self.end_env()
                continue
            m = RE_CMD.match(line, start_pos)
            if m is not None:
                self.do_command(m.group(1))
                continue
            self.do_char(line[start_pos])
            start_pos += 1

    def begin_env(self, env_name):
        self.stack.append(env_name)
        self.stack.append(BEGIN_ENV)

    def end_env(self):
        self.end_line(False)
        begin_index = last_index(self.stack, lambda x: x == BEGIN_ENV)
        if begin_index >= 1:
            env_name = self.stack[begin_index - 1]
            children = self.process_sequence(self.stack[begin_index + 1:])
            env_node = MathTexAST.env_node(env_name, children)
            self.stack = self.stack[0:begin_index - 1]
            self.stack.append(env_node)

    def begin_parse(self):
        self.stack = [ROOT_ENV, BEGIN_ENV]

    def end_parse(self):
        self.end_env()
        return self.stack[-1]

    def end_line(self, new_line):
        self.end_cell(False)
        begin_index = last_index(self.stack, lambda x: (x == BEGIN_LINE or x == BEGIN_ENV))
        children = self.process_sequence(self.stack[begin_index + 1:])
        line_node = MathTexAST.line_node(children)
        if begin_index >= 0 and self.stack[begin_index] == BEGIN_LINE:
            begin_index -= 1
        self.stack = self.stack[0:begin_index + 1]
        self.stack.append(line_node)
        if new_line:
            self.stack.append(BEGIN_LINE)

    def end_cell(self, new_cell):
        begin_index = last_index(self.stack, lambda x: (x == BEGIN_CELL or x == BEGIN_ENV or x == BEGIN_LINE))
        children = self.process_sequence(self.stack[begin_index + 1:])
        cell_node = MathTexAST.cell_node(children)
        if begin_index >= 0 and self.stack[begin_index] == BEGIN_CELL:
            begin_index -= 1
        self.stack = self.stack[0:begin_index + 1]
        self.stack.append(cell_node)
        if new_cell:
            self.stack.append(BEGIN_CELL)

    def do_command(self, cmd):
        if cmd == "\\":
            self.end_line(True)
        elif cmd in TEX_CMD_ARG_NUMBER:
            self.push_command(cmd, TEX_CMD_ARG_NUMBER[cmd])
        else:
            c = TEX_CHARSET.get_char(cmd)
            if c is not None:
                self.stack.append(MathTexAST.text_node(c))
            else:
                self.push_command(cmd, 0)

    def push_command(self, cmd, arg_number):
        self.stack.append(MathTexAST.command_node(cmd, arg_number))

    def do_char(self, c):
        if c == "{":
            self.stack.append(BEGIN_BLOCK)
        elif c == "}":
            begin_index = last_index(self.stack, lambda x: x == BEGIN_BLOCK)
            if begin_index >= 0:
                children = self.process_sequence(self.stack[begin_index + 1:])
                block_node = MathTexAST.block_node(children)
                self.stack = self.stack[0:begin_index]
                self.stack.append(block_node)
        elif c == "_" or c == "^":
            self.push_command(c, 1)
        elif c == "&":
            self.end_cell(True)
        else:
            self.stack.append(MathTexAST.text_node(c))

    @staticmethod
    def process_sequence(nodes):
        result = []
        i = 0
        while i < len(nodes):
            node = nodes[i]
            if isinstance(node, MathTexAST):
                if len(result) > 0:
                    last_node = result[-1]  # type: MathTexAST
                    if last_node.node_type == MathTexAST.TEXT_NODE and node.node_type == MathTexAST.TEXT_NODE:
                        last_node.text += node.text
                        i += 1
                        continue
                if node.node_type == MathTexAST.CMD_NODE:
                    node.children = nodes[i + 1:i + 1 + node.arg_number]
                    i += node.arg_number
                    result.append(node)
                else:
                    result.append(node)
            i += 1
        return result
