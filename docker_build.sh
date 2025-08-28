#!/bin/bash
# this is a container entrypoint

if [  -z "$C_SKETCH_IMPLEMENTATION" ] || [ "$C_SKETCH_IMPLEMENTATION" = "1" ]; then
    (cd src/sketch/libsketch && make -B)
    echo "C_SKETCH_IMPLEMENTATION=1" > src/config.py

    python3 -m poetry env use python3
    eval $(python3 -m poetry env activate)

    poetry install
    python3 -m pip install nuitka

    python3 -m nuitka --user-package-configuration-file=karmtka.nuitka-package.config.yml --remove-output \
        --deployment --mode=onefile --output-filename=karmtka_$(uname -m) src/main.py
else
    echo "C_SKETCH_IMPLEMENTATION=0" > src/config.py

    python3 -m poetry env use python3
    eval $(python3 -m poetry env activate)

    poetry install -E sketch
    python3 -m pip install nuitka

    python3 -m nuitka --remove-output \
        --deployment --mode=onefile --output-filename=karmtka_$(uname -m) src/main.py
fi
