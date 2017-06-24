from markdown.extensions import Extension
from markdown.inlinepatterns import Pattern
from markdown.util import etree
from markdown.util import AtomicString
from mathtex.parser import MathTexParser
from mathtex.htmlrender import HtmlRender
from mathtex.htmlelement import HtmlElement
from typing import List

MATH_TEX_INLINE_REG_PATTERN = r"\$([^$]+)\$"


class MathTexInlinePattern(Pattern):
    def __init__(self):
        super(MathTexInlinePattern, self).__init__(MATH_TEX_INLINE_REG_PATTERN)

    @staticmethod
    def get_elements(node: HtmlElement, offset_x=0, offset_y=0) -> List[etree.Element]:
        if len(node.children) > 0:
            elements = []
            for child in node.children:
                elements += MathTexInlinePattern.get_elements(child, node.x + offset_x, node.y + offset_y)
            return elements
        if node.text is None and node.css_class is None:
            return []
        elem = etree.Element(node.name)
        if node.text is not None:
            elem.text = AtomicString(node.text)
        if node.css_class is not None:
            elem.attrib["class"] = node.css_class
        html_pos = "left:{0}em;top:{1}em;".format(
            (node.x + offset_x) / node.font_size,
            (node.y + offset_y) / node.font_size)
        html_width = "" if node.width is None else "width:{0}em;".format(node.width)
        html_height = "" if node.height is None else "height:{0}em;".format(node.height)
        html_font_size = "" if node.font_size == 1 else "font-size:{0}em;".format(node.font_size)
        elem.attrib["style"] = html_pos + html_width + html_height + html_font_size
        return [elem]

    @staticmethod
    def get_element(node: HtmlElement) -> etree.Element:
        elem = etree.Element("div")
        elem.attrib["class"] = "math"
        elem.attrib["style"] = 'width:{0}em;height:{1}em;vertical-align:{2}em;'.format(
            node.width,
            node.height,
            node.baseline - node.height)
        children = MathTexInlinePattern.get_elements(node)
        elem.extend(children)
        return elem

    def handleMatch(self, m):
        parser = MathTexParser()
        parser.begin_parse()
        parser.parse_line(m.group(2))
        result = parser.end_parse()
        render = HtmlRender()
        html = render.render(result, 1)
        return MathTexInlinePattern.get_element(html)


class MathTexExtension(Extension):
    def extendMarkdown(self, md, md_globals):
        md.inlinePatterns.add('MathTex', MathTexInlinePattern(), '_begin')
