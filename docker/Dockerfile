FROM python:3.12

WORKDIR /usr/code/unraveled

RUN pip install uv

COPY src/unraveled src/unraveled
COPY pyproject.toml .
COPY README.md .

# TODO: Figure out how ghidra should work..
# COPY ghidra/ghidra_stubs-11.2.1.1.0.4-py2.py3-none-any.whl ghidra/

RUN uv sync

CMD [".venv/bin/python", "src/unraveled/container/service.py"]
