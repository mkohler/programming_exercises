#!/usr/bin/env python2.6
from __future__ import division
import operator
import unittest


class NotAnOperatorError(ValueError):
    pass


class Node(object):
    operator_dict = {'+': operator.add,
                     '-': operator.sub,
                     '*': operator.mul,
                     '/': operator.truediv}

    def __init__(self, symbol):
        self.symbol = symbol
        self.children = []

    def add_node(self, symbol):
        child_node = Node(symbol)
        self.children.append(child_node)
        return child_node

    def add_nodes(self, symbol_list):
        return [self.add_node(s) for s in symbol_list]

    def calculate(self):
        if not self.children:
            return self.symbol

        values = [x.calculate() for x in self.children]

        return reduce(self.operator_dict[self.symbol], values)


class TestCalculate(unittest.TestCase):

    def test_calc_add_basic(self):
        root = Node('+')
        root.add_node(1)
        root.add_node(1)
        root.add_node(1)
        self.assertEqual(root.calculate(), 3)

    def test_depth2(self):
        root = Node('*')
        node = root.add_node('+')
        node.add_node(2)
        node.add_node(3)

        node = root.add_node('-')
        node.add_node(10)
        node.add_node(1)

        self.assertEqual(root.calculate(), 45.0)

    def test_unbalanced_tree(self):
        root = Node('+')
        depth1_nodes = root.add_nodes('/+')
        depth1_nodes[0].add_nodes((45, 15))
        add_children = depth1_nodes[1].add_nodes('---')
        add_children[0].add_nodes((100, 10, 1))
        add_children[1].add_nodes((200, 20, 2))
        add_children[2].add_nodes((300, 30, 3))
        self.assertEqual(root.calculate(), 537)


if __name__ == '__main__':
    unittest.main()
