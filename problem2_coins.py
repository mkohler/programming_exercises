# Copyright (c) 2010 Mark Kohler


from __future__ import division
import itertools
import operator
import unittest




def coin_value(coin_types, coin_quantities):
    """Calculate total value in cents of all coins.

    coin_types is a list of coin denominations, in cents.
    coin_quantities is a list of coin quantity in each denomination
    """
    return sum(itertools.imap(operator.mul, coin_types, coin_quantities))


def num_usable(coin_type, coin_quantity, price_in_cents):
    """Reduce the number of coins down to what could be used."""
    return min(coin_quantity, price_in_cents // coin_type)


def adjust_coin_quantities(c_types, c_quantities, price_in_cents):

    adjusted_quantities = []
    for i, coin_type in enumerate(coin_types):
        quantity = num_usable(c_types[i], c_quantities[i], price_in_cents)
        adjusted_quantities.append(quantity)
    return adjusted_quantities


def crange(coins):
    """Like xrange, but goes one higher to include the number itself."""
    return xrange(coins + 1)


def change(coin_types, coin_quantities, price):
    int_price = int(price * 100)

    coin_choices = [ c + 1 for c in coin_quantities ]

    for comb in itertools.product(*itertools.imap(crange, coin_choices)):
#        print comb
        #print coin_value(coin_types, comb)
        if coin_value(coin_types, comb) == int_price:
            pass
            # print '\t\t%s, %s, %s' % comb








class TestCase(unittest.TestCase):
    def test_coin_value(self):
        self.assertEqual(coin_value((1,5,100), (3, 2, 4)), 413)

    # If you have 100 dimes and shiny costs a dollar, you can't use more than
    # 10 dimes.
    def test_num_usable(self):
        self.assertEqual(10, num_usable(10, 109, 100))

    def test_crange(self):
        self.assertEqual([0,1,2,3], list(crange(3)))

    def test_change(self):
        coin_types = (1, 5, 10)
        change(coin_types, (5, 5, 5), .25)



if __name__ == '__main__':
    unittest.main()





# Optimization: Truncate quantities down to price/value.
# i.e. if you have 100 dimes and shiny costs a dollar, you're
# not going to use more than 10 dimes.
