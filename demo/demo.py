from mathtex.parser import MathTexParser
from mathtex.fontmetric import FONT_METRICS

p = MathTexParser()
p.begin_parse()
p.parse_line(r"a+b_{\alpha+\Sigma}^{\frac{e}{1+2}}\begin{array}a&b\\c&d\end{array}")
result = p.end_parse()
print(result)
