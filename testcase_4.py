from pyibex import *
from thickSIVIA import *
from vibes import vibes


class CommArea:
    def __init__(self, m):
        self.l_m = m
        self.Bp = IntervalVector(len(m), [0, 20 ** 2])
        self.Bm = IntervalVector(len(m), [0, 10 ** 2])

    def test(self, X):
        Xm = IntervalVector(len(self.l_m))
        Xp = IntervalVector(len(self.l_m))

        for i, m in enumerate(self.l_m):
            Xm[i] = max(
                Interval(0),
                sign((X[0] - m[0].ub()) * (X[0] - m[0].lb()))
            ) * min(
                sqr(X[0] - m[0].lb()), sqr(X[0] - m[0].ub())
            ) + max(
                Interval(0),
                sign((X[1] - m[1].ub()) * (X[1] - m[1].lb()))
            ) * min(
                sqr(X[1] - m[1].lb()), sqr(X[1] - m[1].ub())
            )

            Xp[i] = max(
                sqr(X[0] - m[0].lb()), sqr(X[0] - m[0].ub())
            ) + max(
                sqr(X[1] - m[1].lb()), sqr(X[1] - m[1].ub())
            )

        Xub = Xm | Xp

        if self.Bp.is_disjoint(Xub):
            return IBOOL.OUT
        elif Xub.is_subset(self.Bm):
            return IBOOL.IN
        else:
            b1 = (Xm - IntervalVector(self.Bp.ub())).is_subset(IntervalVector(len(self.l_m), Interval(-1000, 0)))
            b2 = (IntervalVector(self.Bp.lb()) - Xp).is_subset(IntervalVector(len(self.l_m), Interval(-1000, 0)))
            B1 = Xm - IntervalVector(self.Bm.lb())
            B2 = IntervalVector(self.Bm.ub()) - Xp
            incl = False
            for i in range(0, len(self.l_m)):
                if B1[i].ub() < 0 or B2[i].ub() < 0:
                    incl = True
                    break
            if (b1 and b2) and incl:
                return IBOOL.MAYBE
            return IBOOL.UNK


def testcase_4():
    vibes.beginDrawing()

    eps = 0.5

    X0 = IntervalVector(2, [-20, 20])

    m = [
        [Interval(1).inflate(0.5), Interval(3).inflate(0.5)],
        [Interval(10).inflate(0.5), Interval(-1).inflate(0.5)],
        [Interval(10).inflate(0.5), Interval(6).inflate(0.5)],
        [Interval(-2).inflate(0.5), Interval(-5).inflate(0.5)]
    ]

    vibes.newFigure('TestCase4')
    vibes.setFigureProperties(dict(x=0, y=10, width=500, height=500))
    L_clear, L_dark, L_penumbra, L_too_small = thickSIVIA(X0, CommArea(m), eps)
    draw_thickSIVIA_result(L_clear, L_dark, L_penumbra, L_too_small)

    for item in m:
        vibes.drawCircle(item[0].mid(), item[1].mid(), 0.2, '[k]')
        vibes.drawBox(item[0][0], item[0][1], item[1][0], item[1][1], '[k]')

    vibes.drawArrow([-15, -15], [-15, -10], 1, 'w[w]')
    vibes.drawArrow([-15, -15], [-10, -15], 1, 'w[w]')
    vibes.endDrawing()
