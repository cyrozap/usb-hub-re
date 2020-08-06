meta:
  id: vl81x_fw
  endian: be
  title: VIA Labs VL81x Firmware Image
  license: CC0-1.0
seq:
  - id: device_id
    type: u2
    enum: device_ids
  - id: unk1
    type: u2
  - id: usb3
    type: code_region
  - id: usb2
    type: code_region
  - id: unk2
    size: 16
  - id: unk3
    type: u2
  - id: unk4
    type: u2
instances:
  header_checksum:
    pos: 2
    type: u1
    if: device_id == device_ids::vl812
    doc: "XOR of all the header bytes, excluding this one."
enums:
  device_ids:
    0x0921: vl810
    0x0d08: vl811
    0x0d12: vl812  # Also VL811+
types:
  code_region:
    seq:
      - id: offset
        type: u2
      - id: code_len
        type: u2
    instances:
      code_and_checksum:
        io: _root._io
        pos: offset
        size: code_len + 1
        type: code_and_checksum
  code_and_checksum:
    seq:
      - id: code
        size: _io.size - 1
      - id: checksum
        type: u1
        doc: "XOR of all the code bytes."
