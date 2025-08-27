FROM debian:bullseye

LABEL org.opencontainers.image.source="https://github.com/cyanjnpr/karMtka"

WORKDIR /build

RUN apt-get update && \
    apt-get install -y \
        python3 \
        python3-pip \
        python3-venv \
        gcc \
        patchelf \
        libffi-dev \
        libjpeg-dev \ 
        zlib1g-dev \
        libtiff-dev \
        liblcms2-dev \
        libwebp-dev \
        libstb-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    python3 -m pip install poetry

ENTRYPOINT [ "/bin/bash", "docker_build.sh" ]
