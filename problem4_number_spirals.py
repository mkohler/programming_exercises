#! /usr/bin/env python2.6
# Copyright (c) 2010 Mark Kohler
"""Rackspace Test, Problem 4, Number Spirals.

You are to write an application that creates number spirals.

Write a method that accepts an integer width and height and generates a number
spiral as above.  Note that the numbers are right-aligned and padded with
spaces in columns which are as wide as the widest number in the spiral. Each
column is then separated by a single space.
"""

import optparse
import sys
import unittest


def main():
    usage = '%prog [-h|-t] HEIGHT WIDTH'
    parser = optparse.OptionParser(usage,
                                   description=__doc__)
    parser.add_option('-t', '--test', action='store_true', default=False,
                      help='''Test this program''')
    (options, args) = parser.parse_args()

    if options.test:
        # Remove the options flag and run the tests.
        sys.argv = sys.argv[0:1]
        return unittest.main()

    if len(args) < 2:
        parser.error('''specify HEIGHT and WIDTH of spiral''')

    try:
        height = int(args[0])
        width = int(args[1])
    except ValueError:
        parser.error('''HEIGHT and WIDTH must be integers''')

    oblong_number_spiral_funball(height, width)


def oblong_number_spiral_funball(height, width):
    print OblongNumberSpiral(height, width)


class Matrix(object):
    """Build and store a two-dimensional matrix of values.

    The coordinates are (horizontal, vertical) and the origin is in the upper
    left corner.  For example, the coordinates of Matrix(2, 4) would be
    0,0  0,1, 0,2  0,3
    1,0  1,1, 1,2  1,3
    """

    def __init__(self, height, width):
        self.matrix = [[None] * width for row in range(height)]

    def is_vacant(self, x, y):
        """Return true if the coordinate is valid and empty."""
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


# go_xxx routines
#
# These simple routines define what going forward in a particular direction
# means in our coordinate system.  The origin is in the top left
# corner. That's why north and south seem backward.

def go_east(x, y):
    return x + 1, y


def go_west(x, y):
    return x - 1, y


def go_south(x, y):
    return x, y + 1


def go_north(x, y):
    return x, y - 1


class OblongNumberSpiral(object):

    class NoVacanciesException(Exception):
        pass

    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.matrix = Matrix(height, width)

        # Spirals always start going east (to the right).
        self.go_forward = go_east
        self.make_spiral()

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
        """Encapsulate finding the next location in the spiral.

        When we reach a non-empty or out-of-bounds coordinate, we
        turn 90 degrees clockwise and go that way. And if that way
        is non-empty, we know the spiral is finished.
        """
        # This is a state_transition diagram.
        turn_clockwise = {go_east: go_south,
                          go_south: go_west,
                          go_west: go_north,
                          go_north: go_east}

        # Try moving forward.
        new_x, new_y = self.go_forward(x, y)

        # Check if this space is vacant.
        if self.matrix.is_vacant(new_x, new_y):
            return new_x, new_y

        # If it's not, change directions, and move forward.
        # If the new space isn't vacant, give up, we're done.
        self.go_forward = turn_clockwise[self.go_forward]
        new_x, new_y = self.go_forward(x, y)

        if self.matrix.is_vacant(new_x, new_y):
            return new_x, new_y

        raise self.NoVacanciesException((new_x, new_y))

    def __str__(self):
        number_width = len('%s' % (self.height * self.width))

        cols = []
        for row in range(self.height):
            row_numbers = []
            for col in range(self.width):
                value = self.matrix.get_value(col, row)
                row_numbers.append("%*s" % (number_width, value))
            cols.append(' '.join(row_numbers))
        return '\n'.join(cols)


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
        solution = (" 1  2  3\n"
                    "10 11  4\n"
                    " 9 12  5\n"
                    " 8  7  6")
        self.assertEqual(solution, '%s' % OblongNumberSpiral(4, 3))

    def test_example2(self):
        solution = (" 1  2  3  4  5\n"
                    "18 19 20 21  6\n"
                    "17 28 29 22  7\n"
                    "16 27 30 23  8\n"
                    "15 26 25 24  9\n"
                    "14 13 12 11 10")
        self.assertEqual(solution, '%s' % OblongNumberSpiral(6, 5))


if __name__ == '__main__':
    sys.exit(main())
