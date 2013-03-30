#!/usr/bin/env python3

import logging
import os
import re
import string
import sys

from collections import defaultdict

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)
log.addHandler(logging.StreamHandler())

DICTIONARY_FILE = "./words"
assert os.path.exists(DICTIONARY_FILE)

VALID_WORD_RE = re.compile('^[' + string.ascii_letters + ']+$', re.I)

class WordMatrixSolver:
    """
    Solves for an NxN matrix of words where every row is a valid word
    and every column is a valid word.
    """
    def __init__(self, dimension):
        self.dimension = dimension
        self.words = set()
        log.debug("Reading dictionary %s" % DICTIONARY_FILE)
        with open(DICTIONARY_FILE, 'r') as dictionary:
            for line in dictionary:
                word = line.strip().upper()
                if len(word) == dimension and VALID_WORD_RE.match(word):
                    self.words.add(word)

        log.info("Loaded %d %d-letter words." % (len(self.words), dimension))

        # create a mapping of prefix -> set of words with given prefix
        self.prefixes = defaultdict(set)
        r = range(1, dimension + 1)
        for word in self.words:
            for i in r:
                prefix = word[:i]
                self.prefixes[prefix].add(word)

    def solve_for_word(self, first_row_word, phase=None):
        """
        Find a solution using `first_row_word` in the first row.
        Arguments:
            first_row_word - The word to start with in the first row.
            pahse - A value of 1 causes algorithm to only evaluate solutions
                    with `first_row_word` in the first column.  A value of 2 will
                    cause all possible solutions to be evaluated.
        """
        words, prefixes, d = self.words, self.prefixes, self.dimension
        r = range(1, d)

        def try_first_column_word(column_word):
            result = [first_row_word]
            for i in r: # loop over rows to fill in words
                i_range = range(i + 1) # stupid optimization, memoize
                for crossword in prefixes[column_word[i]]:
                    result.append(crossword)
                    for j in r:
                        # Heuristic: Loop through each column and short-circuit
                        # if any prefix doesnt have possible words
                        prefix = ''.join([result[k][j] for k in i_range])
                        if len(prefix) == d and prefix not in words:
                            break # no words start with this column's prefix
                        elif prefix not in prefixes:
                            break # no words start with this column's prefix
                    else: # all columns have valid prefix, crossword is good (so far)
                        break
                    result.pop()
                else: # no valid crosswords for column word
                    break
                if len(result) < i:
                    break
            else:
                return result

        if phase == 1 or phase is None:
            # Heuristic: Attempt to use the same word from the first row
            # in the first column.
            result = try_first_column_word(first_row_word)
            if result is not None:
                return result
        if phase == 2 or phase is None:
            # Outter loop fills in the first column, guessing and backtracking
            for column_word in prefixes[first_row_word[0]]:
                if column_word is first_row_word:
                    continue
                result = try_first_column_word(column_word)
                if result is not None:
                    return result


    def solve(self):
        log.debug("Starting solver")
        solve_for_word = self.solve_for_word
        # phase 1 - Try using the same word down and across in the
        #           first row/column
        for word in self.words:
            result = solve_for_word(word, phase=1)
            if result is not None:
                log.debug("Finished in phase 1")
                return result

        # phase 2 - Try all other combinations
        for word in self.words:
            result = solve_for_word(word, phase=2)
            if result is not None:
                log.debug("Finished in phase 2")
                return result


if __name__ == "__main__":
    try:
        n = int(sys.argv[1])
    except (IndexError, ValueError):
        n = 5

    wm = WordMatrixSolver(n)
    result = wm.solve()
    print('\n'.join(' '.join(row) for row in result) if result else 'No Solution')
