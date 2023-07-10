FROM python:3.10-slim as builder

RUN pip install setuptools setuptools build
ADD derevo /derevo/derevo/

COPY pyproject.toml README.md /derevo/

RUN cd /derevo && python -m build . --no-isolation

FROM scratch

COPY --from=builder /derevo/dist/*.whl /
