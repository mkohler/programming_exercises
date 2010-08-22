#! /usr/bin/env python2.6
# Copyright (c) 2010 Mark Kohler
"""Problem 3, Substrings.

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

    # To save memory, use the shorter string as the "horizontal" or inner loop.
    if len(str1) < len(str2):
        h_str = str1
        v_str = str2
    else:
        h_str = str2
        v_str = str1

    # Initialize state variables. Use defaultdicts so that we don't have
    # to store all of the zero values in the dynamic programming matrix.
    prev_row = collections.defaultdict(int)
    row = collections.defaultdict(int)
    longest_strings = set()
    max_length_seen = 0

    # Compare each vertical character, with each character in the horizontal
    # string, and then go to the next vertical character.
    for v_char in v_str:
        for i, h_char in enumerate(h_str):

            # If the characters don't match, do nothing.
            # If they do, update the state variables.
            if h_char == v_char:

                # If there's a match, then look back to the previous
                # row and column to see how many previous characters
                # matched. Add one to get the value for this location.
                common_str_len = prev_row[i-1] + 1
                row[i] = common_str_len

                # If this common substring isn't one of the longest
                # we've seen, continue.
                if common_str_len < max_length_seen:
                    continue

                # Extact the common substring from the original string
                # by looking back from our current location, i, by the
                # length of the string.
                common_substr = h_str[i - common_str_len + 1:(i + 1)]

                # Either add this string to the set of equal-length strings,
                # or if this one breaks the record, start a new set.
                if common_str_len == max_length_seen:
                    longest_strings.add(common_substr)
                elif row[i] >= max_length_seen:
                    max_length_seen = common_str_len
                    longest_strings = set([common_substr])

        # After processing each row, discard the oldest row.
        prev_row = row
        row = collections.defaultdict(int)

    return list(longest_strings)


class TestCase(unittest.TestCase):

    def test_some_strings(self):
        self.assertEqual(['dxy'], longest_substring('xydxyaa', 'abcdxyz'))
        self.assertEqual(['substring'],
                         longest_substring('aaaaaasubstringxxxxxx',
                                           'absubstringzzz'))

        self.assertEqual(['shorter'],
                         longest_substring('shorter', 'shorterlonger'))
        self.assertEqual(['shorter'],
                         longest_substring('shorter', 'longershorter'))

    def test_multiple_same_length(self):
        substrs = longest_substring('xxx123yyyy456zzz', '789zzz012xxx345yyy')
        self.assertEqual(3, len(substrs))
        self.assert_('xxx' in substrs)
        self.assert_('yyy' in substrs)
        self.assert_('zzz' in substrs)

    def test_no_common_substrings(self):
        self.assertEqual([], longest_substring('123456', 'abcdef'))

    def test_empty_string(self):
        self.assertEqual([], longest_substring('somestring', ''))


if __name__ == '__main__':
    unittest.main()
