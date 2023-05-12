# Copyright (C) 2022 Analog Devices, Inc.
#
# SPDX short identifier: ADIBSD


import sys

import adi
import matplotlib.pyplot as plt
import numpy as np
from scipy import signal

# dev_name = "ad4020"
dev_name = "adaq4003"

# Optionally pass URI as command line argument,
# else use default context manager search
my_uri = sys.argv[1] if len(sys.argv) >= 2 else "ip:analog.local"
print("uri: " + str(my_uri))

my_adc = adi.ad4020(uri=my_uri, device_name=dev_name)
print("Using " + dev_name.upper())

my_adc.rx_buffer_size = 4096
# my_adc.rx_buffer_size = 16000

print("Sample Rate: ", my_adc.sampling_frequency)

data = my_adc.rx()

x = np.arange(0, len(data))
# voltage = data * my_adc.voltage0_adc.scale
voltage = data * 0.04201208442318
dc = np.average(voltage)  # Extract DC component
ac = voltage - dc  # Extract AC component

plt.figure(1)
plt.clf()
plt.title(dev_name.upper() + " Time Domain Data")
plt.plot(x, voltage)
plt.xlabel("Data Point")
plt.ylabel("Voltage (mV)")
plt.show()

f, Pxx_spec = signal.periodogram(
    ac, my_adc.sampling_frequency, window="flattop", scaling="spectrum"
)
Pxx_abs = np.sqrt(Pxx_spec)

plt.figure(2)
plt.clf()
plt.title(dev_name.upper() + " Spectrum (Volts absolute)")
plt.semilogy(f, Pxx_abs)
plt.ylim([1e-6, 4])
plt.xlabel("frequency [Hz]")
plt.ylabel("Voltage (mV)")
plt.draw()
plt.pause(0.05)

del my_adc
