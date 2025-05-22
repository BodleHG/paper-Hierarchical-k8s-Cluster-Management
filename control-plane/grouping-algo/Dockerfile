# ---------- Build Stage ----------
FROM python:3.11-slim as builder
WORKDIR /app
COPY main.py ./
COPY requirements.txt ./
RUN pip install --upgrade pip && \
    pip install --no-cache-dir --target=/install -r requirements.txt

# ---------- Runtime Stage ----------
FROM python:3.11-slim
WORKDIR /app
COPY --from=builder /app/main.py ./
COPY --from=builder /install /usr/local/lib/python3.11/site-packages

# 필요한 CLI 도구 설치 (kubectl)
ENV KUBECTL_VERSION=v1.29.5

RUN apt-get update && \
    apt-get install -y curl && \
    curl -sSL -o /usr/local/bin/kubectl https://dl.k8s.io/release/${KUBECTL_VERSION}/bin/linux/amd64/kubectl && \
    chmod +x /usr/local/bin/kubectl && \
    apt-get clean && rm -rf /var/lib/apt/lists/*


ENTRYPOINT ["python", "-u", "main.py"]
    