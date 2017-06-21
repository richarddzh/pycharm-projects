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
            if child.baseline > elem.baseline:
                elem.baseline = child.baseline
            elem.width += child.width
        for child in elem.children:
            child.y = elem.baseline - child.baseline
            if child.y + child.height > elem.height:
                elem.height = child.y + child.height
        return elem

    def align_children_grid(self, elem: HtmlElement, children: Array2D[HtmlElement], font_size):
        rows = Array1D(children.height, lambda: RowColumnMeta())
        columns = Array1D(children.width, lambda: RowColumnMeta())

        def update_row_column_meta1(y, x, item: HtmlElement):
            if item.baseline > rows[y].baseline:
                rows[y].baseline = item.baseline
            if item.width > columns[x].width:
                columns[x].width = item.width

        def update_row_column_meta2(y, _, item: HtmlElement):
            y_offset = rows[y].baseline - item.baseline
            new_height = y_offset + item.height
            if new_height > rows[y].height:
                rows[y].height = new_height

        children.for_each_not_none(update_row_column_meta1)
        children.for_each_not_none(update_row_column_meta2)
        for i in range(0, children.height):
            if i > 0:
                rows[i].y = rows[i-1].y + rows[i-1].height + self.line_margin * font_size
            elem.height = rows[i].y + rows[i].height
        elem.update_baseline(font_size)
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

    def render_text(self, text, font_size, middle_align_with=None, italic=True, bold=False) -> HtmlElement:
        elem = HtmlElement(width=0, height=self.line_height * font_size)
        if middle_align_with is not None:
            elem.update_baseline(middle_align_with)
        else:
            elem.update_baseline(font_size)
        for i in range(0, len(text)):
            c = text[i]
            if i > 0:
                elem.width += self.char_margin * font_size
                pre_c = text[i - 1]
                bearing = min(FONT_METRICS.get_glyph(pre_c).right_bearing, FONT_METRICS.get_glyph(c).left_bearing)
                if bearing > 0:
                    elem.width -= bearing * font_size
            css_class = "bold" if bold else None
            if c.isalpha() and italic:
                css_class = "bold italic" if bold else "italic"
            child = HtmlElement(x=elem.width, y=0, text=c, font_size=font_size, css_class=css_class)
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
        if cmd == MathTexAST.CMD_SUB_SUP:
            return self.render_cmd_sub_sup(children, font_size)
        if cmd == "frac":
            return self.render_cmd_fraction(children, font_size)
        return self.render_text(cmd, font_size, italic=False)

    def render_cmd_left_right(self, children: List[MathTexAST], font_size) -> HtmlElement:
        middle_item = self.render(children[2], font_size)
        brace_size = middle_item.height / FONT_METRICS.height
        left = children[0].get_first_string()
        right = children[1].get_first_string()
        elem = HtmlElement()
        if len(left) == 1 and left in "([{":
            if brace_size <= 1:
                elem.children.append(self.render_text(left, brace_size, font_size))
            else:
                elem.children.append(HtmlElement.create_brace(
                    left, middle_item.height, middle_item.baseline, font_size))
        elem.children.append(middle_item)
        if len(right) == 1 and right in ")]}":
            if brace_size <= 1:
                elem.children.append(self.render_text(right, brace_size, font_size))
            else:
                elem.children.append(HtmlElement.create_brace(
                    right, middle_item.height, middle_item.baseline, font_size))
        self.align_children(elem, font_size)
        return elem

    def render_cmd_sub_sup(self, children: List[MathTexAST], font_size) -> HtmlElement:
        elem = HtmlElement()
        main_item = self.render(children[0], font_size)
        elem.children.append(main_item)
        elem.width = main_item.width
        elem.height = main_item.height
        elem.baseline = main_item.baseline
        sub_size = (font_size + 3) / 5
        if children[1] is not None:
            sub_item = self.render(children[1], sub_size)
            sub_item.x = main_item.width + sub_size * self.char_margin
            elem.children.append(sub_item)
            elem.width = sub_item.x + sub_item.width
            if sub_item.height > main_item.height / 2:
                main_item.y = sub_item.height - main_item.height / 2
                elem.baseline += main_item.y
                elem.height += main_item.y
        if children[2] is not None:
            sup_item = self.render(children[2], sub_size)
            sup_item.x = main_item.width + sub_size * self.char_margin
            elem.children.append(sup_item)
            elem.width = max(elem.width, sup_item.x + sup_item.width)
            delta = sup_item.height - main_item.height / 2
            if delta <= 0:
                sup_item.y = main_item.y + main_item.height / 2 - delta
            else:
                sup_item.y = main_item.y + main_item.height / 2
                elem.height += delta
        return elem

    def render_cmd_fraction(self, children: List[MathTexAST], font_size) -> HtmlElement:
        elem = HtmlElement()
        up_item = self.render(children[0], font_size)
        down_item = self.render(children[1], font_size)
        elem.width = max(up_item.width, down_item.width) + font_size / 2
        elem.height = up_item.height + down_item.height + self.line_margin * font_size
        elem.update_baseline(font_size, pseudo_height=up_item.height * 2 + self.line_margin * font_size)
        up_item.x = (elem.width - up_item.width) / 2
        down_item.x = (elem.width - down_item.width) / 2
        down_item.y = elem.height - down_item.height
        line = HtmlElement.create_horizontal_line(
            font_size / 8,
            up_item.height + self.line_margin * font_size / 2,
            elem.width - font_size / 4)
        elem.children = [up_item, down_item, line]
        return elem
