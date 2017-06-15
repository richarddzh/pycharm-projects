from mathtex.parser import MathTexParser
from mathtex.htmlrender import HtmlRender

p = MathTexParser()
p.begin_parse()
p.parse_line(r"\begin{array}af\end{array}\alpha fa(g)+b01.23\begin{array}\left\{hM\right]q&b\\&D-c\end{array}")
result = p.end_parse()
print(result)

rd = HtmlRender()
html = rd.render(result, 1)
print(html.to_html())
