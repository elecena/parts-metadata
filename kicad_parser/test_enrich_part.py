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
    with open(get_fixture_file("attiny2313.yml"), "rt") as yaml_file:
        attiny2313_yaml = yaml_file.read()

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
  '16':
    name: PB4
    type: bidirectional
    alt_funcs:
    - OC1B
    - PCINT4
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
