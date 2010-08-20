# Copyright (c) 2010 Mark Kohler

import unittest


# We want something that will be a multidimenionsal blah blah
# Coordinates of a Matrix(2, 3)
# 0,0 0,1, 0,2 0,3
# 1,0 1,1, 1,2 1,3


class Matrix(object):

    def __init__(self, height, width):
        self.matrix = [[None] * width for row in range(height)]

    def is_vacant(self, x, y):
        if x < 0 or y < 0:
            return False

        try:
            if self.matrix[y][x] is None:
                return True
        except IndexError:
            pass

        return False

    def get_value(self, x, y):
        return self.matrix[y][x]

    def set_value(self, x, y, value):
        self.matrix[y][x] = value

"""
Coordinate System

origin is in the top left corner.

north and south are backward.
"""


def go_east(x, y):
    return x + 1, y


def go_west(x, y):
    return x - 1, y


def go_south(x, y):
    return x, y + 1


def go_north(x, y):
    return x, y - 1

turn_clockwise = {go_east: go_south,
                  go_south: go_west,
                  go_west: go_north,
                  go_north: go_east}


class OblongNumberSpiral(object):

    class NoVacanciesException(Exception):
        pass

    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.matrix = Matrix(height, width)


        self.go_forward = go_east

        self.make_spiral()
        self.print_(height, width)

    def make_spiral(self):
        count = 1
        x = 0
        y = 0

        while True:
            # We always start the loop at an empty square.
            self.matrix.set_value(x, y, count)
            count += 1

            # Then move on
            try:
                x, y = self.next_coordinate(x, y)
            except self.NoVacanciesException:
                return

    def next_coordinate(self, x, y):
            # Try moving forward
            new_x, new_y = self.go_forward(x, y)

            # Check if this is vacant.
            if self.matrix.is_vacant(new_x, new_y):
                return new_x, new_y

            # If it's not change directions, and move forward.
            # It this space isn't vacant, give up, we're done.
            self.go_forward = turn_clockwise[self.go_forward]
            new_x, new_y = self.go_forward(x, y)

            if self.matrix.is_vacant(new_x, new_y):
                return new_x, new_y

            raise self.NoVacanciesException((new_x, new_y))

    def print_(self, height, width):
        number_width = len('%s' % (height * width))

        for row in range(height):
            row_numbers = []
            for col in range(width):
                value = self.matrix.get_value(col, row)
                row_numbers.append("%*s" % (number_width, value))
            print ' '.join(row_numbers)


class TestMatrix(unittest.TestCase):

    def test_is_vacant(self):
        matrix = Matrix(height=2, width=7)
        self.assert_(matrix.is_vacant(0, 0))
        self.assert_(matrix.is_vacant(6, 0))
        self.assert_(matrix.is_vacant(0, 1))
        self.assert_(matrix.is_vacant(6, 1))

        self.failIf(matrix.is_vacant(-1, 0))
        self.failIf(matrix.is_vacant(7, 0))
        self.failIf(matrix.is_vacant(0, -1))
        self.failIf(matrix.is_vacant(0, 2))

    def test_set_value(self):
        matrix = Matrix(height=3, width=2)
        matrix.set_value(0, 0, 1)
        matrix.set_value(1, 0, 2)
        matrix.set_value(1, 1, 3)
        matrix.set_value(1, 2, 4)
        matrix.set_value(0, 2, 5)
        matrix.set_value(0, 1, 6)
        self.assertEqual(matrix.get_value(0, 0), 1)
        self.assertEqual(matrix.get_value(1, 0), 2)
        self.assertEqual(matrix.get_value(1, 1), 3)
        self.assertEqual(matrix.get_value(1, 2), 4)
        self.assertEqual(matrix.get_value(0, 2), 5)
        self.assertEqual(matrix.get_value(0, 1), 6)


class TestSpiral(unittest.TestCase):

    def test_example1(self):
        solution = (" 1  2 3"
                    "10 11 4"
                    " 9 12 5"
                    " 8  7 6")
        o = OblongNumberSpiral(4, 3)
        o.make_spiral()
        o.print_()

    def test_example2(self):
        o = OblongNumberSpiral(6, 5)
        o.make_spiral()

if __name__ == '__main__':
#    o = OblongNumberSpiral(4, 3)
    unittest.main()
