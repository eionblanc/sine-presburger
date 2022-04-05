import numpy as np
import math
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

def lcm(arr : list) -> int:
    """
    Compute the least common multiple of arbitrarily many positive integers.
    :param arr: array of ints
    """
    n = len(arr)
    if n == 0:
        return 1
    elif n == 1:
        return arr[0]
    else:
        return np.lcm(arr[0], lcm(arr[1:]))
    
def divisibility_N(D : dict, n : int) -> int:
    """
    Compute the constant N from the proof of Theorem 4.17 as the least common
    multiple of the reduced divisors for a particular variable.
    :param D: dictionary with keys 'k' and 'p', each divisor and coefficient vector on
              variable; each tuple corresponds to a divisibility predicate.
    :param n: int, variable for coefficients
    """
    N = 1
    for pred in D:
        p = pred['p']
        if p[n] != 0:
            k = pred['k']
            N = np.lcm(N, int(k/np.gcd(k,np.abs(p[n]))))
    return N

def lincombspace(eps : float, c : float, R : float, Ra = None):
    """
    Compute the space of linear combinations; integer multiples plus a constant
    in closed interval determined by either [-R,R] or if specified, [Ra,R].
    :param eps: incremental value
    :param c: constant value to include in linear combination
    :param R: radius of bounded interval to restrict to
    :param Ra: optional lower endpoint for non-centered interval 
    """
    if not Ra:
        Ra = -R
    l_k = int(math.ceil((Ra - c) / eps))
    r_k = int(math.floor((R - c) / eps))
    return (eps*k + c for k in range(l_k, r_k+1))