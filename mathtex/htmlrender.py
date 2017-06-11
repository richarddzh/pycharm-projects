from mathtex.astree import MathTexAST
from mathtex.fontmetric import FONT_METRICS

class HtmlElement:
    def __init__(self):
        self.name = "div"
        self.x = 0
        self.y = 0
        self.width = None
        self.height = None
        self.baseline = None
        self.css_class = None
        self.text = None
        self.children = []

class HtmlRender:
    def __init__(self):
        self.html_elements = []
        self.char_margin = 0
        self.line_height = FONT_METRICS.height

    def render(self, node: MathTexAST):
        if node.node_type == MathTexAST.TEXT_NODE:
            self.render_text(node.text)

    def render_text(self, text) -> HtmlElement:
        elem = HtmlElement()
        elem.width = 0
        elem.height = self.line_height
        elem.baseline = (self.line_height - FONT_METRICS.height) / 2 + FONT_METRICS.baseline
        for i in range(0, len(text)):
            if i > 0:
                elem.width += self.char_margin
            c = text[i]
            child = HtmlElement()
            child.x = elem.width
            child.y = 0
            child.text = c
            elem.width += FONT_METRICS.get_glyph(c).width
            elem.children.append(child)
        return elem
