from pyibex import Interval, IntervalVector, max, min, sqr, sign
from thickSIVIA import *
from vibes import vibes
from testcase_1 import ThickDisk

def testcase_0():
    vibes.beginDrawing()

    X0 = IntervalVector(2, [-2.5, 3.5])

    # vibes.newFigure('TestCase0')
    # vibes.setFigureProperties(dict(x=0, y=10, width=500, height=500))
    # L_clear, L_dark, L_penumbra, L_too_small = thickSIVIA(X0, ThickDisk(Interval(0, 1), Interval(0, 1), 2, 2), 0.1)
    # draw_thickSIVIA_result(L_clear, L_dark, L_penumbra, L_too_small)
    # vibes.drawBox(0, 1, 0, 1, '[k]')

    vibes.newFigure('TestCase0_thin')
    vibes.setFigureProperties(dict(x=0, y=10, width=500, height=500))
    L_clear, L_dark, L_penumbra, L_too_small = thickSIVIA(X0, ThickDisk(Interval(0, 1), Interval(0, 1), 2, 2, True), 0.1)
    draw_thickSIVIA_result(L_clear, L_dark, L_penumbra, L_too_small)
    vibes.drawBox(0, 1, 0, 1, '[k]')

    vibes.endDrawing()
