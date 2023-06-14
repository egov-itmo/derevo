FROM ubuntu:22.04 as builder

RUN apt update && \
    apt install -y wget tar xz-utils git && \
    wget -O flutter.tar.xz https://storage.googleapis.com/flutter_infra_release/releases/stable/linux/flutter_linux_3.10.4-stable.tar.xz && \
    mkdir build && \
    cd build && \
    tar xf /flutter.tar.xz && \
    rm /flutter.tar.xz

RUN git config --global --add safe.directory /build/flutter && \
    PATH="$PATH:/build/flutter/bin" flutter precache

ADD lib /frontend/lib/
ADD web /frontend/web/
COPY .gitignore .metadata analysis_options.yaml pubspec.yaml pubspec.lock /frontend/

RUN cd frontend && \
    PATH="$PATH:/build/flutter/bin" flutter build web


FROM nginx:latest

COPY --from=builder /frontend/build/web /usr/share/nginx/html
