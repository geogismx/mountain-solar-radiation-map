# -*- coding: cp936 -*-
import os
import datetime
import math


def JMonth(Julian ,JulDay):
    I = 1
    if Julian == 365:
        I = 0
    if JulDay <=31:
        MM = 1
    elif JulDay <= 59 + I:
        MM = 2
    elif JulDay <= 90 + I:
        MM = 3
    elif JulDay <= 120 + I:
        MM = 4
    elif JulDay <= 151 + I:
        MM = 5
    elif JulDay <= 181 + I:
        MM = 6
    elif JulDay <= 212 + I:
        MM = 7
    elif JulDay <= 243 + I:
        MM = 8
    elif JulDay <= 273 + I:
        MM = 9
    elif JulDay <= 304 + I:
        MM = 10
    elif JulDay <= 334 + I:
        MM = 11
    else:
        MM = 12
    return MM