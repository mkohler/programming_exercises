# Copyright (c) 2010 Mark Kohler


from __future__ import division
import itertools
import operator
import unittest


def how_much_change_do_i_use(coin_types_float, coin_quantities,
        price_of_shiny):

    coin_types = coin_types_in_pennies(coin_types_float)
    price_in_cents = int(price_of_shiny * 100)

    reduced_quantities = adjust_coin_quantities(coin_types,
                                                coin_quantities,
                                                price_in_cents)

    matches  = change(coin_types, reduced_quantities, price_in_cents)

    num_coins = [ sum(match) for match in matches ]

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
    unittest.main()





# Optimization: Truncate quantities down to price/value.
# i.e. if you have 100 dimes and shiny costs a dollar, you're
# not going to use more than 10 dimes.
