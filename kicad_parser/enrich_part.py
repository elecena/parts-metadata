"""
Tries to get additional data for the parts from official datasheets.
"""

from extractors.avr import is_avr_datasheet, parse_pdf_from_url

from part import Part


def enrich_part(part: Part):
    if is_avr_datasheet(part.datasheet):
        # 'PB6': ['MISO', 'DO', 'PCINT6'],
        # 'PD2': ['CKOUT', 'XCK', 'INT0'],
        parsed = parse_pdf_from_url(part.datasheet)
        # print(parsed)

        # "1": {name: "DO": type: "input"}
        for pin_data in part.pinout.values():
            pin_name = pin_data.name.split("/")[0]  # PA2/~{RESET} or PB7
            # remove the extra bits in the pin name
            pin_data.name = pin_name

            # enrich the pinout
            if pin_name in parsed:
                pin_data.alt_funcs = parsed[pin_name]
