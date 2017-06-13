from mathtex.astree import MathTexAST
from mathtex.fontmetric import FONT_METRICS
from mathtex.util import Array2D
from typing import List

class RowColumnMeta:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.width = 0
        self.height = 0
        self.baseline = 0


class HtmlElement:
    def __init__(self):
        self.name = "div"
        self.x = 0  # x-offset relative to parent
        self.y = 0  # y-offset relative to parent
        self.width = None  # element width
        self.height = None  # element height
        self.baseline = 0  # baseline relative to element top
        self.font_size = 1  # font-size relative to 1em
        self.css_class = None
        self.text = None
        self.children = []


class HtmlRender:
    def __init__(self):
        self.html_elements = []
        self.char_margin = 0
        self.cell_margin = 0.5
        self.line_margin = 0
        self.line_height = FONT_METRICS.height

    def render(self, node: MathTexAST, font_size) -> HtmlElement:
        if node.node_type == MathTexAST.TEXT_NODE:
            return self.render_text(node.text, font_size)
        if node.node_type == MathTexAST.BLOCK_NODE:
            return self.render_block(node.children, font_size)
        if node.node_type == MathTexAST.CELL_NODE:
            return self.render_block(node.children, font_size)

    def render_text(self, text, font_size) -> HtmlElement:
        elem = HtmlElement()
        elem.width = 0
        elem.height = self.line_height * font_size
        elem.baseline = ((self.line_height - FONT_METRICS.height) / 2 + FONT_METRICS.baseline) * font_size
        elem.font_size = font_size
        for i in range(0, len(text)):
            if i > 0:
                elem.width += self.char_margin * font_size
            c = text[i]
            child = HtmlElement()
            child.x = elem.width
            child.y = 0
            child.text = c
            child.font_size = font_size
            elem.width += FONT_METRICS.get_glyph(c).width * font_size
            elem.children.append(child)
        return elem

    def render_block(self, children, font_size) -> HtmlElement:
        elem = HtmlElement()
        elem.width = 0
        elem.height = 0
        elem.baseline = 0
        for i in range(0, len(children)):
            if i > 0:
                elem.width += self.char_margin * font_size
            child = self.render(children[i], font_size)
            child.x = elem.width
            child.y = 0
            if child.height > elem.height:
                elem.height = child.height
            if child.baseline > elem.baseline:
                elem.baseline = child.baseline
            elem.width += child.width
            elem.children.append(child)
        for child in elem.children:
            child.y = elem.baseline - child.baseline
        return elem

    def render_env(self, lines, font_size):
        a2d = Array2D()  # type: Array2D
        rows = []  # type: List[RowColumnMeta]
        columns = []  # type: List[RowColumnMeta]
        for i in range(0, len(lines)):
            rows.append(RowColumnMeta())
            if i > 0:
                rows[i].y = rows[i-1].y + rows[i-1].height + self.line_margin * font_size
            line = lines[i]  # type: MathTexAST
            for j in range(0, len(line.children)):
                if j >= len(columns):
                    columns.append(RowColumnMeta())
                cell = line.children[j]  # type: MathTexAST
                elem = self.render_block(cell.children, font_size)
                a2d.set(i, j, elem)
                if elem.height >= rows[i].height:
                    rows[i].height = elem.height
                if elem.baseline >= rows[i].baseline:
                    rows[i].baseline = elem.baseline
                if elem.width >= columns[j].width:
                    columns[j].width = elem.width
        for j in range(1, len(columns)):
            columns[j].x = columns[j-1].x + columns[j-1].width + self.cell_margin * font_size

