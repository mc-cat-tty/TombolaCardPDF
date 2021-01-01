'''
Cartella pdf formatter (from html template)
'''

import pdfkit
from jinja2 import Template, Environment, FileSystemLoader

HTML_TEMPLATE_FILENAME = "cartella_template.html"
HTML_FILENAME = "cartella.html"
PDF_FILENAME = "cartella.pdf"

def main() -> None:
    template_loader = FileSystemLoader(searchpath="./")  # Place files inside the same directory
    template_env = Environment(loader=template_loader)
    template = template_env.get_template(HTML_TEMPLATE_FILENAME)
    with open(HTML_FILENAME, "w") as f:
        text = template.render()
        f.write(text)
    pdfkitfron_file(HTML_FILENAME, PDF_FILENAME)

if __name__ == "__main__":
    main()
