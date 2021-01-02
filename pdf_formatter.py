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
import argparse
from PyPDF2 import PdfFileMerger, PdfFileReader

HTML_TEMPLATE_FILENAME: str = "cards_set_template.html"
HTML_FILENAME: str = "cards_set.html"
PDF_FILENAME: str = "cards_set.pdf"
LOGO_FILENAME: str = "logo.jpeg"
BOTTOM_TEXT: str = "test_txt"

#def transpose_matrix(original_matrix: List[List]) -> List[List]:
#    original_matrix_lens: List[int] = [len(col) for col in original_matrix]
#    max_col_len: int = max(original_matrix_lens)
#    for col in original_matrix:
#        if len(col) < max_col_len:
#            col.extend([-1] * (max_col_len - len(col)))
#    transposed_matrix: List[List] = list(zip(*original_matrix))
#    return transposed_matrix

def import_data_from(source: List[str]) -> CardsSet:
    global bottom_text
    cards_set = CardsSet()
    for i, line_pair in enumerate(zip(source, source[1:])):
        if not i%2:
            title: str = line_pair[0]
            if not line_pair[1]:
                continue
            # cols_list: List[List] = ast.literal_eval(line_pair[1])
            # rows_list: List[List] = transpose_matrix(cols_list)
            rows_list: List[List] = ast.literal_eval(line_pair[1])
            cards_set.append(Card(rows_list, title))  # Inside title there are set number and card number
    return cards_set


def main(logo_filename: str, bottom_text: str, template_filename: str) -> None:
    merger = PdfFileMerger()
    counter: int = 0
    while True:
        buf: List[str] = list()
        for line in sys.stdin:
            line: str = line.strip()
            if not line:
                break
            buf.append(line)
        if not buf:
            break
        cards_set: CardsSet = import_data_from(buf)
        
        # Jinja 2 configuration
        template_loader = FileSystemLoader(searchpath="./")  # Place files inside the same directory
        template_env = Environment(loader=template_loader)
        template = template_env.get_template(template_filename)
        with open(HTML_FILENAME, "w") as f:
            text = template.render(cards_set=cards_set, logo_filename=logo_filename, bottom_text=bottom_text, enumerate=enumerate)
            f.write(text)
        
        # pdfkit configuration
        options = {
                "page-size": "A4",
                "enable-local-file-access": None
        }
        pdfkit.from_file(HTML_FILENAME, PDF_FILENAME, options=options)
        with open(PDF_FILENAME, 'rb') as f:
            merger.append(PdfFileReader(f))
        #with open(PDF_FILENAME, "wb") as f:
        #    f.write(pdf_buf)
        counter += 1
        print(f"\t\tPrinted set {counter}")
    merger.write(PDF_FILENAME)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-l", "--logo", help="Logo filename", default=LOGO_FILENAME, type=str, dest="logo_filename")
    parser.add_argument("-b", "--bottomtext", help="Bottom text", default=BOTTOM_TEXT, type=str, dest="bottom_text")
    parser.add_argument("-t", "--template", help="HTML template filename", default=HTML_TEMPLATE_FILENAME, type=str, dest="template_filename")
    args = parser.parse_args()
    main(args.logo_filename, args.bottom_text, args.template_filename)
