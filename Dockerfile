FROM python:3.10-slim-bullseye

RUN pip install poetry

WORKDIR /app
COPY . .

RUN touch std.log
RUN poetry config virtualenvs.create false
RUN poetry install --no-interaction --no-ansi

CMD ["poetry", "run", "bot"]
