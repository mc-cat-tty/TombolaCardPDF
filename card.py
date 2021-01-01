'''
Module containing class Card and some method for its management
'''

from typing import List

class Card:
    def __init__(self, row_list: List[List], title: str):
        self.content: List[List] = row_list
        self.title: str = title 

class CardsSet(list):
    pass
