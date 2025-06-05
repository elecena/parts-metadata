from dataclasses import dataclass
from typing import Dict, Optional

from kicad_sym import KicadSymbol


@dataclass
class Pin:
    """
    Keep a single pin definition, a subset of kicad_sym.Pin class
    """
    name: str   # e.g. DO, Q3, GND, CLK, VCC
    type: str  # e.g. tri_state, input, power_in, output
    alt_funcs: Optional[list[str]]  # alternative functions, useful for microprocessors

    def __repr__(self) -> str:
        return f'<Pin {self.name} [{self.type}]>'

    def as_dict(self) -> dict:
        return {
            'name': self.name,
            'type': self.type,
        }


@dataclass
class Part:
    """
    Keeps the device pinout, a subset of kicad_sym.KicadSymbol class
    """
    name: str  # e.g. 74469
    pinout:  Dict[str, Pin]  # "1": {name: "DO": type: "input"}
    datasheet: Optional[str]
    description: Optional[str]

    def __repr__(self) -> str:
        pinout = '\n'.join([
            f'\t{no} {repr(pin)}'
          for no, pin in self.pinout.items()
        ])

        return f'<Part {self.name}\n\tDesc: {self.description}\n\tPDF: {self.datasheet}\n{pinout}\n>'

    def as_dict(self) -> dict:
        return {
            'name': self.name,
            'description': self.description,
            'datasheet': self.datasheet,
            'pinout': {no: pin.as_dict() for no, pin in self.pinout.items()},
        }

    @classmethod
    def from_kicad_symbol(cls, symbol: KicadSymbol):
        pinout = {
            pin.number: Pin(
                name=pin.name,
                type=pin.etype,
                alt_funcs=[],  # TODO
            )
            # pins should be sorted by their numbers
            for pin in sorted(
                symbol.pins,
                key=lambda p: int(p.number) if str(p.number).isnumeric() else p.number
            )
        }
        symbol_properties = {prop.name.lower(): prop.value for prop in symbol.properties}

        return cls(
            name=symbol.name,
            pinout=pinout,
            datasheet=symbol_properties.get('datasheet'),
            description=symbol_properties.get('description'),
        )
