# AI Court Debate Agent - Docker 构建文件
FROM golang:1.22-alpine AS builder

# 安装依赖
RUN apk add --no-cache git build-base python3 py3-pip

WORKDIR /app

# 复制项目文件
COPY . .

# 构建 Go 应用
WORKDIR /app/tenapp
RUN go build -o bin/app main.go

# 运行时镜像
FROM python:3.11-slim

# 安装运行时依赖
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    ca-certificates && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# 从构建阶段复制应用
COPY --from=builder /app/tenapp /app

# 安装 Python 依赖
RUN pip install --no-cache-dir \
    ten_runtime_python \
    pydantic

# 暴露端口（如果需要）
EXPOSE 8080

# 启动命令
CMD ["./bin/app"]
