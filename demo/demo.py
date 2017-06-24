from mathtex import markdown
from sys import argv

input_file = "test.md"
output_file = "test.html"

if len(argv) > 1:
    input_file = argv[1] + ".md"
    output_file = argv[1] + ".html"

markdown.save_markdown_as_html(input_file, output_file)
