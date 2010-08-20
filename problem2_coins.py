#! /usr/bin/env python2.6
# Copyright (c) 2010 Mark Kohler
"""Rackspace Test, Problem 2, Coins.

You are given an array of floating point values representing American currency,
another array representing the quantity of each coin in your possession and a
dollar amount.  The values of the coins aren't necessarily standard
denominations. However, you may assume the array of coin values are sorted in
ascending order, and that all coins consist of at most two decimal places.
Additionally you may assume that the price will never exceed 10 dollars.  Write
a method to determine the smallest number of coins that can represent the
dollar amount.

signature: coins array = how much change do i use(array coin types,
    array coin quantities, float price of shiny)

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
    '''%prog [-h|-t] TYPES AMOUNTS PRICE\n\n''' +
    '''      TYPES        value1,value2,...\n''' +
    '''      QUANTITIES   quantity1,quantity2,...\n''' +
    '''      PRICES       dd.cc\n\n''' +
    '''Example: 10 each of pennies, nickels, and dimes, price $1.25\n''' +
    '''         %prog 0.01,0.05,0.10 10,10,10 1.25''')
    parser = optparse.OptionParser(usage,
                                   description=__doc__)
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
        coin_types = map(float, args[0].split(','))
        coin_quantities = map(int, args[1].split(','))
        price = float(args[2])
    except ValueError:
        parser.error('invalid parameters')

    num_coins = how_much_change_do_i_use(coin_types, coin_quantities, price)
    if num_coins == 0:
        print 'The coins entered cannot sum to %s' % price
    else:
        print 'minimum coins: %s' % num_coins


def how_much_change_do_i_use(coin_types_float, coin_quantities,
        price_of_shiny):

    coin_types = coin_types_in_pennies(coin_types_float)
    price_in_cents = int(price_of_shiny * 100)

    reduced_quantities = adjust_coin_quantities(coin_types,
                                                coin_quantities,
                                                price_in_cents)

    matches = change(coin_types, reduced_quantities, price_in_cents)

    num_coins = [sum(match) for match in matches]

    if len(num_coins) == 0:
        return None

    return min(num_coins)


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


# equivalent to nested for loops for each coin type.
def change(coin_types, coin_quantities, price):

    combs = itertools.product(*itertools.imap(crange, coin_quantities))

    return (c for c in combs if coin_value(coin_types, c) == price)


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

    def test_change(self):
        coin_types = (1, 5, 10)
        matches = list(change(coin_types, (5, 1, 1), 10))
        self.assert_((5, 1, 0) in matches)
        self.assert_((0, 0, 1) in matches)
        self.assertEqual(2, len(matches))

    def test_cant_make_change(self):
        coin_types = (5, 10)
        matches = list(change(coin_types, (5, 10), 3))
        self.assertEqual(0, len(matches))


if __name__ == '__main__':
    sys.exit(main())
