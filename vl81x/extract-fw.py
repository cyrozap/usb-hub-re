#!/usr/bin/env python3
# SPDX-License-Identifier: 0BSD

# Copyright (C) 2020 by Forest Crossman <cyrozap@gmail.com>
#
# Permission to use, copy, modify, and/or distribute this software for
# any purpose with or without fee is hereby granted.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL
# WARRANTIES WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE
# AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL
# DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR
# PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER
# TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR
# PERFORMANCE OF THIS SOFTWARE.


import argparse
import sys

from functools import reduce

try:
    import vl81x_fw
except ModuleNotFoundError:
    print("Error: Failed to import \"vl81x_fw.py\". Please run \"make\" in this directory to generate that file, then try running this script again.", file=sys.stderr)
    sys.exit(1)


DEVICE_ID_MAP = {
    vl81x_fw.Vl81xFw.DeviceIds.vl810: "VL810",
    vl81x_fw.Vl81xFw.DeviceIds.vl811: "VL811",
    vl81x_fw.Vl81xFw.DeviceIds.vl812: "VL811+/VL812",
}


def checksum(data):
    return reduce(int.__xor__, data)

def validate_checksum(name, data, expected):
    calc_csum = checksum(data)
    exp_csum = expected
    if calc_csum != exp_csum:
        print("Error: Invalid {} checksum: expected {:#04x}, got: {:#04x}".format(name, exp_csum, calc_csum), file=sys.stderr)
        sys.exit(1)
    print("{} checksum OK!".format(name))

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("firmware", type=str, help="The firmware binary.")
    args = parser.parse_args()

    split = args.firmware.split('.')
    ext = split[-1]
    basename = '.'.join(split[:-1])

    fw_bytes = open(args.firmware, 'rb').read()
    fw = vl81x_fw.Vl81xFw.from_bytes(fw_bytes)
    print("Chip: {}".format(DEVICE_ID_MAP.get(fw.device_id, "Unknown")))

    regions = (
        ("USB2", fw.usb2),
        ("USB3", fw.usb3),
    )
    for (name, region) in regions:
        if region.code_len > 0:
            code = region.code_and_checksum.code
            csum = region.code_and_checksum.checksum
            validate_checksum(name, code, csum)

            open("{}.{}.{}".format(basename, name.lower(), ext), 'wb').write(code)


if __name__ == "__main__":
        main()
