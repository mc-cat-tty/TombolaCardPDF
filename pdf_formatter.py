'''
Card pdf formatter (from html template)
Pipe input into the script
'''

import pdfkit
from jinja2 import Template, Environment, FileSystemLoader
from card import Card, CardsSet

HTML_TEMPLATE_FILENAME = "card_template.html"
HTML_FILENAME = "card.html"
PDF_FILENAME = "card.pdf"

def transpose_matrix(original_matrix: List[List]) -> List[List]:
    transposed_matrix: List[List] = 
    return transposed_matrix

def import_data_from(source) -> CardsSet:
    cards_set = CardsSet()
    for i, line_pair in enumerate(zip(source, source[1:])):
        if not i%2:
            title: str = line_pair[0]
            cols_list: List[List] = list(line_pair[1])
            rows_list: List[List] = transpose_matrix(cols_list)
            cards_set.append(Card(title, rows_list))
    return cards_set


def main() -> None:
    buf: str = ""
    for line in sys.stdin:
        buf += line
    cards_set: CardsSet = import_data_from(buf)
    print(cards_set)
    template_loader = FileSystemLoader(searchpath="./")  # Place files inside the same directory
    template_env = Environment(loader=template_loader)
    template = template_env.get_template(HTML_TEMPLATE_FILENAME)
    with open(HTML_FILENAME, "w") as f:
        text = template.render(name="Cartella 1.1", cartella=[[1.2], [2,2]])
        f.write(text)
    pdfkit.from_file(HTML_FILENAME, PDF_FILENAME)

if __name__ == "__main__":
    main()
