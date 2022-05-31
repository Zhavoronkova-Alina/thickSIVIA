from pyibex import *
from thickSIVIA import *
from vibes import vibes
import numpy as np


# Tolerable-United solution sets
#  /                 \    /  \     /       \
# | [2, 4]    [-2, 0] |  | x1 | = | [-1, 1] |
# | [-1, 1]    [2, 4] |  | x2 |   | [0, 2]  |
#  \                 /    \  /     \       /


class TolUnSolSets:
    def __init__(self, B):
        self.B = B

    def test(self, X):
        Xm = IntervalVector([
            (min(2 * X[0], 4 * X[0]) + min(-2 * X[1], Interval(0))),
            (min(-X[0], X[0]) + min(2 * X[1], 4 * X[1]))
        ])

        Xp = IntervalVector([
            (max(2 * X[0], 4 * X[0]) + max(-2 * X[1], Interval(0))),
            (max(-X[0], X[0]) + max(2 * X[1], 4 * X[1]))
        ])

        Xub = Xm | Xp

        if self.B.is_disjoint(Xub):
            return IBOOL.OUT
        elif self.B.is_superset(Xub):
            return IBOOL.IN
        else:
            b1 = (Xm - self.B.ub()).is_subset(IntervalVector(2, Interval(-1000, 0)))
            b2 = (self.B.lb() - Xp).is_subset(IntervalVector(2, Interval(-1000, 0)))
            B1 = Xm - self.B.lb()
            B2 = self.B.ub() - Xp
            incl = False
            for i in range(0, self.B.size()):
                if B1[i].ub() < 0 or B2[i].ub() < 0:
                    incl = True
                    break
            if (b1 and b2) and incl:
                return IBOOL.MAYBE
            return IBOOL.UNK


def draw_axis(x_min, x_max, y_min, y_max):
    eps = 0.05
    vibes.drawArrow([x_min, y_min], [x_max, y_min], 0.1, 'w[w]')
    vibes.drawArrow([x_min, y_min], [x_min, y_max], 0.1, 'w[w]')
    for i in np.arange(0.5, x_max - x_min, 0.5):
        vibes.drawLine([[x_min + i, y_min - eps], [x_min + i, y_min + eps]], 'w')
    for i in np.arange(0.5, y_max - y_min, 0.5):
        vibes.drawLine([[x_min - eps, y_min + i], [x_min + eps, y_min + i]], 'w')


def testcase_2():
    vibes.beginDrawing()

    eps = 0.025

    X0 = IntervalVector([[-1.5, 3.5], [-1, 3]]).inflate(1)
    box = IntervalVector([[-1, 1], [0, 2]])

    vibes.newFigure('TestCase2')
    vibes.setFigureProperties(dict(x=0, y=10, width=500, height=500))
    L_clear, L_dark, L_penumbra, L_too_small = thickSIVIA(X0, TolUnSolSets(box), eps)
    draw_thickSIVIA_result(L_clear, L_dark, L_penumbra, L_too_small)

    draw_axis(-1.5, 3.5, -1, 3)

    vibes.drawLine([[-1.5, 0], [3.5, 0]], 'w')
    vibes.drawLine([[0, -1], [0, 3]], 'w')

    vibes.endDrawing()
