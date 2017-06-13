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
        self.children = []  # type: List[HtmlElement]

    def to_html(self, offset_x=0, offset_y=0) -> str:
        if len(self.children) > 0:
            lines = []
            for child in self.children:
                line = child.to_html(self.x + offset_x, self.y + offset_y)
                if len(line) > 0:
                    lines.append(line)
            return '\n'.join(lines)
        if self.text is None and self.css_class is None:
            return ""
        html_text = "" if self.text is None else self.text
        html_pos = "left:{0}em;top:{1}em;".format(self.x + offset_x, self.y + offset_y)
        html_width = "" if self.width is None else "width:{0}em;".format(self.width)
        html_height = "" if self.height is None else "height:{0}em;".format(self.height)
        html_font_size = "" if self.font_size == 1 else "font-size:{0}em;".format(self.font_size)
        html_class = "" if self.css_class is None else ' class="{0}"'.format(self.css_class)
        return '<{0} style="{1}"{2}>{3}</{0}>'.format(
            self.name, html_pos + html_width + html_height + html_font_size, html_class, html_text)


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

    def render(self, node: MathTexAST, font_size) -> HtmlElement:
        if node.node_type == MathTexAST.TEXT_NODE:
            return self.render_text(node.text, font_size)
        if node.node_type == MathTexAST.BLOCK_NODE:
            return self.render_block(node.children, font_size)
        if node.node_type == MathTexAST.CELL_NODE:
            return self.render_block(node.children, font_size)
        if node.node_type == MathTexAST.ENV_NODE:
            return self.render_env(node.children, font_size)

    def render_text(self, text, font_size) -> HtmlElement:
        elem = HtmlElement()
        elem.width = 0
        elem.height = self.line_height * font_size
        elem.baseline = self.get_baseline(elem.height, font_size)
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

    def render_env(self, lines, font_size) -> HtmlElement:
        env_elem = HtmlElement()
        env_elem.width = 0
        env_elem.height = 0
        env_elem.baseline = 0
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
                elem = self.render(line.children[j], font_size)
                a2d.set(i, j, elem)
                if elem.height >= rows[i].height:
                    rows[i].height = elem.height
                if elem.baseline >= rows[i].baseline:
                    rows[i].baseline = elem.baseline
                if elem.width >= columns[j].width:
                    columns[j].width = elem.width
            env_elem.height = rows[i].y + rows[i].height
        for j in range(0, len(columns)):
            if j > 0:
                columns[j].x = columns[j-1].x + columns[j-1].width + self.cell_margin * font_size
            env_elem.width = columns[j].x + columns[j].width
        env_elem.baseline = self.get_baseline(env_elem.height, font_size)
        for i in range(0, len(lines)):
            line = lines[i]  # type: MathTexAST
            for j in range(0, len(line.children)):
                elem = a2d.get(i, j)  # type: HtmlElement
                elem.x = columns[j].x
                elem.y = rows[i].y + elem.baseline - rows[i].baseline
                env_elem.children.append(elem)
        return env_elem


