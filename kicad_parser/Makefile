test:
	pytest . -vv

update:
	sh update_mirror.sh

fetch_kicad_symbols:
	wget --backups=1 https://gitlab.com/kicad/libraries/kicad-symbols/-/archive/master/kicad-symbols-master.zip

lint:
	black *.py
	pylint *.py
