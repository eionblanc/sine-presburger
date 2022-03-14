import numpy as np
from functools import reduce

def gcd_rational(ab : tuple, cd : tuple) -> tuple:
    """
    Compute the greatest common divisor of a/b and c/d.
    Return numerator and denominator to facilitate reduction.
    :param ab: 2-tuple of ints, first numerator and denominator
    :param cd: 2-tuple of ints, second numerator and denominator
    """
    return (np.gcd(ab[0], cd[0]), np.lcm(ab[1], cd[1]))

def gcd(arr : list) -> float:
    """
    Compute the greatest common divisor of arbitrarily many rational numbers.
    Return the decimal value, not its fraction form.
    :param arr: array of 2-tuples of ints, each numerator and denominator
    """
    ab = reduce(gcd_rational, arr)
    return ab[0] / ab[1]

def lincombspace(eps : float, c : float, R : float):
    """
    Compute the space of linear combinations; integer multiples plus a constant
    in centered, bounded interval.
    :param eps: incremental value
    :param c: constant value to include in linear combination
    :param R: radius of centered, bounded interval to restrict to
    """
    l_k = int((-R - c) // eps) + 1
    r_k = int((R - c) // eps)
    return (eps*k + c for k in range(l_k, r_k+1))