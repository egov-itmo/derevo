FROM python:3.10-slim as builder

RUN pip install setuptools setuptools build
ADD compositioner /compositioner/compositioner/

COPY pyproject.toml README.md /compositioner/

RUN cd /compositioner && python -m build . --no-isolation

FROM scratch

COPY --from=builder /compositioner/dist/*.whl /
