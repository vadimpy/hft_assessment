from dataclasses import dataclass
from copy import deepcopy
from typing import Optional

@dataclass
class WordPlace:
    i: int
    j: int
    l: int
    h: bool

@dataclass
class StackRecursionFrame:
    pattern: list[list[str]]
    depth: int
    word_places: list[WordPlace]
    word_used: list[bool]

    def __str__(self):
        res = ''
        for l in self.pattern:
            res += ''.join(l)
            res += '\n'
        res += f'depth = {self.depth}, words used = {sum(self.word_used)}'

        return res
        

def get_vertical_word_len(pattern: list[str], i: int, j: int) -> int:
    res = 0
    for k in range(i, len(pattern)):
        if pattern[k][j] == '*':
            res += 1
        else:
            break
    return res

def get_horizontal_word_len(pattern: list[str], i: int, j: int) -> int:
    res = 0
    for k in range(j, len(pattern[0])):
        if pattern[i][k] == '*':
            res += 1
        else:
            break
    return res

def get_word_places(pattern: list[str]) -> list[WordPlace]:
    word_places = []

    # get horizontal positions
    for i in range(len(pattern)):
        j = 0
        while j < len(pattern[0]):
            l = get_horizontal_word_len(pattern, i, j)
            if l > 0:
                word_places.append(WordPlace(i, j, l, True))
            j += l + 1

    # get vertical positions
    for j in range(len(pattern[0])):
        i = 0
        while i < len(pattern):
            l = get_vertical_word_len(pattern, i, j)
            if l > 0:
                word_places.append(WordPlace(i, j, l, False))
            i += l + 1

    return word_places

def match_word(word: str, pattern: list[list[str]], word_place: WordPlace):
    if len(word) != word_place.l:
        return False

    if word_place.h:
        for word_j, pattern_j in enumerate(range(word_place.j, word_place.j + word_place.l)):
            word_ch = word[word_j]
            pattern_ch = pattern[word_place.i][pattern_j]
            if word_ch != pattern_ch and pattern_ch != '*':
                return False
        return True
    else:
        for word_j, pattern_i in enumerate(range(word_place.i, word_place.i + word_place.l)):
            word_ch = word[word_j]
            pattern_ch = pattern[pattern_i][word_place.j]
            if word_ch != pattern_ch and pattern_ch != '*':
                return False
        return True

def insert_word(word: str, pattern: list[list[str]], word_place: WordPlace):
    if word_place.h:
        for word_j, pattern_j in enumerate(range(word_place.j, word_place.j + word_place.l)):
            pattern[word_place.i][pattern_j] = word[word_j]
    else:
        for word_j, pattern_i in enumerate(range(word_place.i, word_place.i + word_place.l)):
            pattern[pattern_i][word_place.j] = word[word_j]

def solve(word_list: list[str], pattern: list[list[str]], word_places: list[WordPlace]) -> Optional[list[list[str]]]:
    word_len_map = dict()
    depth = 0
    stack = []
    words_amt = len(word_list)
    word_used = [False for _ in range(words_amt)]

    for i, word in enumerate(word_list):
        if len(word) not in word_len_map:
            word_len_map[len(word)] = [i]
        else:
            word_len_map[len(word)].append(i)

    for k, word_place in enumerate(word_places):
        if word_place.l in word_len_map:
            for i in word_len_map[word_place.l]:
                word = word_list[i]
                stack_frame = deepcopy(StackRecursionFrame(pattern, depth + 1, word_places, word_used))
                insert_word(word, stack_frame.pattern, word_place)
                stack_frame.word_places.pop(k)
                stack_frame.word_used[i] = True
                stack.append(stack_frame)

    while stack:
        stack_frame = stack.pop()
        depth = stack_frame.depth
        if depth == words_amt:
            return stack_frame.pattern
 
        pattern = stack_frame.pattern
        word_places = stack_frame.word_places
        word_used = stack_frame.word_used
        for k, word_place in enumerate(word_places):
            if word_place.l in word_len_map:
                for i in word_len_map[word_place.l]:
                    word = word_list[i]
                    if not word_used[i] and match_word(word, pattern, word_place):
                        stack_frame = deepcopy(StackRecursionFrame(pattern, depth + 1, word_places, word_used))
                        stack_frame.word_places.pop(k)
                        insert_word(word, stack_frame.pattern, word_place)
                        stack_frame.word_used[i] = True
                        stack.append(stack_frame)

    return None


def main():
    with open('input.txt') as f:
        pattern = []
        line = f.readline()
        while line != '\n':
            pattern.append(line.rstrip())
            line = f.readline()
        words = f.readline().split()

    word_places = get_word_places(pattern)
    pattern = [list(row) for row in pattern]

    res = solve(words, pattern, word_places)
    if res:
        for l in res:
            print(''.join(l))
    else:
        print("NO!")

if __name__ == '__main__':
    main()
