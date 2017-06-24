import markdown
from mathtex.mdextension import MathTexExtension

HTML_HEADER = '''<!DOCTYPE html>
<html>
<head>
<meta http-equiv="content-type" content="application/xhtml+xml; charset=UTF-8">
<style>
.math {
    display: inline-block;
    position: relative;
    padding: 0;
    margin: 0;
}
.math div {
    position: absolute;
    padding: 0;
    margin: 0;
    font-family: "Lucida Sans Unicode";
}
.math .italic {
    font-style: italic;
}
.math .bold {
    font-weight: bold;
}
.math .hline {
    border-top: 0.14ex solid;
}
.math .left-bracket, .math .left-bracket-rounded {
    border-left: 0.14ex solid;
    border-top: 0.1ex solid;
    border-bottom: 0.1ex solid;
    width: 0.25em;
}
.math .right-bracket, .math .right-bracket-rounded {
    border-right: 0.14ex solid;
    border-top: 0.1ex solid;
    border-bottom: 0.1ex solid;
    width: 0.25em;
}
.math .left-bracket-rounded {
    border-top-left-radius: 0.5em 100%;
    border-bottom-left-radius: 0.5em 100%;
}
.math .right-bracket-rounded {
    border-top-right-radius: 0.5em 100%;
    border-bottom-right-radius: 0.5em 100%;
}
.math .left-brace0, .math .right-brace2 {
    border-left: 0.14ex solid;
    border-top: 0.1ex solid;
    border-top-left-radius: 0.5em 1ex;
    width: 0.25em;
}
.math .left-brace1, .math .right-brace3 {
    border-right: 0.14ex solid;
    border-bottom: 0.1ex solid;
    border-bottom-right-radius: 0.5em 1ex;
    width: 0.25em;
}
.math .left-brace2, .math .right-brace0 {
    border-right: 0.14ex solid;
    border-top: 0.1ex solid;
    border-top-right-radius: 0.5em 1ex;
    width: 0.25em;
}
.math .left-brace3, .math .right-brace1 {
    border-left: 0.14ex solid;
    border-bottom: 0.1ex solid;
    border-bottom-left-radius: 0.5em 1ex;
    width: 0.25em;
}
.math .sqrt1 {
    border-right: 0.14ex solid;
    border-bottom: 0.14ex solid;
    border-bottom-right-radius: 100%;
}
.math .sqrt2 {
    border-right: 0.14ex solid;
    border-top: 0.14ex solid;
    border-top-right-radius: 100%;
}
</style>
</head>
<body>
'''

HTML_FOOTER = "</body></html>"


def parse_markdown(text: str) -> str:
    return HTML_HEADER + markdown.markdown(text, extensions=[MathTexExtension()]) + HTML_FOOTER


def parse_markdown_file(filename: str) -> str:
    with open(filename, "r", encoding="utf8") as file:
        text = file.read()
    return parse_markdown(text)


def save_markdown_as_html(file_in: str, file_out: str):
    html = parse_markdown_file(file_in)
    with open(file_out, "w", encoding="utf8") as file:
        file.write(html)
