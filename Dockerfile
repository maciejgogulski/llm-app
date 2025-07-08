FROM python:3.10


WORKDIR /app


COPY requirements.txt .
RUN pip install -r requirements.txt

COPY main.py .
COPY llm/ llm/
COPY config/ config/
COPY routes/ routes/
COPY db/ db/

RUN pip install --no-cache-dir -r requirements.txt

COPY main.py .

EXPOSE 5000

CMD ["python", "main.py"]
