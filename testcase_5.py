from pyibex import *
from thickSIVIA import *
from vibes import vibes

SQR = Function("x1", "x2", "(max(0, sign(x1 * x2) * min(x1^2, x2^2)), max(x1^2, x2^2))")
MINUS = Function("x1", "x2", "y1", "y2", "(x1 - y2, x2 - y1)")
PLUS = Function("x1", "x2", "y1", "y2", "(x1 + y1, x2 + y2)")


class Location:
    def __init__(self, m):
        self.l_m = m
        self.Bp = IntervalVector(len(m), [0, 20 ** 2])

    def test(self, X):
        Xm = IntervalVector(len(self.l_m))
        Xp = IntervalVector(len(self.l_m))

        for i, m in enumerate(self.l_m):
            dX0 = MINUS.eval_vector(IntervalVector([
                [X[0].lb(), X[0].ub()],
                [X[0].lb(), X[0].ub()],
                [m[0].lb(), m[0].lb()],
                [m[0].ub(), m[0].ub()]
            ]))

            dX1 = MINUS.eval_vector(IntervalVector([
                [X[1].lb(), X[1].ub()],
                [X[1].lb(), X[1].ub()],
                [m[1].lb(), m[1].lb()],
                [m[1].ub(), m[1].ub()]
            ]))

            S0 = SQR.eval_vector(IntervalVector([
                [dX0[0].lb(), dX0[0].ub()],
                [dX0[1].lb(), dX0[1].ub()]
            ]))

            S1 = SQR.eval_vector(IntervalVector([
                [dX1[0].lb(), dX1[0].ub()],
                [dX1[1].lb(), dX1[1].ub()]
            ]))

            N2 = PLUS.eval_vector(IntervalVector([
                [S0[0].lb(), S0[0].ub()],
                [S0[1].lb(), S0[1].ub()],
                [S1[0].lb(), S1[0].ub()],
                [S1[1].lb(), S1[1].ub()]
            ]))

            Xm[i], Xp[i] = N2[0], N2[1]

        Xub = Xm | Xp

        if self.Bp.is_disjoint(Xub):
            return IBOOL.OUT
        elif Xub.is_subset(self.Bp):
            return IBOOL.IN
        else:
            b1 = (Xm - IntervalVector(self.Bp.ub())).is_subset(IntervalVector(len(self.l_m), Interval(-1000, 0)))
            b2 = (IntervalVector(self.Bp.lb()) - Xp).is_subset(IntervalVector(len(self.l_m), Interval(-1000, 0)))
            B1 = (Xm - IntervalVector(self.Bp.lb()))
            B2 = (IntervalVector(self.Bp.ub()) - Xp)
            incl = False
            for i in range(0, len(self.l_m)):
                if B1[i].ub() < 0 or B2[i].ub() < 0:
                    incl = True
                    break
            if (b1 and b2) and incl:
                return IBOOL.MAYBE
            return IBOOL.UNK


def testcase_5():
    vibes.beginDrawing()

    eps = 0.5

    X0 = IntervalVector(2, [-30, 30])

    m = [
        [Interval(-1, 3), Interval(1, 5)],
        [Interval(8, 12), Interval(-3, 1)],
        [Interval(8, 12), Interval(4, 8)]
    ]

    vibes.newFigure('TestCase5')
    vibes.setFigureProperties(dict(x=0, y=10, width=500, height=500))
    L_clear, L_dark, L_penumbra, L_too_small = thickSIVIA(X0, Location(m), eps)
    draw_thickSIVIA_result(L_clear, L_dark, L_penumbra, L_too_small)

    for item in m:
        vibes.drawCircle(item[0].mid(), item[1].mid(), 0.2, '[k]')
        vibes.drawBox(item[0][0], item[0][1], item[1][0], item[1][1], '[k]')

    vibes.drawArrow([-15, -15], [-15, -10], 1, 'w[w]')
    vibes.drawArrow([-15, -15], [-10, -15], 1, 'w[w]')
    vibes.endDrawing()
