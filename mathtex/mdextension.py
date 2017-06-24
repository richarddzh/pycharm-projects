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

    def handleMatch(self, m):
        parser = MathTexParser()
        parser.begin_parse()
        parser.parse_line(m.group(3))
        result = parser.end_parse()
        render = HtmlRender()
        html = render.render(result, 1)
        return html.to_html_div()


class MathTexExtension(Extension):
    def extendMarkdown(self, md, md_globals):
        md.inlinePatterns.add('MathTex', MathTexInlinePattern(), '_begin')
