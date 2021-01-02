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
        self.id: int = self.__get_number(self.title, 2)
        self.set_id: int = self.__get_number(self.title, 1)

    def __get_number(self, s: str, pos: int) -> int:
        l = s.split()
        if l[pos].isdigit():
            return int(l[pos])

class CardsSet(list):
    pass
