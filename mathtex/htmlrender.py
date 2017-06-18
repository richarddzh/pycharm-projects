from mathtex.astree import MathTexAST
from mathtex.fontmetric import FONT_METRICS
from mathtex.htmlelement import HtmlElement
from mathtex.util import Array1D
from mathtex.util import Array2D
from typing import List


class RowColumnMeta:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.width = 0
        self.height = 0
        self.baseline = 0


class HtmlRender:
    def __init__(self):
        self.html_elements = []
        self.char_margin = 0
        self.cell_margin = 0.5
        self.line_margin = 0
        self.line_height = FONT_METRICS.height

    @staticmethod
    def get_baseline(line_height, font_size):
        return (line_height - FONT_METRICS.height * font_size) / 2 + FONT_METRICS.baseline * font_size

    def align_children(self, elem: HtmlElement, font_size):
        elem.width = 0
        elem.height = 0
        elem.baseline = 0
        for i in range(0, len(elem.children)):
            if i > 0:
                elem.width += self.char_margin * font_size
            child = elem.children[i]
            child.x = elem.width
            if child.height > elem.height:
                elem.height = child.height
            if child.baseline > elem.baseline:
                elem.baseline = child.baseline
            elem.width += child.width
        for child in elem.children:
            child.y = elem.baseline - child.baseline
        return elem

    def align_children_grid(self, elem: HtmlElement, children: Array2D[HtmlElement], font_size):
        rows = Array1D(children.height, lambda: RowColumnMeta())
        columns = Array1D(children.width, lambda: RowColumnMeta())

        def update_row_column_meta(y, x, item: HtmlElement):
            if item.height > rows[y].height:
                rows[y].height = item.height
            if item.baseline > rows[y].baseline:
                rows[y].baseline = item.baseline
            if item.width > columns[x].width:
                columns[x].width = item.width
        children.for_each_not_none(update_row_column_meta)
        for i in range(0, children.height):
            if i > 0:
                rows[i].y = rows[i-1].y + rows[i-1].height + self.line_margin * font_size
            elem.height = rows[i].y + rows[i].height
        elem.baseline = self.get_baseline(elem.height, font_size)
        for j in range(0, children.width):
            if j > 0:
                columns[j].x = columns[j-1].x + columns[j-1].width + self.cell_margin * font_size
            elem.width = columns[j].x + columns[j].width

        def update_cell_position(y, x, item: HtmlElement):
            item.x = columns[x].x
            item.y = rows[y].y + rows[y].baseline - item.baseline
            elem.children.append(item)
        children.for_each_not_none(update_cell_position)

    def render(self, node: MathTexAST, font_size) -> HtmlElement:
        node.prepare_render()
        if node.node_type == MathTexAST.TEXT_NODE:
            return self.render_text(node.text, font_size)
        if node.node_type == MathTexAST.BLOCK_NODE:
            return self.render_block(node.children, font_size)
        if node.node_type == MathTexAST.CELL_NODE:
            return self.render_block(node.children, font_size)
        if node.node_type == MathTexAST.ENV_NODE:
            return self.render_env(node.children, font_size)
        if node.node_type == MathTexAST.CMD_NODE:
            return self.render_command(node.command, node.children, font_size)
        return HtmlElement(width=0, height=0)

    def render_text(self, text, font_size, middle_align_with=None) -> HtmlElement:
        elem = HtmlElement(width=0, height=self.line_height * font_size)
        if middle_align_with is not None:
            elem.baseline = self.get_baseline(elem.height, middle_align_with)
        else:
            elem.baseline = self.get_baseline(elem.height, font_size)
        for i in range(0, len(text)):
            c = text[i]
            if i > 0:
                elem.width += self.char_margin * font_size
                pre_c = text[i - 1]
                bearing = min(FONT_METRICS.get_glyph(pre_c).right_bearing, FONT_METRICS.get_glyph(c).left_bearing)
                if bearing > 0:
                    elem.width -= bearing * font_size
            child = HtmlElement(x=elem.width, y=0, text=c, font_size=font_size)
            elem.width += FONT_METRICS.get_glyph(c).width * font_size
            elem.children.append(child)
        return elem

    def render_block(self, children: List[MathTexAST], font_size) -> HtmlElement:
        elem = HtmlElement()
        for i in range(0, len(children)):
            child = self.render(children[i], font_size)
            elem.children.append(child)
        self.align_children(elem, font_size)
        return elem

    def render_env(self, lines: List[MathTexAST], font_size) -> HtmlElement:
        elem = HtmlElement()
        children = Array2D()  # type: Array2D[HtmlElement]
        for i in range(0, len(lines)):
            line = lines[i]
            for j in range(0, len(line.children)):
                child = self.render(line.children[j], font_size)
                children.set(i, j, child)
        self.align_children_grid(elem, children, font_size)
        return elem

    def render_command(self, cmd, children: List[MathTexAST], font_size) -> HtmlElement:
        if cmd == MathTexAST.CMD_LEFT_RIGHT:
            return self.render_cmd_left_right(children, font_size)

    def render_cmd_left_right(self, children: List[MathTexAST], font_size) -> HtmlElement:
        middle_item = self.render(children[2], font_size)
        brace_size = middle_item.height / FONT_METRICS.height
        left = children[0].get_first_string()
        right = children[1].get_first_string()
        elem = HtmlElement()
        if len(left) == 1 and left in "([{":
            elem.children.append(self.render_text(left, brace_size, font_size))
        elem.children.append(middle_item)
        if len(right) == 1 and right in ")]}":
            elem.children.append(self.render_text(right, brace_size, font_size))
        self.align_children(elem, font_size)
        return elem
