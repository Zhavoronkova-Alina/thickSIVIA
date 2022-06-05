from pyibex import *
from thickSIVIA import *
from vibes import vibes


# Parametric model
# y_m (x, t) = x_1 * exp( -x_2 * t ),
# where x = (x_1, x_2) is the parameter vector, and t (in R) is the time
# ---------------------------
# i |     [t_i]    |  [y_i]
# ---------------------------
# 1 | [0.03, 0.06] | [4, 8]
# 2 | [0.09, 0.12] | [2, 6]
# 3 | [0.15, 0.18] | [2, 5]
# 4 | [0.21, 0.24] | [1, 3]
# 5 | [0.27, 0.3 ] | [0, 2]


class ParamEstimation:
    def __init__(self, t, y, is_classic=False):
        self.t = t
        self.y = y
        self.is_classic = is_classic

    def test(self, X):
        Xm = IntervalVector(len(self.t))
        Xp = IntervalVector(len(self.t))

        for i in range(0, len(self.t)):
            Xm[i] = X[0] * exp(-max(X[1] * self.t[i].lb(), X[1] * self.t[i].ub()))
            Xp[i] = X[0] * exp(-min(X[1] * self.t[i].lb(), X[1] * self.t[i].ub()))

        Xub = Xm | Xp

        if self.y.is_disjoint(Xub):
            return IBOOL.OUT
        elif Xub.is_subset(self.y):
            return IBOOL.IN
        else:
            if self.is_classic:
                return IBOOL.UNK
            b1 = (Xm - IntervalVector(self.y.ub())).is_subset(IntervalVector(len(self.t), Interval(-1000, 0)))
            b2 = (IntervalVector(self.y.lb()) - Xp).is_subset(IntervalVector(len(self.t), Interval(-1000, 0)))
            B1 = Xm - IntervalVector(self.y.lb())
            B2 = IntervalVector(self.y.ub()) - Xp
            incl = False
            for i in range(0, len(self.t)):
                if B1[i].ub() < 0 or B2[i].ub() < 0:
                    incl = True
                    break
            if (b1 and b2) and incl:
                return IBOOL.MAYBE
            return IBOOL.UNK


def testcase_3():
    vibes.beginDrawing()

    eps = 0.1

    X0 = IntervalVector([[2, 20], [-2, 16]])

    l_ti = [[0.03, 0.06], [0.09, 0.12], [0.15, 0.18], [0.21, 0.24], [0.27, 0.3]]
    l_yi = [[4, 8], [2, 6], [2, 5], [1, 3], [0, 2]]

    ti, yi = map(IntervalVector, [l_ti, l_yi])

    vibes.newFigure('TestCase2')
    vibes.setFigureProperties(dict(x=0, y=10, width=500, height=500))
    L_clear, L_dark, L_penumbra, L_too_small = thickSIVIA(X0, ParamEstimation(ti, yi), eps)
    draw_thickSIVIA_result(L_clear, L_dark, L_penumbra, L_too_small)

    vibes.newFigure('TestCase2 Classic Intervals')
    vibes.setFigureProperties(dict(x=0, y=10, width=500, height=500))
    L_clear, L_dark, L_penumbra, L_too_small = thickSIVIA(X0, ParamEstimation(ti, yi, True), eps)
    draw_thickSIVIA_result(L_clear, L_dark, L_penumbra, L_too_small)

    vibes.endDrawing()
