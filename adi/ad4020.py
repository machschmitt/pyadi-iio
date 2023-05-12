# Copyright (C) 2022-2024 Analog Devices, Inc.
#
# SPDX short identifier: ADIBSD

import numpy as np
from adi.attribute import attribute
from adi.context_manager import context_manager
from adi.rx_tx import rx


class ad4020(rx, context_manager):
    """AD40xx differential SAR ADC device"""

    _device_name = ""
    _compatible_parts = [
        "ad4003",
        "ad4007",
        "ad4011",
        "ad4020",
        "adaq4003",
    ]

    def __repr__(self):
        retstr = f"""
ad40xx(uri="{self.uri}") object "{self._device_name}"
AD4003/AD4007/AD4011, AD4020/AD4021/AD4022, and ADAQ4003 belong to a family of
differential SAR ADC devices.
"""
        return retstr

    _rx_data_type = np.int32
    _complex_data = False
    _rx_channel_names = ["voltage0"]

    def __init__(self, uri="", device_name=""):

        context_manager.__init__(self, uri, self._device_name)

        if device_name not in self._compatible_parts:
            raise Exception(
                "Not a compatible device: "
                + str(device_name)
                + ". Please select from "
                + str(self.self._compatible_parts)
            )
        else:
            self._ctrl = self._ctx.find_device(device_name)
            self._rxadc = self._ctx.find_device(device_name)

        # Dynamically get channel after the index
        for ch in self._ctrl.channels:
            name = ch._id
            output = ch._output
            setattr(self, name + "_adc", self._channel_adc(self._ctrl, name, output))

        rx.__init__(self)

    @property
    def sampling_frequency(self):
        """sample_rate
        """
        return self._get_iio_dev_attr("sampling_frequency")

    @sampling_frequency.setter
    def sampling_frequency(self, value):
        self._set_iio_dev_attr_str("sampling_frequency", value)

    class _channel_adc(attribute):
        """AD40xx Differential Input Voltage Channel"""

        # AD40xx ADC channel
        def __init__(self, ctrl, channel_name, output):
            self.name = channel_name
            self._ctrl = ctrl
            self._output = output

        @property
        def raw(self):
            return self._get_iio_attr(self.name, "raw", self._output)

        @property
        def scale(self):
            return float(self._get_iio_attr_str(self.name, "scale", self._output))

        def __call__(self, mV=None):
            """Convenience function, set / get voltages in SI units (millivolts)"""
            if mV is not None:
                self.raw = int(float(mV) / float(self.scale))
            return self.raw * self.scale
