# Copyright 2018 Ace Monster Toys. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS-IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Wiegand based badge reader directly connected via GPIO
"""

from authbox.api import BasePinThread, GPIO
import bitstring

bits = bitstring.BitStream('0x0')
t = 15
timeout = t


class WiegandGPIOReader(BasePinThread):
  """Badge reader hardware abstraction.

  A Wiegand GPIO badge reader is defined in config as:

    [pins]
    name = WiegandGPIOReader:3:5

  where 3 is the D0 pin (physical numbering), and 5 is the D1 pin (also 
  hysical numbering).
  """
  def __init__(self, event_queue, config_name, d0_pin, d1_pin, bit_len=26, on_scan=None):
    super(WiegandGPIOReader, self).__init__(event_queue, config_name)
    self._on_scan = on_scan
    if self._on_scan:
        GPIO.add_event_detect(d0_pin, GPIO.FALLING, callback=self._callback)
        GPIO.add_event_detect(d1_pin, GPIO.FALLING, callback=self._callback)


  def _callback(self, unused_channel):
    """Wrapper to queue events instead of calling them directly."""
    if self._on_scan:
      self.event_queue.put((self._on_scan, self))

  def decode(self, channel):
      global bits
      global timeout
      if channel == self.d0_pin:
          bits.append('0b0')
      elif channel == self.d1_pin:
          bits.append('0b1')
      timeout = t


  def read_input(self):
    """

    Args:
      device: input device to listen to

    Returns:
      badge value as string
    """
    global bits
    global timeout

    rfid = ''
    print "About to read_input"
    while 1:
        if bits:
            timeout = timeout -1
            time.sleep(0.001)
            if len(bits) > 1 and timeout == 0:
                #print "Binary:",bits
                #result = int(str(bits[1:26]),2)
                print('Bits is {} bits in length'.format(len(bits)))
                print('{:012X}'.format(bits[-25:-1].int))
                print('{0:30b}'.format(bits[-25:-1].int))
                bits = bitstring.BitStream('0x0')
        else:
            time.sleep(0.001)

    print "Badge read:", rfid
    return rfid

  def run_inner(self):
    line = self.read_input()
    self.event_queue.put((self._on_scan, line))
