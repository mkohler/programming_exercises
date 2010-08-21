#! /usr/bin/env python2.6
# Copyright (c) 2010 Mark Kohler
"""Rackspace Test, Problem 3, Substrings.

You are given two strings of arbitrary, and possibly different, length. Write a
method to determine the set of longest possible substrings common to both, if
any exists. Note that library methods, if implemented in your language of
choice, will not be accepted.

signature: substring = longest substring(string s1, string s2)

This solution uses dynamic programming and runs in O(len(s1) * len(s2)).

The generalized suffix tree algorith offers O(len(s1) + len(s2) performance
at the cost of a more complicated algorithm. The best reference for suffix
tree algorithms appears to be Gusfield 1999.

Tested with Python 2.6.


"""

import collections
import unittest



def longest_substring(s1, s2):

    if len(s1) < len(s2):
        h_str = s1
        v_str = s2
    else:
        h_str = s2
        v_str = s1

    prev_row = collections.defaultdict(int)
    row = collections.defaultdict(int)
    longest_strings = set()
    max_length_seen = 0

    for v_char in v_str:
        for i, h_char in enumerate(h_str):
            print 'v_char: %s, h_char %s' % (v_char, h_char)
            if h_char == v_char:
                common_str_len = prev_row[i-1] + 1
                row[i] = common_str_len
                print "common: %s" % h_str[i-common_str_len+1:i+1]
                if row[i] == max_length_seen:
                    #longest_strings.add()
                    pass
                elif row[i] >= max_length_seen:
                    max_length_seen = row[i]
                    #longest_strings = set([])

                print 'row[%s]: %s' % (i, row[i])
        prev_row = row
        row = collections.defaultdict(int)




class TestCase(unittest.TestCase):
    def test_something(self):
        longest_substring('xydxyaa', 'abcdxyz')

if __name__ == '__main__':
    unittest.main()
