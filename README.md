# CartellaTombolaPDF
Tombola card pdf generator from html format template

## Setting up
```
pip3 install jinja2
pip3 install pdfkit
sudo apt install wkhtmltopdf
```

## Run the script
```
cat cards_set.txt > python3 pdf_formatter.py
```

OR

Pipe generator output directly into pdf_formatter

```
python3 generator.py | python3 pdf_formatter.py
```

### Arguments
-b  Bottom text
-l  Logo filename

## _cards_set.txt_ sample
Input must be formatted in the following way: [cards_set.txt sample](cards_set.txt)

Formatting rules:
- there must be two lines for each card:
	- the first one is the name of that card inside the set
	- the second one is a Python list containing one list of integers for each row (of that card)
- everything after the last pair of lines will be discarded (odd line)


