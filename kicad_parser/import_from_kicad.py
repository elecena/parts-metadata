#!/usr/bin/env python3
import logging

from typing import Iterable

from zipfile import ZipFile
from tempfile import NamedTemporaryFile

from kicad_sym import KicadLibrary
from part import Part

"""
Reads the provided ZipFile and extract "_sym" files.
Yields temporary file names with the extracted content, file by file.
"""
def iterate_archive(zip_file: ZipFile) -> Iterable[str]:
    logger = logging.getLogger('iterate_archive')

    # https://docs.python.org/3/library/zipfile.html
    for item in zip_file.namelist():
        # kicad-symbols-master/74xx.kicad_sym
        if not item.endswith('_sym'):
            continue

        # INFO:iterate_archive: > Found archive item: "kicad-symbols-master/power.kicad_sym"
        # Connector_Generic.kicad_sym
        # Mechanical.kicad_sym
        if 'power.kicad' in item or '/Connector' in item or 'Mechanical' in item:
            continue

        logger.info(f' > Found archive item: "{item}"')

        with zip_file.open(item, mode='r') as my_file:
            # e.g. /tmp/kicad_4ykd6li7_sym
            with NamedTemporaryFile(mode='wt', prefix='kicad_', suffix='_sym') as temp_file:
                with open(temp_file.name, 'wt') as temp_io:
                    for line in my_file:
                        temp_io.write(line.decode('utf-8'))

                logger.info(f' < Saved in "{temp_file.name}"')
                yield temp_file.name


"""
Takes the KiCad repo zip file and yields parsed parts
"""
def iterate_parts(zip_file: ZipFile) -> Iterable[Part]:
    for sym_file in iterate_archive(zip_file):
        library = KicadLibrary.from_file(sym_file)

        logging.info(f'Symbols found: {len(library.symbols)}')

        for symbol in library.symbols:
            try:
                part = Part.from_kicad_symbol(symbol)
                logging.info(f'* {part.name} ({part.description})')

                yield part
            except (AssertionError, TypeError) as ex:
                # WARNING:root:Part 1N4934 not parsed: Pinout of 1N4934 is empty
                # WARNING:root:Part ADAU1761 not parsed: '<' not supported between instances of 'str' and 'int'
                logging.warn(f'Part {symbol.name} not parsed: {str(ex)}')
                # raise ex


def main(archive_file: str):
    logging.info(f'Importing symbols from {archive_file} file ...')
    parts_count = 0

    with ZipFile(archive_file, 'r') as zip_file:
        for part in iterate_parts(zip_file):
            parts_count += 1

    # INFO:root:Found 20253 parts
    logging.info(f'Found {parts_count} parts')


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s %(levelname)-8s %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    # logging.basicConfig(level=logging.WARN)

    # fetch by
    # wget https://gitlab.com/kicad/libraries/kicad-symbols/-/archive/master/kicad-symbols-master.zip
    main(archive_file='kicad-symbols-master.zip')
