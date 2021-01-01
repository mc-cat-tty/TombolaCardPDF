'''
Card pdf formatter (from html template)
Pipe input into the script
'''

import sys
import pdfkit
import ast
from jinja2 import Template, Environment, FileSystemLoader
from card import Card, CardsSet
from typing import List

HTML_TEMPLATE_FILENAME: str = "cards_set_template.html"
HTML_FILENAME: str = "cards_set.html"
PDF_FILENAME: str = "cards_set.pdf"
LOGO_FILENAME: str = "logo.jpeg"
BOTTOM_TEXT: str = "test_txt"

def transpose_matrix(original_matrix: List[List]) -> List[List]:
    original_matrix_lens: List[int] = [len(col) for col in original_matrix]
    max_col_len: int = max(original_matrix_lens)
    for col in original_matrix:
        if len(col) < max_col_len:
            col.extend([-1] * (max_col_len - len(col)))
    transposed_matrix: List[List] = list(zip(*original_matrix))
    return transposed_matrix

def import_data_from(source: List[str]) -> CardsSet:
    global bottom_text
    cards_set = CardsSet()
    for i, line_pair in enumerate(zip(source, source[1:])):
        if not i%2:
            title: str = line_pair[0]
            if not line_pair[1]:
                continue
            cols_list: List[List] = ast.literal_eval(line_pair[1])
            rows_list: List[List] = transpose_matrix(cols_list)
            cards_set.append(Card(rows_list, title))
    return cards_set


def main() -> None:
    buf: List[str] = list()
    for line in sys.stdin:
        buf.append(line.strip())
    cards_set: CardsSet = import_data_from(buf)
    
    # Jinja 2 configuration
    template_loader = FileSystemLoader(searchpath="./")  # Place files inside the same directory
    template_env = Environment(loader=template_loader)
    template = template_env.get_template(HTML_TEMPLATE_FILENAME)
    with open(HTML_FILENAME, "w") as f:
        text = template.render(cards_set=cards_set, logo_filename=LOGO_FILENAME, bottom_text=BOTTOM_TEXT, enumerate=enumerate)
        f.write(text)
    
    # pdfkit configuration
    options = {
            "page-size": "A4",
            "enable-local-file-access": None
    }
    pdfkit.from_file(HTML_FILENAME, PDF_FILENAME, options=options)

if __name__ == "__main__":
    main()
