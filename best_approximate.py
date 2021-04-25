import numpy as np

def approx(N, d):
    """
    Compute the best approximate of N up to d under the sine function.
    :param N: int being approximated
    :param d: int degree of approximation
    :return A: int approximation of N up to d
    """
    if N < 0:
        pass
    if d >= N or d < 0:
        return N
    sine_true = np.sin(N)
    sine_approx = -1
    A = 0
    for n in range(d+1):
        s = np.sin(n)
        if sine_approx < s and s < sine_true:
            sine_approx = s
            A = n
    return A
    # Sleeker but slower
    #return np.argmax([np.sin(n) if np.sin(n) <= sine_true else -1 for n in range(d+1)])

def diff_approx(x1, x2, d, e):
    """
    Compute the best difference approximates of x1 and x2 under the sine function.
    That is, minimize |sin(x2) - sin(x1) - |sin(y1) - sin(y2)||,
    where y1 is at most d and y2 is at most e.
    :param x1: int with lower sine value for difference approximation
    :param x2: int with greater sine value for difference approximation
    :param d: int upper bound for returned y1
    :param e: int upper bound for returned y2
    :return y1: int bounded by d comprising a best difference approximate
    :return y2: int bounded by e comprising a best difference approximate
    """
    diff_true = np.sin(x2) - np.sin(x1)
    y1,y2 = (None,None)
    if min(x1,x2,d,e) < 0 or diff_true <= 0:
        return y1,y2
    err_approx = 2.
    for n1 in range(d+1):
        s1 = np.sin(n1)
        for n2 in range(e+1):
            s2 = np.sin(n2)
            error = np.abs(diff_true - np.abs(s1-s2))
            if error < err_approx:
                err_approx = error
                y1 = n1
                y2 = n2
    return y1,y2