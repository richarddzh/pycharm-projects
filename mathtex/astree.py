class MathTexAST:
    BLOCK_NODE = 0
    LINE_NODE = 1
    CELL_NODE = 2
    TEXT_NODE = 3
    ENV_NODE = 4
    CMD_NODE = 5

    def __init__(self, node_type):
        self.children = []
        self.text = ""
        self.env_name = ""
        self.command = ""
        self.arg_number = 0
        self.node_type = node_type

    @staticmethod
    def block_node(children):
        node = MathTexAST(MathTexAST.BLOCK_NODE)
        node.children = children
        return node

    @staticmethod
    def cell_node(children):
        node = MathTexAST(MathTexAST.CELL_NODE)
        node.children = children
        return node

    @staticmethod
    def line_node(children):
        node = MathTexAST(MathTexAST.LINE_NODE)
        node.children = children
        return node

    @staticmethod
    def text_node(text):
        node = MathTexAST(MathTexAST.TEXT_NODE)
        node.text = text
        return node

    @staticmethod
    def env_node(env_name, children):
        node = MathTexAST(MathTexAST.ENV_NODE)
        node.env_name = env_name
        node.children = children
        return node

    @staticmethod
    def command_node(cmd, arg_number):
        node = MathTexAST(MathTexAST.CMD_NODE)
        node.command = cmd
        node.arg_number = arg_number
        node.children = []
        return node

    def __str__(self):
        sub_nodes = ",".join(map(lambda x: str(x), self.children))
        if self.node_type == MathTexAST.BLOCK_NODE:
            return "<Block: {0}>".format(sub_nodes)
        elif self.node_type == MathTexAST.CELL_NODE:
            return "<Cell: {0}>".format(sub_nodes)
        elif self.node_type == MathTexAST.ENV_NODE:
            return "<Env {0}: {1}>".format(self.env_name, sub_nodes)
        elif self.node_type == MathTexAST.LINE_NODE:
            return "<Line: {0}>".format(sub_nodes)
        elif self.node_type == MathTexAST.TEXT_NODE:
            return "<Text: {0}>".format(self.text)
        elif self.node_type == MathTexAST.CMD_NODE:
            return "<Cmd {0}: {1}>".format(self.command, sub_nodes)
        else:
            return "<MathTexAST Unknown>"