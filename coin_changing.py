#! /usr/bin/env python2.6
# Copyright (c) 2010 Mark Kohler
"""Problem 2, Coins.

Tested with Python 2.6.
"""

from __future__ import division
import itertools
import operator
import optparse
import sys
import unittest


def main():
    usage = (
    '''%prog [-h|-r|-t] TYPES AMOUNTS PRICE\n\n''' +
    '''      TYPES        value1,value2,...\n''' +
    '''      QUANTITIES   quantity1,quantity2,...\n''' +
    '''      PRICES       dd.cc\n\n''' +
    '''Example: 10 each of pennies, nickels, and dimes, price $1.25\n''' +
    '''         %prog 0.01,0.05,0.10 10,10,10 1.25''')
    parser = optparse.OptionParser(usage,
                                   description=__doc__)
    parser.add_option('-r', '--recursive', action='store_true', default=False,
                      help='''Use recursive algorithm''')
    parser.add_option('-t', '--test', action='store_true', default=False,
                      help='''Test this program''')
    (options, args) = parser.parse_args()

    if options.test:
        # Remove the options flag and run the tests.
        sys.argv = sys.argv[0:1]
        return unittest.main()

    if len(args) < 3:
        parser.error('missing parameters')

    try:
        coin_types = [float(t) for t in args[0].split(',')]
        coin_quantities = [int(q) for q in args[1].split(',')]
        price = float(args[2])
    except ValueError:
        parser.error('invalid parameters')

    if len(coin_types) != len(coin_quantities):
        parser.error('TYPES and AMOUNTS do not match.')

    solutions = how_much_change_do_i_use(coin_types, coin_quantities, price,
                                         options.recursive)
    if solutions:
        print format_solutions(coin_types, solutions)
    else:
        print 'The coins entered cannot represent %.2f.' % price


def format_solutions(coin_types, solutions):
    output_lines = []
    for i, solution in enumerate(solutions, 1):
        line = []
        line.append('Solution %s:' % i)
        for coin, quantity in zip(coin_types, solution):
            line.append(' %.2f: %s coin(s)' % (coin, quantity))
        output_lines.append(' '.join(line))
    return '\n'.join(output_lines)


def how_much_change_do_i_use(coin_types_float, coin_quantities,
        price_of_shiny, recursive=False):
    """Normalize inputs into integer amounts and massage output of change()."""

    coin_types = coin_types_in_pennies(coin_types_float)
    price_in_cents = int(price_of_shiny * 100)

    reduced_quantities = adjust_coin_quantities(coin_types,
                                                coin_quantities,
                                                price_in_cents)

    if recursive:
        matches_gen = change_r(coin_types, reduced_quantities, price_in_cents)
    else:
        matches_gen = change(coin_types, reduced_quantities, price_in_cents)

    # Make a copy of the generator because we're going to do two passes over
    # the list of matches.
    matches_gen, min_coins_gen = itertools.tee(matches_gen)

    # First we'll run through all of the coin combinations to find the
    # minimum number of coins, returning None if there were no solutions.
    try:
        min_coins = min((sum(match) for match in min_coins_gen))
    except ValueError:
        return None

    # Second, we'll create a filter for that number of coins. There may
    # be multiple solutions that use the same number of coins.
    min_coin_gen = (m for m in matches_gen if sum(m) == min_coins)

    return list(min_coin_gen)


def coin_types_in_pennies(coin_types_floats):
    """Convert coin_types list from dollar-floats to penny-ints."""
    return [int(c_type * 100) for c_type in coin_types_floats]


def adjust_coin_quantities(c_types, c_quantities, price_in_cents):
    """Reduce the coin_quantity list down to what's feasible."""
    adjusted_quantities = []
    for i, coin_type in enumerate(c_types):
        quantity = num_usable(c_types[i], c_quantities[i], price_in_cents)
        adjusted_quantities.append(quantity)
    return adjusted_quantities


def num_usable(coin_type, coin_quantity, price_in_cents):
    """Reduce the number of coins down to what could be used."""
    return min(coin_quantity, price_in_cents // coin_type)


def change(coin_types, coin_quantities, price):
    """change implements a brute-force algorithm for making change."""

    # combs (combinations) is a generator expression that generates
    # every combination of coins.
    combs = itertools.product(*itertools.imap(crange, coin_quantities))

    # Create another generator that runs through combs looking for
    # combinations that add up to the specified price.
    return (c for c in combs if coin_value(coin_types, c) == price)


def change_r(ctypes, avail, price_in_cents):

    if price_in_cents == 0:
        return [(0,)]
    results = []
    _change_r(ctypes, avail, price_in_cents, [0] * len(ctypes), 0, results)
    return results


def _change_r(ctypes, avail, price_in_cents, used, coin_index, results):
    """Recursive variant of change routine.

    For each type of coin, there is a level of recursion.
    """
    value = coin_value(ctypes, used)
    if value == price_in_cents:
        results.append(tuple(used))
        return
    if value > price_in_cents or coin_index >= len(ctypes):
        return

    # Take the first type of coin in the array.
    # For every possible quanity of this coin, call change().
    for n_coins_of_this_type in range(avail[coin_index] + 1):
        # There has to be a better way. I want an expression that will
        # add n_coins_of_this_type to the used[coin_index] and return
        # the modified version of used.
        used_r = used[:]
        used_r[coin_index] = n_coins_of_this_type
        _change_r(ctypes,
                  avail,
                  price_in_cents,
                  used_r,
                  coin_index + 1,
                  results)

    return

def crange(coins):
    """Like xrange, but goes one higher to include the number itself."""
    return xrange(coins + 1)


def coin_value(coin_types, coin_quantities):
    """Calculate total value in cents of all coins.

    coin_types is a list of coin denominations, in cents.
    coin_quantities is a list of coin quantity in each denomination
    """
    return sum(itertools.imap(operator.mul, coin_types, coin_quantities))


class TestCase(unittest.TestCase):

    def test_coin_value(self):
        self.assertEqual(coin_value((1, 5, 100), (3, 2, 4)), 413)

    def test_coin_types_in_pennies(self):
        orig = [0.01, 0.03, 1.23]
        expected = [1, 3, 123]
        self.assertEqual(expected, coin_types_in_pennies(orig))

    # If you have 100 dimes and shiny costs a dollar, you can't use more than
    # 10 dimes.
    def test_num_usable(self):
        self.assertEqual(10, num_usable(10, 109, 100))

    def test_adjust_coin_quantities(self):
        types = (1, 5, 10)
        quantities = (1000, 1000, 1000)
        price = 100
        expected = [100, 20, 10]
        self.assertEqual(expected,
                         adjust_coin_quantities(types, quantities, price))

    def test_crange(self):
        self.assertEqual([0, 1, 2, 3], list(crange(3)))

    def test_how_much_normal_case(self):
        types = [0.01, 0.05, 0.10]
        quantities = [5, 5, 50]
        price = 0.63
        answers = how_much_change_do_i_use(types, quantities, price)
        self.assertEqual([(3, 0, 6)], answers)

    def test_how_much_non_unique_solutions(self):
        types = [0.01, 0.10, 0.28]
        quantities = [10, 10, 10]
        price = 0.60
        answers = how_much_change_do_i_use(types, quantities, price)
        self.assertEqual(3, len(answers))
        self.assert_((0, 6, 0) in answers)
        self.assert_((2, 3, 1) in answers)
        self.assert_((4, 0, 2) in answers)

    def test_how_much_fails(self):
        types = [0.01, 0.10, 0.28]
        quantities = [1, 1, 1]
        price = 0.30
        answers = how_much_change_do_i_use(types, quantities, price)
        self.assertEqual(None, answers)


class TestChange(unittest.TestCase):
    def test_null_case(self):
        input_args = ([1], [5], 0)
        expected = [(0,)]

        self.assertEqual(expected, list(change(*input_args)))
        self.assertEqual(expected, list(change_r(*input_args)))

    def test_3_pennies(self):
        input_args = ([1], [5], 3)
        expected = [(3,)]
        self.assertEqual(expected, list(change(*input_args)))
        self.assertEqual(expected, list(change_r(*input_args)))

    def test_3_nickels(self):
        input_args = ([5], [5], 15)
        expected = [(3,)]
        self.assertEqual(expected, list(change(*input_args)))
        self.assertEqual(expected, list(change_r(*input_args)))

    def test_two_coins_two_solutions(self):
        input_args = ([1, 5], [10, 10], 6)
        expected = [(1, 1), (6, 0)]
        self.assertEqual(expected, list(change(*input_args)))
        self.assertEqual(expected, list(change_r(*input_args)))

    def test_change_not_enough_coins(self):
        input_args = ([1, 5], [5, 5], 100)
        expected = []
        self.assertEqual(expected, list(change(*input_args)))
        self.assertEqual(expected, list(change_r(*input_args)))

    def test_change_three_coins(self):
        input_args = ((1, 5, 10), (5, 1, 1), 10)
        expected1 = (5,1,0)
        expected2 = (0,0,1)
        self.assert_(expected1 in list(change(*input_args)))
        self.assert_(expected2 in list(change_r(*input_args)))

    def test_no_nickels(self):
        input_args = ((1, 10, 25), (5, 5, 5), 30)
        expected1 = (0, 3, 0)
        expected2 = (5, 0, 1)
        self.assert_(expected1 in list(change(*input_args)))
        self.assert_(expected2 in list(change_r(*input_args)))

    def test_change_fails(self):
        input_args = ((5, 10), (5, 10), 3)
        expected = 0
        self.assertEqual(0, len(list(change(*input_args))))
        self.assertEqual(0, len(list(change_r(*input_args))))

if __name__ == '__main__':
    sys.exit(main())
