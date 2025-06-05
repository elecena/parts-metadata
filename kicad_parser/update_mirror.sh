#!/bin/sh

for FILE in kicad_sym.py boundingbox.py sexpr.py;
do
	wget "https://gitlab.com/kicad/libraries/kicad-library-utils/-/raw/master/common/${FILE}"
done
