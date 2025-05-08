# -------- Stage 1: Build stage --------
FROM python:3.11-slim AS builder

WORKDIR /app

COPY requirements.txt ./
COPY main.py ./


# install dependencies in isolated directory
RUN pip install --upgrade pip && \
    pip install --no-cache-dir --target=/install -r requirements.txt

# -------- Stage 2: Runtime stage --------
FROM python:3.11-slim

WORKDIR /app

# 복사: main.py와 최소한의 라이브러리만
COPY --from=builder /app/main.py ./
COPY --from=builder /install /usr/local/lib/python3.11/site-packages

CMD ["python", "-u", "main.py"]
    