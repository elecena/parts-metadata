import pathlib


def get_fixture_file(file: str) -> str:
    return str(pathlib.Path(__file__).parent.resolve()) + f"/fixtures/{file}"
