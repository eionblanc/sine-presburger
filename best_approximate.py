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