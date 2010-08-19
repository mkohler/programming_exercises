import unittest


class NotAnOperatorError(ValueError):
    pass


class Node(object):

    def __init__(self, oper):
        if oper not in ('+', '-', '*', '/'):
            raise NotAnOperatorError('"%s" is not a supported operator' % oper)
        self.oper = oper


class Tests(unittest.TestCase):

    def test_good_operator(self):
        root = Node('+')

    def test_bad_operator(self):
        self.assertRaises(NotAnOperatorError, Node, 'x')

if __name__ == '__main__':
    unittest.main()
