from mathtex.parser import MathTexParser
from mathtex.htmlrender import HtmlRender

p = MathTexParser()
p.begin_parse()
p.parse_line(r"\begin{array}af\end{array}_{\left\{i^2+j^2\right\}}"
             r"^{\left(\begin{array}m+n\\hello\end{array}\right]}"
             r"\alpha fa(g)^{\begin{array}up\\down&Down\end{array}}"
             r"+b01.23"
             r"\left\{\begin{array}"
             r"\left\{hM\right]q&b\\"
             r"&D-c\\bla&bla"
             r"\end{array}\right)")
result = p.end_parse()
print(result)

rd = HtmlRender()
html = rd.render(result, 1)
print(html.to_html())
