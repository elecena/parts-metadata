from dataclasses import dataclass
from typing import Dict, Optional

from kicad_sym import KicadSymbol


@dataclass
class Pin:
    """
    Keep a single pin definition, a subset of kicad_sym.Pin class
    """
    name: str   # e.g. DO, Q3, GND, CLK, VCC
    type: str  # e.g. tri_state, input, power_in, output, no_connect
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
    footprint: Optional[str]
    datasheet: Optional[str]
    description: Optional[str]

    def __str__(self) -> str:
        return f'<Part {self.name} ({self.description})>'

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
            'footprint': self.footprint,
            'pinout': {no: pin.as_dict() for no, pin in self.pinout.items()},
        }

    @classmethod
    def from_kicad_symbol(cls, symbol: KicadSymbol):
        # Some devices extend other symbols
        # get_parent_symbol
        # 	(symbol "7400"
        # 		(extends "74LS00")
        parent = symbol.get_parent_symbol()

        # follow further parent symbols
        # (symbol "INA281A2"
        #   (extends "INA281A1")
        # (symbol "INA281A1"
		#   (extends "AD8211")
        if parent:
            grandparent = parent.get_parent_symbol()
            if grandparent:
                parent = grandparent

        pinout = {
            pin.number: Pin(
                name=pin.name,
                type=pin.etype,
                alt_funcs=[],  # TODO
            )
            # pins should be sorted by their numbers
            for pin in sorted(
                symbol.pins if not parent else parent.pins,
                key=lambda p: int(p.number) if str(p.number).isnumeric() else p.number
            )
        }

        assert len(pinout.keys()) > 0, f'Pinout of {symbol.name} is empty'

        datasheet = symbol.get_property('Datasheet')
        description = symbol.get_property('Description')
        footprint = symbol.get_property('Footprint')  # e.g. Package_DIP:DIP-28_W7.62mm

        return cls(
            name=symbol.name,
            pinout=pinout,
            datasheet=datasheet.value if datasheet else None,
            description=description.value if description else None,
            footprint=footprint.value if footprint else None,
        )
