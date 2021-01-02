'''
Card set generator: 6 cards for each set
All numbers from 1 to 90 must be present in the set
Numbers of a row must be sorted
Each columns must contain number of the same decade
Row: 9 fields ==> 5 numbers, 4 spaces
3 cols
'''

import argparse
import random
from card import Card, CardsSet
from typing import List, Tuple
from copy import deepcopy
from collections import defaultdict

SET_NUMBER: int = 1

def print_sets(sets: List[CardsSet]) -> None:
    for cards_set in sets:
        for card in cards_set:
            print(card.title)
            print(card.content)
        print("")  # Blank line

def generate_set(set_num: int) -> CardsSet:
    cards_set: CardsSet = CardsSet()
    nums: List[List[int]] = list()
    for t in range(0, 9):  # Tens
        nums.append(list())
        for u in range(0, 10):  # Units
            if not t and not u:  # Skip 0
                continue
            nums[t].append(t*10 + u)
        if t == 8:
            nums[8].append(90)
        random.shuffle(nums[t])
    # print(nums)
    for i in range(6):
        card: Card = generate_card(i+1, set_num, nums)
        cards_set.append(card)
    if any(nums):
        exit(1)  # Some error occurred
   # if any(nums):  # Numbers distribution within a set is not perfect, but this way the generation is much faster
   #     last_card: Card = cards_set.pop()
   #     for row_num, row in enumerate(last_card.content):
   #         for col_num, ele in enumerate(row):
   #             if ele != -1:
   #                 nums[col_num].append(ele)
   #     for _ in range(3):
   #         for i in range(9):
   #             nums[i].append(random.randint(10*i, 10*i+9))
   #     for row_num in range(3):
   #         counter: int = 9-last_card.content[row_num].count(-1)
   #         # print(counter)
   #         if row_num%2 == 0:
   #             for col_num, col in enumerate(nums):
   #                 if counter >= 5:
   #                     break
   #                 if len(col) != 0 and last_card.content[row_num][col_num] == -1:
   #                     last_card.content[row_num][col_num] = col.pop()
   #                     counter += 1
   #         else:
   #             for col_num, col in enumerate(nums[::-1]):
   #                 if counter >= 5:
   #                     break
   #                 if len(col) != 0 and last_card.content[row_num][8-col_num] == -1:
   #                     last_card.content[row_num][8-col_num] = col.pop()
   #                     counter += 1
   #     cards_set.append(last_card)
    # print(nums)
    return cards_set

def generate_last_cards(card_num: int, set_num: int, nums: List[List[int]]) -> Card:
    l: List[int] = [-1] * 9
    card_content: List[List[int]] = [deepcopy(l) for _ in range(3)]
    for row in card_content:
        counter: int = 0    
       # if row_num%2 == 0:
       #     for col_num, col in enumerate(nums):
       #         if counter >= 5:
       #             break
       #         if len(col) != 0 and row[col_num] == -1:
       #             row[col_num] = col.pop()
       #             counter += 1
       # else:
       #     for col_num, col in enumerate(nums[::-1]):
       #         if counter >= 5:
       #             break
       #         if len(col) != 0 and row[8-col_num] == -1:
       #             row[8-col_num] = col.pop()
       #             counter += 1
        d: Dict[int, List[int]] = dict()
        for index, ele_l in enumerate(nums):
            d[index] = ele_l
        sorted_key_list: List[int] = sorted(d, key=lambda k: len(d[k]), reverse=True)
        sorted_d: Dict[int, List[int]] = {k: d[k] for k in sorted_key_list}
        # print(sorted_d)
        shuffled_sorted_d = defaultdict(list)
        for k, v in sorted_d.items():
            shuffled_sorted_d[len(v)].append((k, v))
        tmp_l: List[Tuple[int, List[int]]] = list()
        for v in shuffled_sorted_d.values():
            random.shuffle(v)
            for ele in v:
                tmp_l.append(ele)
        shuffled_sorted_d = dict(tmp_l)
        for k, v in shuffled_sorted_d.items():
            if counter >= 5:
                break
            if len(v) != 0 and row[k] == -1:
                    row[k] = v.pop()
                    counter += 1
    card: Card = Card(card_content, f"Cartella {set_num} {card_num}")
    return card


def generate_card(card_num: int, set_num: int, nums: List[List[int]]) -> Card:
    if card_num >= 3:  # If it's ont of the last cards (last four cards) of the set
        # print("generating last cards")
        return generate_last_cards(card_num, set_num, nums)
    number_placement_matrix: List[List[bool]] = generate_number_placement_matrix(nums)
    l: List[int] = [-1] * 9
    card_content: List[List[int]] = [deepcopy(l) for _ in range(3)]
    for row_num, row in enumerate(number_placement_matrix):  # Is this pythonic? I think no
        for col_num, ele in enumerate(row):
            if ele:
                card_content[row_num][col_num] = nums[col_num].pop()
    card: Card = Card(card_content, f"Cartella {set_num} {card_num}")
    return card

def generate_number_placement_matrix(nums: List[List[int]]) -> List[List[bool]]:
    # def is_row_ok(number_placement_matrix_row: List[bool], nums: List[List[int]]) -> bool:
    #    not_empty_cols: List[bool] = [not not len(ele) for ele in nums]
    #    cols_and: List[bool] = [ele1 and ele2 for ele1, ele2 in zip(number_placement_matrix_row, not_empty_cols)]
    #    return cols_and.count(True) >= 5
    cols: int = 9
    nums_on_a_row: int = 5
    rows: int = 3
    matrix: List[List[bool]] = list()
    for r in range(rows):
        matrix.append(list())
        for _ in range(nums_on_a_row):
            matrix[r].append(True)
        for _ in range(cols-nums_on_a_row):
            matrix[r].append(False)
        random.shuffle(matrix[r])
    # print(matrix)
    return matrix


def main(set_number: int) -> None:
    sets: List[CardsSet] = list()
    for i in range(set_number):
        card_set = generate_set(i+1)
        # while card_set is None:
        #    card_set = generate_set(i+1)
        sets.append(card_set)
    print_sets(sets)
    

if __name__ == "__main__":
   parser = argparse.ArgumentParser()
   parser.add_argument("-n", "--number", help="Number of sets to generate", default=SET_NUMBER, type=int, dest="set_number")
   args = parser.parse_args()
   main(args.set_number)


