#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

from tsl2561 import TSL2561

'''Driver for the TSL2561 digital luminosity (light) sensors.

Pick one up at http://www.adafruit.com/products/439

Adafruit invests time and resources providing this open source code,
please support Adafruit and open-source hardware by purchasing
products from Adafruit!

Code ported from Adafruit Arduino library,
commit ced9f731da5095988cd66158562c2fde659e0510:
https://github.com/adafruit/Adafruit_TSL2561
'''


if __name__ == "__main__":
    tsl = TSL2561(debug=True)

    print(tsl.lux())
