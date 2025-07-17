FROM python:3.12

ENV PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  # Poetry's configuration:
  POETRY_NO_INTERACTION=1 \
  POETRY_VIRTUALENVS_CREATE=false \
  POETRY_CACHE_DIR='/var/cache/pypoetry' \
  POETRY_HOME='/usr/local'

# For special needs (COMMENT 'RUN curl')
# ENV PATH="${PATH}:/root/.local/bin"
# RUN pip --trusted-host pypi.org install poetry
# RUN poetry config certificates.PyPI.cert false

RUN curl -sSL https://install.python-poetry.org | python3 -

WORKDIR /usr/local/app

COPY poetry.lock pyproject.toml /usr/local/app/

RUN poetry install --no-root --no-interaction --no-ansi

COPY ./src /usr/local/app/src

RUN python /usr/local/app/src/llm/loadLLM.py

EXPOSE 8000

CMD ["fastapi", "run", "src/main.py", "--reload", "--port", "8000"]
