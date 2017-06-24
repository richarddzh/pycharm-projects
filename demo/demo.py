from markdown import markdown
from mathtex.mdextension import MathTexExtension

with open(r"C:\d\github\pycharm-projects\test.md", "r", encoding="utf8") as input_file:
    text = input_file.read()

md = markdown(text, extensions=[MathTexExtension()])
print(md)
