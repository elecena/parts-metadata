"""
Extractor of additional data for the Atmel AVR microcontrollers.

Requires the "pdftotext" tool to be installed from the "pdf-poppler" package.

https://poppler.freedesktop.org/
"""
import functools
import logging
import re
from requests import Session
from subprocess import run
from tempfile import NamedTemporaryFile
from typing import Optional

type pinout = dict[str, list[str]]

# prepare a shared HTTP session for all requests
http_session = Session()
http_session.headers['user-agent'] = 'PartsBot/1.0 (+https://github.com/elecena/parts-metadata/)'


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


@functools.lru_cache(maxsize=2_000)
def parse_pdf_from_url(url: str) -> pinout:
    """
    Fetches the PDF file from the given URL and parses it.
    """
    logger = logging.getLogger(__name__)
    logger.info(f'Fetching PDF from URL: {url}')

    resp = http_session.get(url)
    logger.info(f'Got HTTP {resp.status_code} response with headers: {repr(resp.headers)}')
    resp.raise_for_status()

    with NamedTemporaryFile(prefix='avr-', suffix='.pdf') as pdf_file:
        pdf_file.write(resp.content)

        logger.info(f'Parsing PDF file: {pdf_file.name} ...')
        return parse_pdf(pdf_file.name)


def parse_pdf(file_name: str) -> pinout:
    """
    Parses the provided PDF file and returns a dictionary with the extracted pinout data.

    https://github.com/elecena/parts-metadata/issues/13
    """
    if file_name.startswith('http'):
        raise Exception(f"parse_pdf: URLs are not supported: {file_name}")

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
                pins[pin_match.group(0)] = list(map(lambda item: str(item).strip(), functions_match.group(1).split('/')))

    # sort by pins
    return dict(sorted(pins.items()))
