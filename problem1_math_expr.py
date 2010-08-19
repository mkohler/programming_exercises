from __future__ import division
import operator
import unittest


class NotAnOperatorError(ValueError):
    pass


class Node(object):
    operator_dict = { '+': operator.add,
                      '-': operator.sub,
                      '*': operator.mul,
                      '/': operator.truediv }

    def __init__(self, symbol):
        self.symbol = symbol

        self.children = []

        #if oper not in ('+', '-', '*', '/'):
        #    raise NotAnOperatorError('"%s" is not a supported operator' % oper)
        #self.oper = oper

    def add_node(self, symbol):
        self.children.append(Node(symbol))

    def calculate(self):
        if not self.children:
            return self.symbol

        values = [ x.calculate() for x in self.children ]

        return reduce(self.operator_dict[self.symbol], values)

#        for node in nodes:
#            if node is a number:
#                return number
#            else:
#                calculate(node)




    # Traverse the tree, out-of-order, in order to print on a terminal,
    # sideways.
#    def __str__(self):
#        return self.str_r(self.root, 0)
#
#    def str_r(self, node, level):
#        if node is None:
#            return ''
#        return (self.str_r(node._right, level+1)
#                + "%s%s:%s\n" % (6 * level * ' ', node.key, node.data)
#                + self.str_r(node._left, level+1))


class Tests(unittest.TestCase):
    def test_good_operator(self):
        root = Node('+')

    def xtest_bad_operator(self):
        self.assertRaises(NotAnOperatorError, Node, 'x')

    def test_add_leaf(self):
        root = Node('+')
        root.add_node(2.3)
        root.add_node(2.3)


class TestCalculate(unittest.TestCase):
    def test_calc_add_basic(self):
        root = Node('+')
        root.add_node(1)
        root.add_node(1)
        self.assertEqual(root.calculate(), 2)

    def test_calc_add_basic(self):
        root = Node('+')
        root.add_node(1)
        root.add_node(1)
        root.add_node(1)
        self.assertEqual(root.calculate(), 3)

    def test_calc_sub_basic(self):
        root = Node('-')
        root.add_node(5.0)
        root.add_node(0.5)
        self.assertEqual(root.calculate(), 4.5)


if __name__ == '__main__':
    unittest.main()
