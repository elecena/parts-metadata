"""
Extractor of additional data for the Atmel AVR microcontrollers.

Requires the "pdftotext" tool to be installed from the "pdf-poppler" package.

https://poppler.freedesktop.org/
"""
from typing import Optional


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
