from extractors.avr import is_avr_datasheet


def test_is_avr_datasheet():
    pdfs = [
        "http://ww1.microchip.com/downloads/en/DeviceDoc/ATmega328_P%20AVR%20MCU%20with%20picoPower%20Technology%20Data%20Sheet%2040001984A.pdf",
        "http://ww1.microchip.com/downloads/en/DeviceDoc/Atmel-2543-AVR-ATtiny2313_Datasheet.pdf",
        "http://ww1.microchip.com/downloads/en/DeviceDoc/atmel-2586-avr-8-bit-microcontroller-attiny25-attiny45-attiny85_datasheet.pdf",
        "http://ww1.microchip.com/downloads/en/DeviceDoc/ATtiny807_1607-Data-Sheet-40002030A.pdf",
    ]

    for pdf in pdfs:
        assert is_avr_datasheet(pdf) == True, pdf


def test_is_not_avr_datasheet():
    pdfs = [
        "http://arduino.cc/ATtiny807_1607-Data-Sheet-40002030A.pdf",
    ]

    for pdf in pdfs:
        assert is_avr_datasheet(pdf) == False, pdf
