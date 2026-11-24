FROM python:3.12-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY fonts ./fonts
COPY builder ./builder
COPY content ./content
COPY webapp ./webapp

# Build every book (US and UK) now, so the site starts fast and downloads are instant
RUN python -m builder build all --spelling both > /dev/null \
    && useradd --create-home app && chown -R app /app
USER app

ENV HOST=0.0.0.0 PORT=8000
EXPOSE 8000
CMD ["python", "-m", "webapp"]
