import pathlib
from json import dumps

from kicad_sym import KicadLibrary
from part import Part


def get_fixture_file() -> str:
    return pathlib.Path(__file__).parent.resolve().__str__() + '/fixtures/74xx.sym'


# https://gitlab.com/kicad/libraries/kicad-symbols/-/raw/master/74xx.kicad_sym?ref_type=heads
def test_74xx():
    library = KicadLibrary.from_file(get_fixture_file())
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
    library = KicadLibrary.from_file(get_fixture_file())
    symbol = library.symbols[0]

    part = Part.from_kicad_symbol(symbol)
    # print(part, dumps(part.as_dict(), indent=True))

    assert part.name == '74469'
    assert part.description == '8-bit synchronous up/down counter, parallel load and hold capability (obsolete)'
    assert part.datasheet == 'http://www.ti.com/lit/gpn/sn74469'
    assert len(part.pinout) == 24

    assert part.pinout['1'].name == 'CLK'
    assert part.pinout['1'].type == 'input'

    assert part.pinout['12'].name == 'GND'
    assert part.pinout['12'].type == 'power_in'

    assert part.pinout['24'].name == 'VCC'
    assert part.pinout['24'].type == 'power_in'
