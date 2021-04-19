import numpy as np
from utils import *


def boxPattern(daily_high, daily_low):
    # find local max and min, first order
    locArr = np.arange(len(daily_high))
    max_x, max_y = findLocalExtreme(locArr, daily_high, "max")
    max_xx, max_yy = findLocalExtreme(max_x, max_y, "max")
    # second order
    min_x, min_y = findLocalExtreme(locArr, daily_low, "min")
    min_xx, min_yy = findLocalExtreme(min_x, min_y, "min")

    # return signals
    signals = findBoxPatterns(min_xx, min_yy, max_xx, max_yy)
    return signals