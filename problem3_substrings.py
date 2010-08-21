#! /usr/bin/env python2.6
# Copyright (c) 2010 Mark Kohler
"""Rackspace Test, Problem 3, Substrings.

Tested with Python 2.6.

Performance Notes

This solution uses a dynamic programming algorithm, checking each character of
one string against each character of the other. Its runtime performance is
O(len(str1) * len(str2)).

To save memory, this implemention only saves the non-zero values of the
current and previous rows of the dynamic programming matrix. Thus, in the
worst case, where the strings of similar length and have a long common
substring, the memory use will be roughly twice the combined length of the
strings.

Much greater performance can be achieved by using a generalized suffix tree
instead of dynamic programming: O(len(str1) + len(str2)), but at the cost of
much higher memory usage and a more complicated algorithm. See Gusfield 1999.
"""

import collections
import unittest


def longest_substring(str1, str2):

    # Use the shorter string as the "horizontal" or inner loop.
    if len(str1) < len(str2):
        h_str = str1
        v_str = str2
    else:
        h_str = str2
        v_str = str1

    # Initialize state variables.
    prev_row = collections.defaultdict(int)
    row = collections.defaultdict(int)
    longest_strings = set()
    max_length_seen = 0

    # Compare each vertical character, with each character in the horizontal
    # string, and then go to the next vertical character.
    for v_char in v_str:
        for i, h_char in enumerate(h_str):

            # If the characters match, 
            if h_char == v_char:
                common_str_len = prev_row[i-1] + 1
                row[i] = common_str_len
                common_substr = h_str[i - common_str_len + 1:(i + 1)]

                if row[i] == max_length_seen:
                    longest_strings.add(common_substr)
                elif row[i] >= max_length_seen:
                    max_length_seen = row[i]
                    longest_strings = set([common_substr])

                #print 'row[%s]: %s' % (i, row[i])
        prev_row = row
        row = collections.defaultdict(int)

    return tuple(longest_strings)


class TestCase(unittest.TestCase):

    def test_something(self):
        longest_substring('xydxyaa', 'abcdxyz')
        longest_substring('aaaaaarackspacexxxxxx', 'abrackspacezzz')
        longest_substring('aaaaaaaaa', 'aaaaaaaaaaaaaaaaaaaaaaaaaa')

    def test_multiple_same_length(self):
        longest_substring('xxx123yyyy456zzz', '789zzz012xxx345yyy')

    def test_no_common_substrings(self):
        longest_substring('123456', 'abcdef')

    def test_empty_string(self):
        longest_substring('rackspace', '')


if __name__ == '__main__':
    unittest.main()
