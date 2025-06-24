"""
Test suites for AVR metadata extractors.
"""

# pylint: disable=line-too-long

import pathlib
import yaml

from extractors.avr import is_avr_datasheet, parse_pdf
from part import Part


def get_fixture_file(file: str) -> str:
    return str(pathlib.Path(__file__).parent.resolve()) + f"/fixtures/{file}"


def test_is_avr_datasheet():
    pdfs = [
        "http://ww1.microchip.com/downloads/en/DeviceDoc/ATmega328_P%20AVR%20MCU%20with%20picoPower%20Technology%20Data%20Sheet%2040001984A.pdf",
        "http://ww1.microchip.com/downloads/en/DeviceDoc/Atmel-2543-AVR-ATtiny2313_Datasheet.pdf",
        "http://ww1.microchip.com/downloads/en/DeviceDoc/atmel-2586-avr-8-bit-microcontroller-attiny25-attiny45-attiny85_datasheet.pdf",
        "http://ww1.microchip.com/downloads/en/DeviceDoc/ATtiny807_1607-Data-Sheet-40002030A.pdf",
    ]

    for pdf in pdfs:
        assert is_avr_datasheet(pdf) is True, pdf


def test_is_not_avr_datasheet():
    pdfs = [
        "http://arduino.cc/ATtiny807_1607-Data-Sheet-40002030A.pdf",
    ]

    for pdf in pdfs:
        assert is_avr_datasheet(pdf) is False, pdf


def test_parse_pdf():
    file_name = get_fixture_file("attiny2313.pdf")

    pins = parse_pdf(file_name)
    # print(pins)

    # PB7 (UCSK/SCL/PCINT7)
    # PD0 (RXD)
    # (TXD) PD1
    # (CKOUT/XCK/INT0) PD2
    # (XTAL1) PA0
    # (XTAL2) PA1
    assert pins["PB7"] == "UCSK/SCK/PCINT7".split("/")
    assert pins["PD0"] == "RXD".split("/")
    assert pins["PD1"] == "TXD".split("/")
    assert pins["PD2"] == "CKOUT/XCK/INT0".split("/")
    assert pins["PA0"] == "XTAL1".split("/")
    assert pins["PA1"] == "XTAL2".split("/")
    assert pins["PA2"] == "RESET/dW".split("/")


def test_enrich_attiny2313():
    attiny2313_yaml = """---
name: ATtiny2313V-10P
description: 10MHz, 2kB Flash, 128B SRAM, 128B EEPROM, debugWIRE, DIP-20
datasheet: http://ww1.microchip.com/downloads/en/DeviceDoc/Atmel-2543-AVR-ATtiny2313_Datasheet.pdf
footprint: Package_DIP:DIP-20_W7.62mm
pinout:
  '1':
    name: PA2/~{RESET}
    type: bidirectional
  '2':
    name: PD0
    type: bidirectional
  '3':
    name: PD1
    type: bidirectional
  '4':
    name: PA1/XTAL2
    type: bidirectional
  '5':
    name: PA0/XTAL1
    type: bidirectional
  '6':
    name: PD2
    type: bidirectional
  '7':
    name: PD3
    type: bidirectional
  '8':
    name: PD4
    type: bidirectional
  '9':
    name: PD5
    type: bidirectional
  '10':
    name: GND
    type: power_in
  '11':
    name: PD6
    type: bidirectional
  '12':
    name: PB0
    type: bidirectional
  '13':
    name: PB1
    type: bidirectional
  '14':
    name: PB2
    type: bidirectional
  '15':
    name: PB3
    type: bidirectional
  '16':
    name: PB4
    type: bidirectional
  '17':
    name: PB5
    type: bidirectional
  '18':
    name: PB6
    type: bidirectional
  '19':
    name: PB7
    type: bidirectional
  '20':
    name: VCC
    type: power_in
"""

    attiny2313 = Part.from_dict(yaml.safe_load(attiny2313_yaml))

    # https://www.msarnoff.org/chipdb/ATtiny2313
    print(attiny2313.pinout)
    assert attiny2313.pinout["1"].name == "PA2/~{RESET}"
    assert attiny2313.pinout["6"].name == "PD2"
    assert attiny2313.pinout["20"].name == "VCC"
