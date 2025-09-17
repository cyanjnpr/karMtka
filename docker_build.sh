#!/bin/bash
# container entrypoint

# assume yes by default
if [  -z "$C_SKETCH_IMPLEMENTATION" ] || [ "$C_SKETCH_IMPLEMENTATION" = "1" ]; then
    (cd src/sketch/libsketch && make -B)
    # this is probably not the way to do it, but neither toltec nor entware have libpotrace
    [ "$(uname -m)" = "armv7l" ] && cp -L /usr/lib/arm-linux-gnueabihf/libpotrace.so.0 src/sketch/libsketch/
    [ "$(uname -m)" = "aarch64" ] && cp -L /usr/lib/aarch64-linux-gnu/libpotrace.so.0 src/sketch/libsketch/

    echo "C_SKETCH_IMPLEMENTATION=1" > src/config.py

    python3 -m poetry env use python3
    eval $(python3 -m poetry env activate)

    poetry install
    python3 -m pip install nuitka

    python3 -m nuitka --user-package-configuration-file=karmtka.nuitka-package.config.yml --remove-output \
        --deployment --mode=onefile --output-filename=karmtka_$(uname -m) src/main.py
    rm src/sketch/libsketch/libpotrace.so.0
elif [ "$C_SKETCH_IMPLEMENTATION" = "0" ]; then
    echo "C_SKETCH_IMPLEMENTATION=0" > src/config.py

    python3 -m poetry env use python3
    eval $(python3 -m poetry env activate)

    poetry install -E sketch
    python3 -m pip install nuitka

    python3 -m nuitka --remove-output \
        --deployment --mode=onefile --output-filename=karmtka_$(uname -m) src/main.py
fi
