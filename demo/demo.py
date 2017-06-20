from mathtex.parser import MathTexParser
from mathtex.htmlrender import HtmlRender

p = MathTexParser()
p.begin_parse()
p.parse_line(r"\left[\begin{array}{ccc}\sin af+\frac{1}{22}\end{array}_{\left\{i_2+j^2\right\}}"
             r"^{\left(\begin{array}m+n\\hello\end{array}\right]}"
             r"\cos\alpha fa(g)^{\begin{array}up\\down&Down\end{array}}"
             r"+b01.23^{\frac{1+e^x}{e^x-1}}"
             r"\left\{\begin{array}{lr}"
             r"\left\{hM\right]q&b\\"
             r"&D-c\\bla&bla"
             r"\end{array}\right)\right]")
result = p.end_parse()
print(result)

rd = HtmlRender()
html = rd.render(result, 1)
print(html.to_html_div())
