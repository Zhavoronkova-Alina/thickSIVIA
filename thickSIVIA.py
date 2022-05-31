from enum import Enum
from pyibex import IntervalVector, LargestFirst
from collections import deque
from vibes import vibes


class IBOOL(Enum):
    IN = 0
    OUT = 1
    MAYBE = 2
    UNK = 3
    EMPTY = 4


def thickSIVIA(X0, test, eps):
    stack = deque([IntervalVector(X0)])
    L_clear = deque()
    L_dark = deque()
    L_penumbra = deque()
    L_too_small = deque()
    lf = LargestFirst(eps / 2.0)
    i = 0
    while len(stack) > 0:
        i = i + 1
        X = stack.popleft()
        t = test.test(X)

        if t == IBOOL.IN:
            L_clear.append(X)
        elif t == IBOOL.OUT:
            L_dark.append(X)
        elif t == IBOOL.MAYBE:
            L_penumbra.append(X)
        else:
            if X.max_diam() > eps:
                (X1, X2) = lf.bisect(X)
                stack.append(X1)
                stack.append(X2)
            else:
                L_too_small.append(X)
    print("Number of tests : %d" % i)
    return L_clear, L_dark, L_penumbra, L_too_small


def draw_thickSIVIA_result(L_clear: deque, L_dark: deque, L_penumbra: deque, L_too_small: deque):
    while len(L_clear) > 0:
        X = L_clear.popleft()
        vibes.drawBox(X[0][0], X[0][1], X[1][0], X[1][1], '[r]')

    while len(L_dark) > 0:
        X = L_dark.popleft()
        vibes.drawBox(X[0][0], X[0][1], X[1][0], X[1][1], '[b]')

    while len(L_penumbra) > 0:
        X = L_penumbra.popleft()
        vibes.drawBox(X[0][0], X[0][1], X[1][0], X[1][1], '[orange]')

    while len(L_too_small) > 0:
        X = L_too_small.popleft()
        vibes.drawBox(X[0][0], X[0][1], X[1][0], X[1][1], '[y]')

    vibes.axisEqual()
