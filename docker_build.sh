#!/bin/bash
# this is a container entrypoint

python3 -m poetry env use python3
eval $(python3 -m poetry env activate)

poetry install
python3 -m pip install nuitka

python3 -m nuitka --remove-output --deployment --mode=onefile --output-filename=karmtka_$(uname -m) src/main.py
