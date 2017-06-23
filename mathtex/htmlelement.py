from mathtex.fontmetric import FONT_METRICS
from typing import List


class HtmlElement:
    def __init__(self, x=0.0, y=0.0, width=None, height=None, baseline=0, font_size=1, text=None, css_class=None):
        self.name = "div"
        self.x = x  # x-offset relative to parent
        self.y = y  # y-offset relative to parent
        self.width = width  # element width
        self.height = height  # element height
        self.baseline = baseline  # baseline relative to element top
        self.font_size = font_size  # font-size relative to 1em
        self.css_class = css_class
        self.text = text
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
        html_pos = "left:{0}em;top:{1}em;".format(
            (self.x + offset_x) / self.font_size,
            (self.y + offset_y) / self.font_size)
        html_width = "" if self.width is None else "width:{0}em;".format(self.width)
        html_height = "" if self.height is None else "height:{0}em;".format(self.height)
        html_font_size = "" if self.font_size == 1 else "font-size:{0}em;".format(self.font_size)
        html_class = "" if self.css_class is None else ' class="{0}"'.format(self.css_class)
        return '<{0} style="{1}"{2}>{3}</{0}>'.format(
            self.name, html_pos + html_width + html_height + html_font_size, html_class, html_text)

    def to_html_div(self) -> str:
        inner_html = self.to_html()
        begin_div = '<div class="math" style="width:{0}em;height:{1}em;vertical-align:{2}em;">'.format(
            self.width,
            self.height,
            self.baseline - self.height)
        lines = [begin_div, inner_html, "</div>"]
        return '\n'.join(lines)

    def update_baseline(self, font_size, pseudo_height=None):
        if pseudo_height is None:
            pseudo_height = self.height
        self.baseline = (pseudo_height - FONT_METRICS.height * font_size) / 2 + FONT_METRICS.baseline * font_size

    @staticmethod
    def create_brace(brace, brace_size, brace_baseline, font_size):
        is_left = brace in "([{"
        sides = "left" if is_left else "right"
        rounded = "-rounded" if brace in "()" else ""
        height = brace_size - font_size / 4
        baseline = brace_baseline - font_size / 8
        if brace in "([])":
            elem = HtmlElement(width=0.25, height=height, baseline=baseline)
            item = HtmlElement()
            item.css_class = "{0}-bracket{1}".format(sides, rounded)
            item.height = height
            elem.children.append(item)
            return elem
        elif brace in "{}":
            elem = HtmlElement(width=0.5, height=height, baseline=baseline)
            x_left = [1, 0, 0, 1]
            x_right = [0, 1, 1, 0]
            for i in range(4):
                item = HtmlElement()
                item.css_class = "{0}-brace{1}".format(sides, i)
                item.y = i / 4 * height
                item.x = (x_left[i] if is_left else x_right[i]) * 0.25
                item.height = height / 4
                elem.children.append(item)
            return elem

    @staticmethod
    def create_horizontal_line(x, y, width):
        return HtmlElement(x=x, y=y, width=width, css_class="hline")

    @staticmethod
    def create_square_root_group(width, height, font_size):
        line = HtmlElement.create_horizontal_line(0.3 * font_size, 0.1 * font_size, width - 0.5 * font_size)
        root1 = HtmlElement(x=0.1 * font_size,
                            y=line.y,
                            width=0.2 * font_size,
                            height=height - 0.3 * font_size,
                            css_class="sqrt1")
        root2 = HtmlElement(x=0,
                            y=line.y + 0.6 * height,
                            width=0.1 * font_size,
                            height=0.4 * height - 0.3 * font_size,
                            css_class="sqrt2")
        return [line, root1, root2]
