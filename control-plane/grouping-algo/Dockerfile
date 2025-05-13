# ---------- Build Stage ----------
FROM python:3.11-slim as builder
WORKDIR /app
COPY main.py ./
RUN pip install --upgrade pip

# ---------- Runtime Stage ----------
FROM python:3.11-slim
WORKDIR /app
COPY --from=builder /app/main.py ./

# 필요한 CLI 도구 설치 (kubectl)
ENV KUBECTL_VERSION=v1.29.5

RUN apt-get update && \
    apt-get install -y curl && \
    curl -sSL -o /usr/local/bin/kubectl https://dl.k8s.io/release/${KUBECTL_VERSION}/bin/linux/amd64/kubectl && \
    chmod +x /usr/local/bin/kubectl && \
    apt-get clean && rm -rf /var/lib/apt/lists/*


ENTRYPOINT ["python", "-u", "main.py"]
    