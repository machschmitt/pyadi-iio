# Copyright (C) 2023 Analog Devices, Inc.
#
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without modification,
# are permitted provided that the following conditions are met:
#     - Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     - Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in
#       the documentation and/or other materials provided with the
#       distribution.
#     - Neither the name of Analog Devices, Inc. nor the names of its
#       contributors may be used to endorse or promote products derived
#        from this software without specific prior written permission.
#     - The use of this software may or may not infringe the patent rights
#       of one or more patent holders.  This license does not release you
#       from the requirement that you obtain separate licenses from these
#       patent holders to use this software.
#     - Use of the software either in source or binary form, must be run
#       on or directly connected to an Analog Devices Inc. component.
#
# THIS SOFTWARE IS PROVIDED BY ANALOG DEVICES "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES,
# INCLUDING, BUT NOT LIMITED TO, NON-INFRINGEMENT, MERCHANTABILITY AND FITNESS FOR A
# PARTICULAR PURPOSE ARE DISCLAIMED.
#
# IN NO EVENT SHALL ANALOG DEVICES BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
# EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, INTELLECTUAL PROPERTY
# RIGHTS, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR
# BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT,
# STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF
# THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

from adi.attribute import attribute
from adi.context_manager import context_manager


class ad7091rx(context_manager):
    """AD7091R-2/AD7091R-4/AD7091R-8 SPI interface,
       2-/4-/8-channel, 12-bit SAR ADC"""

    _device_name = ""

    def __repr__(self):
        retstr = f"""
ad7091rx(uri="{self.uri}") object "{self._device_name}"
Analog I/O pins are configured in the device tree and can be ADC, DAC, or both.
Channel attributes are as follows, where X corresponds to device channel number:

voltageX_adc.raw:              Raw 12-bit ADC code. read only for ADC channels
voltageX_adc.scale:            ADC scale, millivolts per lsb
voltageX():                    Returns ADC reading in millivolts (read only)

"""
        return retstr

    def __init__(self, uri="", device_name=""):

        context_manager.__init__(self, uri, self._device_name)

        compatible_parts = [
            "ad7091r2",
            "ad7091r4",
            "ad7091r8",
        ]

        self.ctrl = None

        if not device_name:
            device_name = compatible_parts[0]
        else:
            if device_name not in compatible_parts:
                raise Exception("Not a compatible device: " + device_name)

        # Selecting the device matching device_name AD7091RX family as working device.
        for device in self._ctx.devices:
            if device.name in device_name:
                self._ctrl = device
                break

        # Dynamically get channels after the index
        for ch in self._ctrl.channels:
            name = ch._id
            output = ch._output
            setattr(self, name + "_adc", self._channel_adc(self._ctrl, name, output))

    class _channel_adc(attribute):
        """AD7091R-8/-4/-2 Input Voltage Channels"""

        # AD7091RX ADC channel
        def __init__(self, ctrl, channel_name, output):
            self.name = channel_name
            self._ctrl = ctrl
            self._output = output

        @property
        # AD7091RX channel raw value, property only for ADC channels
        def raw(self):
            return self._get_iio_attr(self.name, "raw", self._output)

        @property
        # AD7091RX channel scale (gain)
        def scale(self):
            return float(self._get_iio_attr_str(self.name, "scale", self._output))

        def __call__(self, mV=None):
            """Convenience function, set / get voltages in SI units (millivolts)"""
            if mV is not None:
                self.raw = int(float(mV) / float(self.scale))
            return self.raw * self.scale
