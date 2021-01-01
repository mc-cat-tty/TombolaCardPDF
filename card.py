'''
Module containing needed data structures:
- class Card and some method for its management
- class CardsSet
'''

from typing import List

class Card:
    def __init__(self, row_list: List[List], title: str) -> None:
        self.content: List[List] = row_list
        self.title: str = title
        self.id: int = self.__get_number(self.title)

    def __get_number(self, s: str) -> int:
        for n in s.split():
            if n.isdigit():
                return int(n)

class CardsSet(list):
    pass
