from mathtex.parser import MathTexParser
from mathtex.htmlrender import HtmlRender

p = MathTexParser()
p.begin_parse()
p.parse_line(r"\sqrt{\left[1+e^x\right\}}+"
             r"\frac{1}{\sqrt{\frac{\sqrt{1}}{2}}}")
result = p.end_parse()
print(result)

rd = HtmlRender()
html = rd.render(result, 1)
print(html.to_html_div())
