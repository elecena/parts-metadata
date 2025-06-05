import pathlib

from kicad_sym import KicadLibrary

# https://gitlab.com/kicad/libraries/kicad-symbols/-/raw/master/74xx.kicad_sym?ref_type=heads
def test_74xx():
    fixture: str = pathlib.Path(__file__).parent.resolve().__str__() + '/fixtures/74xx.sym'
    library = KicadLibrary.from_file(fixture)
    # print(library)

    assert library.generator == 'kicad_symbol_editor'
    assert library.version == '20241209'

    assert len(library.symbols) == 2
    assert [symbol.name for symbol in library.symbols] == ['74469', '7454']

    # symbol = library.symbols[0]
    # print(symbol.pins)
