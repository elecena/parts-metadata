"""
Extractor of additional data for the Atmel AVR microcontrollers.

Requires the "pdftotext" tool to be installed from the "pdf-poppler" package.

https://poppler.freedesktop.org/
"""
import re
from subprocess import run
from typing import Optional

type pinout = dict[str, list[str]]


def extract_pin_functions(name: str, datasheet: Optional[str]) -> list[str]:
    """
    Returns a list of pin functions for the given microcontroller.
    """

    #


def is_avr_datasheet(datasheet: Optional[str]) -> bool :
    """
    Checks if the given datasheet is from an Atmel AVR microcontroller.
    """
    if not datasheet:
        return False

    if 'microchip.com/' not in datasheet:
        return False

    # datasheet: http://ww1.microchip.com/downloads/en/DeviceDoc/Atmel-8151-8-bit-AVR-ATmega128A_Datasheet.pdf
    # datasheet: http://ww1.microchip.com/downloads/en/DeviceDoc/atmel-8235-8-bit-avr-microcontroller-attiny20_datasheet.pdf
    if 'avr' in datasheet.lower():
        return True

    # datasheet: https://ww1.microchip.com/downloads/en/DeviceDoc/ATtiny1624-26-27-DataSheet-DS40002234A.pdf
    if '/attiny' in datasheet.lower():
        return True

    # datasheet: http://ww1.microchip.com/downloads/en/DeviceDoc/ATmega328_P%20AVR%20MCU%20with%20picoPower%20Technology%20Data%20Sheet%2040001984A.pdf
    if '/atmega' in datasheet.lower():
        return True

    return False


def parse_pdf(file_name: str) -> pinout:
    """
    Parses the provided PDF file and returns a dictionary with the extracted pinout data.

    https://github.com/elecena/parts-metadata/issues/13
    """
    res = run(
        [
            "pdftotext",
            # from page 0 to 30
            "-f",
            "0",
            "-l",
            "30",
            # the file
            file_name,
            # If text-file is ´-', the text is sent to stdout
            '-',
        ], capture_output=True, check=True, encoding='utf-8')

    if res.returncode != 0:
        raise Exception(f"pdftotext failed with return code {res.returncode}")

    if res.stderr != '':
        raise Exception(f"pdftotext failed with stderr output: {res.stderr}")

    pins: pinout = dict()

    for line in res.stdout.splitlines():
        # PB7 (UCSK/SCL/PCINT7)
        # PD0 (RXD)
        # PB7 (UCSK/SCK/PCINT7)
        # (CKOUT/XCK/INT0) PD2
        # (XTAL1) PA0
        if re.search(r'^P[A-D]\d\s\(', line) or re.search(r'\)\sP[A-D]\d$', line):
            pin_match = re.search(r'P[A-D]\d', line)
            functions_match = re.search(r'\(([^)]+)\)', line)

            if pin_match and functions_match:
                # print(line, pin_match, functions_match)

                # PB7 (UCSK/SCL/PCINT7) -> PB7: 'UCSK','SCL','PCINT7'
                # (XTAL1) PA0 -> PA0: 'XTAL1'
                pins[pin_match.group(0)] = functions_match.group(1).split('/')

    # sort by pins
    return dict(sorted(pins.items()))
