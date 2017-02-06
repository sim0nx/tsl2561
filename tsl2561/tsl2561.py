#!/usr/bin/env python
from future import absolute_import, division, print_function, unicode_literals
'''Driver for the TSL2561 digital luminosity (light) sensors.

Pick one up at http://www.adafruit.com/products/439

Adafruit invests time and resources providing this open source code,
please support Adafruit and open-source hardware by purchasing
products from Adafruit!

Code ported from Adafruit Arduino library,
commit ced9f731da5095988cd66158562c2fde659e0510:
https://github.com/adafruit/Adafruit_TSL2561
'''

from __future__ import absolute_import
import time
from Adafruit_GPIO import I2C
from tsl2561.constants import *  # pylint: disable=unused-wildcard-import

__author__ = 'Georges Toth <georges@trypill.org>'
__credits__ = ['K.Townsend (Adafruit Industries)', 'Yongwen Zhuang (zYeoman)', 'miko (mikostn)', 'Simon Gansen (theFork)']
__license__ = 'BSD'
__version__ = 'v3.0'

'''HISTORY
v3.0 - Port to Python 3.x
v2.2 - Merge PR #4 regarding wrong use of integration time
v2.1 - Minor adaptations required by latest Adafruit pyton libraries
v2.0 - Rewrote driver for Adafruit_Sensor and Auto-Gain support, and
       added lux clipping check (returns 0 lux on sensor saturation)
v1.0 - First release (previously TSL2561)
'''


class TSL2561(object):
    '''Driver for the TSL2561 digital luminosity (light) sensors.'''
    def __init__(self, address=None, busnum=None,
                 integration_time=TSL2561_INTEGRATIONTIME_402MS,
                 gain=TSL2561_GAIN_1X, autogain=False, debug=False):

        # Set default address and bus number if not given
        if address is not None:
            self.address = address
        else:
            self.address = TSL2561_ADDR_FLOAT
        if busnum is None:
            self.busnum = 1

        self.i2c = I2C.get_i2c_device(self.address, busnum=busnum)

        self.debug = debug
        self.integration_time = integration_time
        self.gain = gain
        self.autogain = autogain

        if self.integration_time == TSL2561_INTEGRATIONTIME_402MS:
            self.delay_time = TSL2561_DELAY_INTTIME_402MS
        elif self.integration_time == TSL2561_INTEGRATIONTIME_101MS:
            self.delay_time = TSL2561_DELAY_INTTIME_101MS
        elif self.integration_time == TSL2561_INTEGRATIONTIME_13MS:
            self.delay_time = TSL2561_DELAY_INTTIME_13MS
        self._begin()

    def _begin(self):
        '''Initializes I2C and configures the sensor (call this function before
        doing anything else)
        '''
        # Make sure we're actually connected
        x = self.i2c.readU8(TSL2561_REGISTER_ID)

        if not x & 0x0A:
            raise Exception('TSL2561 not found!')
        ##########

        # Set default integration time and gain
        self.set_integration_time(self.integration_time)
        self.set_gain(self.gain)

        # Note: by default, the device is in power down mode on bootup
        self.disable()

    def enable(self):
        '''Enable the device by setting the control bit to 0x03'''
        self.i2c.write8(TSL2561_COMMAND_BIT | TSL2561_REGISTER_CONTROL,
                        TSL2561_CONTROL_POWERON)

    def disable(self):
        '''Disables the device (putting it in lower power sleep mode)'''
        self.i2c.write8(TSL2561_COMMAND_BIT | TSL2561_REGISTER_CONTROL,
                        TSL2561_CONTROL_POWEROFF)

    @staticmethod
    def delay(value):
        '''Delay times must be specified in milliseconds but as the python
        sleep function only takes (float) seconds we need to convert the sleep
        time first
        '''
        time.sleep(value / 1000.0)

    def _get_data(self):
        '''Private function to read luminosity on both channels'''

        # Enable the device by setting the control bit to 0x03
        self.enable()

        # Wait x ms for ADC to complete
        TSL2561.delay(self.delay_time)

        # Reads a two byte value from channel 0 (visible + infrared)
        broadband = self.i2c.readU16(TSL2561_COMMAND_BIT | TSL2561_WORD_BIT |
                                     TSL2561_REGISTER_CHAN0_LOW)

        # Reads a two byte value from channel 1 (infrared)
        ir = self.i2c.readU16(TSL2561_COMMAND_BIT | TSL2561_WORD_BIT |
                              TSL2561_REGISTER_CHAN1_LOW)

        # Turn the device off to save power
        self.disable()

        return (broadband, ir)

    def set_integration_time(self, integration_time):
        '''Sets the integration time for the TSL2561'''

        # Enable the device by setting the control bit to 0x03
        self.enable()

        self.integration_time = integration_time

        # Update the timing register
        self.i2c.write8(TSL2561_COMMAND_BIT | TSL2561_REGISTER_TIMING,
                        self.integration_time | self.gain)

        # Turn the device off to save power
        self.disable()

    def set_gain(self, gain):
        '''Adjusts the gain on the TSL2561 (adjusts the sensitivity to light)
        '''

        # Enable the device by setting the control bit to 0x03
        self.enable()

        self.gain = gain

        # Update the timing register
        self.i2c.write8(TSL2561_COMMAND_BIT | TSL2561_REGISTER_TIMING,
                        self.integration_time | self.gain)

        # Turn the device off to save power
        self.disable()

    def set_auto_range(self, value):
        '''Enables or disables the auto-gain settings when reading
        data from the sensor
        '''
        self.autogain = value

    def _get_luminosity(self):
        '''Gets the broadband (mixed lighting) and IR only values from
        the TSL2561, adjusting gain if auto-gain is enabled
        '''
        valid = False

        # If Auto gain disabled get a single reading and continue
        if not self.autogain:
            return self._get_data()

        # Read data until we find a valid range
        _agcCheck = False
        broadband = 0
        ir = 0

        while not valid:
            if self.integration_time == TSL2561_INTEGRATIONTIME_13MS:
                _hi = TSL2561_AGC_THI_13MS
                _lo = TSL2561_AGC_TLO_13MS
            elif self.integration_time == TSL2561_INTEGRATIONTIME_101MS:
                _hi = TSL2561_AGC_THI_101MS
                _lo = TSL2561_AGC_TLO_101MS
            else:
                _hi = TSL2561_AGC_THI_402MS
                _lo = TSL2561_AGC_TLO_402MS

            _b, _ir = self._get_data()

            # Run an auto-gain check if we haven't already done so ...
            if not _agcCheck:
                if _b < _lo and self.gain == TSL2561_GAIN_1X:
                    # Increase the gain and try again
                    self.set_gain(TSL2561_GAIN_16X)
                    # Drop the previous conversion results
                    _b, _ir = self._get_data()
                    # Set a flag to indicate we've adjusted the gain
                    _agcCheck = True
                elif _b > _hi and self.gain == TSL2561_GAIN_16X:
                    # Drop gain to 1x and try again
                    self.set_gain(TSL2561_GAIN_1X)
                    # Drop the previous conversion results
                    _b, _ir = self._get_data()
                    # Set a flag to indicate we've adjusted the gain
                    _agcCheck = True
                else:
                    # Nothing to look at here, keep moving ....
                    # Reading is either valid, or we're already at the chips
                    # limits
                    broadband = _b
                    ir = _ir
                    valid = True
            else:
                # If we've already adjusted the gain once, just return the new
                # results.
                # This avoids endless loops where a value is at one extreme
                # pre-gain, and the the other extreme post-gain
                broadband = _b
                ir = _ir
                valid = True

        return (broadband, ir)

    def _calculate_lux(self, broadband, ir):
        '''Converts the raw sensor values to the standard SI lux equivalent.
        Returns 0 if the sensor is saturated and the values are unreliable.
        '''
        # Make sure the sensor isn't saturated!
        if self.integration_time == TSL2561_INTEGRATIONTIME_13MS:
            clipThreshold = TSL2561_CLIPPING_13MS
        elif self.integration_time == TSL2561_INTEGRATIONTIME_101MS:
            clipThreshold = TSL2561_CLIPPING_101MS
        else:
            clipThreshold = TSL2561_CLIPPING_402MS

        # Return 0 lux if the sensor is saturated
        if broadband > clipThreshold or ir > clipThreshold:
            raise Exception('Sensor is saturated')

        # Get the correct scale depending on the integration time
        if self.integration_time == TSL2561_INTEGRATIONTIME_13MS:
            chScale = TSL2561_LUX_CHSCALE_TINT0
        elif self.integration_time == TSL2561_INTEGRATIONTIME_101MS:
            chScale = TSL2561_LUX_CHSCALE_TINT1
        else:
            chScale = 1 << TSL2561_LUX_CHSCALE

        # Scale for gain (1x or 16x)
        if not self.gain:
            chScale = chScale << 4

        # Scale the channel values
        channel0 = (broadband * chScale) >> TSL2561_LUX_CHSCALE
        channel1 = (ir * chScale) >> TSL2561_LUX_CHSCALE

        # Find the ratio of the channel values (Channel1/Channel0)
        ratio1 = 0
        if channel0 != 0:
            ratio1 = (channel1 << (TSL2561_LUX_RATIOSCALE + 1)) / channel0

        # round the ratio value
        ratio = (int(ratio1) + 1) >> 1

        b = 0
        m = 0

        if ratio >= 0 and ratio <= TSL2561_LUX_K1T:
            b = TSL2561_LUX_B1T
            m = TSL2561_LUX_M1T
        elif ratio <= TSL2561_LUX_K2T:
            b = TSL2561_LUX_B2T
            m = TSL2561_LUX_M2T
        elif ratio <= TSL2561_LUX_K3T:
            b = TSL2561_LUX_B3T
            m = TSL2561_LUX_M3T
        elif ratio <= TSL2561_LUX_K4T:
            b = TSL2561_LUX_B4T
            m = TSL2561_LUX_M4T
        elif ratio <= TSL2561_LUX_K5T:
            b = TSL2561_LUX_B5T
            m = TSL2561_LUX_M5T
        elif ratio <= TSL2561_LUX_K6T:
            b = TSL2561_LUX_B6T
            m = TSL2561_LUX_M6T
        elif ratio <= TSL2561_LUX_K7T:
            b = TSL2561_LUX_B7T
            m = TSL2561_LUX_M7T
        elif ratio > TSL2561_LUX_K8T:
            b = TSL2561_LUX_B8T
            m = TSL2561_LUX_M8T

        temp = (channel0 * b) - (channel1 * m)

        # Do not allow negative lux value
        if temp < 0:
            temp = 0

        # Round lsb (2^(LUX_SCALE-1))
        temp += 1 << (TSL2561_LUX_LUXSCALE - 1)

        # Strip off fractional portion
        lux = temp >> TSL2561_LUX_LUXSCALE

        # Signal I2C had no errors
        return lux

    def lux(self):
        '''Read sensor data, convert it to LUX and return it'''
        broadband, ir = self._get_luminosity()
        return self._calculate_lux(broadband, ir)


if __name__ == "__main__":
    tsl = TSL2561(debug=True)

    print(tsl.lux())
