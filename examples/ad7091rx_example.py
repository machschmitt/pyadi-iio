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
#       from this software without specific prior written permission.
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

import sys

import adi

# Optionally pass URI as command line argument, else use analog.local
# (URI stands for "Uniform Resource Identifier")
# Optionally pass device name argument.
my_uri = sys.argv[1] if len(sys.argv) >= 2 else "ip:analog.local"
dev_name = sys.argv[2] if len(sys.argv) >= 3 else "ad7091r-8"

print("uri: " + str(my_uri))
print("dev_name: " + str(dev_name))

# Set up AD7091R-2/AD7091R-4/AD7091R-8 from specific uri address and device name.
my_ad7091rx = adi.ad7091rx(uri=my_uri, device_name=dev_name)

# Create iterable list of channels. This is only for test purposes in the example,
# where the channel configuration is not known ahead of time.
channels = []
for attr in dir(my_ad7091rx):
    if type(getattr(my_ad7091rx, attr)) in (adi.ad7091rx._channel_adc,):
        channels.append(getattr(my_ad7091rx, attr))

# Read each channels and its parameters
for ch in channels:
    print("***********************")  # Just a separator for easier serial read
    print("Channel Name: ", ch.name)  # Channel Name
    print("Channel Scale: ", ch.scale)  # Channel Scale is Vref/2^12
    print("Channel Raw Value: ", ch.raw)  # Channel Raw Value

    # Print Real Voltage in mV
    print(
        "Channel Real Value (mV): ", ch()
    )  # Use channel's call method, which returns millivolts.
