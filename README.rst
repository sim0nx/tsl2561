.. image:: https://landscape.io/github/sim0nx/tsl2561/master/landscape.svg?style=flat
   :target: https://landscape.io/github/sim0nx/tsl2561/master
   :alt: Code Health

.. image:: https://badge.fury.io/py/tsl2561.svg
   :target: https://badge.fury.io/py/tsl2561
   :alt: PyPI version


Python library for TSL2561
==========================
  This is python library for working with Adafruit's TSL2561 luminosity sensor.

Requirements
------------
  - Python 2.7 or Python 3.x
  - Adafruit GPIO library (https://github.com/adafruit/Adafruit_Python_GPIO)
  - Adafruit PureIO library (https://github.com/adafruit/Adafruit_Python_PureIO)

Installation
------------
Install the latest version using pip:

.. code-block:: bash

  pip install tsl2561


Example
-------

.. code-block:: python

  from tsl2561 import TSL2561


  if __name__ == "__main__":
    tsl = TSL2561(debug=True)
    print(tsl.lux())

License
=======
Copyright (c) 2015 Kevin Townsend for Adafruit Industries.
All rights reserved.

Copyright (c) 2016-present, Georges Toth
All rights reserved.


Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:
1. Redistributions of source code must retain the above copyright
notice, this list of conditions and the following disclaimer.
2. Redistributions in binary form must reproduce the above copyright
notice, this list of conditions and the following disclaimer in the
documentation and/or other materials provided with the distribution.
3. Neither the name of the copyright holders nor the
names of its contributors may be used to endorse or promote products
derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS ''AS IS'' AND ANY
EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER BE LIABLE FOR ANY
DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
