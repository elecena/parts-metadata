"""
Test suites for AVR metadata extractors.
"""

# pylint: disable=line-too-long

import pathlib
from extractors.avr import is_avr_datasheet, parse_pdf


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
