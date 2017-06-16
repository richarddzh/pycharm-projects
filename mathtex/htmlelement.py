from typing import List


class HtmlElement:
    def __init__(self, x=0, y=0, width=None, height=None, font_size=1, text=None):
        self.name = "div"
        self.x = x  # x-offset relative to parent
        self.y = y  # y-offset relative to parent
        self.width = width  # element width
        self.height = height  # element height
        self.baseline = 0  # baseline relative to element top
        self.font_size = font_size  # font-size relative to 1em
        self.css_class = None
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
        html_pos = "left:{0}em;top:{1}em;".format(self.x + offset_x, self.y + offset_y)
        html_width = "" if self.width is None else "width:{0}em;".format(self.width)
        html_height = "" if self.height is None else "height:{0}em;".format(self.height)
        html_font_size = "" if self.font_size == 1 else "font-size:{0}em;".format(self.font_size)
        html_class = "" if self.css_class is None else ' class="{0}"'.format(self.css_class)
        return '<{0} style="{1}"{2}>{3}</{0}>'.format(
            self.name, html_pos + html_width + html_height + html_font_size, html_class, html_text)
