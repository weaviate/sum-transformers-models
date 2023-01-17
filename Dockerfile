FROM python:3.9-slim-buster

WORKDIR /app

COPY requirements.txt .
RUN pip3 install -r requirements.txt

ARG MODEL_NAME
ARG ONNX_RUNTIME
COPY download.py .
RUN chmod +x ./download.py
RUN ./download.py

COPY . .

ENTRYPOINT ["/bin/sh", "-c"]
CMD ["uvicorn app:app --host 0.0.0.0 --port 8080"]