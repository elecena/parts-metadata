"""
Test suites for the code that provides extra pinout for the parts.
"""

import pathlib
import responses
import yaml

from enrich_part import enrich_part
from part import Part


def get_fixture_file(file: str) -> str:
    return str(pathlib.Path(__file__).parent.resolve()) + f"/fixtures/{file}"


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
    # print(attiny2313.pinout)
    assert attiny2313.name == "ATtiny2313V-10P"
    assert attiny2313.pinout["1"].name == "PA2/~{RESET}"
    assert attiny2313.pinout["6"].name == "PD2"
    assert attiny2313.pinout["20"].name == "VCC"

    with responses.RequestsMock() as http_mock:
        with open(get_fixture_file("attiny2313.pdf"), "rb") as pdf_file:
            http_mock.get(attiny2313.datasheet, body=pdf_file.read())
            enrich_part(attiny2313)

    # PB7 (UCSK/SCK/PCINT7)
    # PD0 (RXD)
    # (TXD) PD1
    # (CKOUT/XCK/INT0) PD2
    # (XTAL1) PA0
    # (XTAL2) PA1
    assert attiny2313.name == "ATtiny2313V-10P"
    assert attiny2313.pinout["1"].name == "PA2"
    assert attiny2313.pinout["1"].alt_funcs == "RESET/dW".split("/")
    assert attiny2313.pinout["5"].name == "PA0"
    assert attiny2313.pinout["5"].alt_funcs == "XTAL1".split("/")
    assert attiny2313.pinout["19"].name == "PB7"
    assert attiny2313.pinout["19"].alt_funcs == "UCSK/SCK/PCINT7".split("/")

    yaml_output = attiny2313.as_yaml()
    # print(yaml_output)
    assert (
        """
  '17':
    name: PB5
    type: bidirectional
    alt_funcs:
    - MOSI
    - DI
    - SDA
    - PCINT5
"""
        in yaml_output
    )

    assert (
        """
  '19':
    name: PB7
    type: bidirectional
    alt_funcs:
    - UCSK
    - SCK
    - PCINT7
"""
        in yaml_output
    )
