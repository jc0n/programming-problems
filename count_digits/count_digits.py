#~/usr/bin/env python
"""
Solutions to count the total number of digits in all of the numbers 0..n
"""

__author__ = 'John O\'Connor'
__version__ = 0.1

from math import floor, log10

# Number of digits in the integer n
num_digits = lambda n: int(floor(log10(n)) + 1)

# Build the desired string by hand
buildstr = lambda n: ''.join(map(str, xrange(0, n + 1)))

# O(n) linear solution
#
# Explanation:
#
# floor(log10(n)) gives one less the number of digits in `n`
# The sum of floor(log10(i)) + 1 from i=0..n adds up the count of digits in each number from 0..n
#
def size_linear(n):
    i = 1
    x = 0
    while (i <= n):
        x += num_digits(i)
        i += 1
    return int(x + 1)

# O(n) linear solution
# Different represenation of the above
def size_linear2(n):
    return int(sum(num_digits(i) for i in xrange(1, n + 1)) + 1 if n > 0 else 1)


# O(log10 n) solution
#
# Explanation:
#
# Solution uses a series bounded by floor(log10(n)) + 1 which yields better than linear complexity.
# It works by counting the number of digits in `n` ie. (floor(log10(n)) + 1) and then multiplying `n` by the number of digits in `n` while
# continually subtracting the digits counted more than once.
#
# Expansion of the series looks like:
# m = floor(log10(n)) + 1
# (n with at least 1 digit) + (n with at least 2 digits minus n with only 1 digit)  + ... + (1 for the zero)
# = n + (n - 10^1 - 1) + (n - 10^2 - 1) + ... + 1
# = n + (n - 9) + (n - 99) + ... + 1
# = (m * n) - sum(10^i - 1 from i=1 to m) + 1
# = m(n+1) - sum(10^i from i=0 to m) + 1
def size_log10(n):
    if n == 0: # log10(0) -> undefined
        return 1
    m = num_digits(n)
    x = n + m
    b = 10
    for i in range(1, m):
        x += n - b
        b *= 10
    return x

# Optimal Solution: O(1)
# Same as above but solved the partial sum for the series 10^m where m = floor(log10(n)) + 1
def size_constant(n):
    if n == 0:
        return 1
    m = num_digits(n)
    return int((m * (n + 1)) - ((10 ** m - 1) / 9.0) + 1)


