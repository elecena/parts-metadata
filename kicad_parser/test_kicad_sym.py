import pathlib
from json import dumps

from kicad_sym import KicadLibrary
from part import Part


def get_fixture_file(file: str) -> str:
    return pathlib.Path(__file__).parent.resolve().__str__() + f'/fixtures/{file}'


# https://gitlab.com/kicad/libraries/kicad-symbols/-/raw/master/74xx.kicad_sym?ref_type=heads
def test_74xx():
    library = KicadLibrary.from_file(get_fixture_file('74xx.sym'))
    # print(library)

    assert library.generator == 'kicad_symbol_editor'
    assert library.version == '20241209'

    assert len(library.symbols) == 2
    assert [symbol.name for symbol in library.symbols] == ['74469', '7454']

    # symbol = library.symbols[0]

    # etype: tri_state, input, power_in, output
    # print('Pins', {pin.number:[pin.name, pin.etype] for pin in symbol.pins})
    # print('Properties', {prop.name.lower(): prop.value for prop in symbol.properties})


def test_parse_symbol():
    library = KicadLibrary.from_file(get_fixture_file('74xx.sym'))
    symbol = library.symbols[0]

    part = Part.from_kicad_symbol(symbol)
    # print(part, dumps(part.as_dict(), indent=True))

    assert part.name == '74469'
    assert part.footprint == ''
    assert part.description == '8-bit synchronous up/down counter, parallel load and hold capability (obsolete)'
    assert part.datasheet == 'http://www.ti.com/lit/gpn/sn74469'
    assert len(part.pinout) == 24

    assert part.pinout['1'].name == 'CLK'
    assert part.pinout['1'].type == 'input'

    assert part.pinout['12'].name == 'GND'
    assert part.pinout['12'].type == 'power_in'

    assert part.pinout['24'].name == 'VCC'
    assert part.pinout['24'].type == 'power_in'


def test_parse_symbol_with_inheritance():
    library = KicadLibrary.from_file(get_fixture_file('attiny.sym'))

    assert len(library.symbols) == 2
    assert [symbol.name for symbol in library.symbols] == ['ATtiny48-P', 'ATtiny88-P']

    attiny48 = Part.from_kicad_symbol(library.symbols[0])
    attiny88 = Part.from_kicad_symbol(library.symbols[1])

    # print(str(attiny48), str(attiny88))

    assert attiny48.name == 'ATtiny48-P'
    assert attiny48.footprint == 'Package_DIP:DIP-28_W7.62mm'
    assert attiny48.description == '12MHz, 4kB Flash, 256B SRAM, 64B EEPROM, DIP-28'
    assert attiny88.name == 'ATtiny88-P'
    assert attiny88.footprint == 'Package_DIP:DIP-28_W7.62mm'
    assert attiny88.description == '12MHz, 8kB Flash, 512B SRAM, 64B EEPROM, DIP-28'

    # these devices share the same pinout
    assert attiny48.pinout['1'].name == '~{RESET}/PC6'
    assert attiny88.pinout['1'].name == '~{RESET}/PC6'
    assert attiny48.pinout['28'].name == 'PC5'
    assert attiny88.pinout['28'].name == 'PC5'
