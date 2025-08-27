#!/bin/bash
# this is a container entrypoint

(cd src/sketch/libsketch && make)

python3 -m poetry env use python3
eval $(python3 -m poetry env activate)

poetry install
python3 -m pip install nuitka

python3 -m nuitka --user-package-configuration-file=karmtka.nuitka-package.config.yml --remove-output \
    --deployment --mode=onefile --output-filename=karmtka_$(uname -m) src/main.py
