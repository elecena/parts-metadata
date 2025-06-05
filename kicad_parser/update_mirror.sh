#!/bin/sh

for FILE in kicad_sym.py boundingbox.py sexpr.py geometry.py;
do
	echo "Syncing ${FILE} ..."
	curl -s "https://gitlab.com/kicad/libraries/kicad-library-utils/-/raw/master/common/${FILE}" > $FILE
done

echo "Done."
