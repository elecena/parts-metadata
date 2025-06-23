"""
This directory contains the Kicad Python code mirrored from the official Kicad repo.

Use "make update" to keep these files up to date.
"""

import os
import sys

# hacky: add the current directory so that kicad repo mirrored file do not need to have the imports changed
this_dir = os.path.dirname(__file__)
sys.path.append(this_dir)

# print('kicad paths', sys.path)\
