#!/bin/bash

set -e

echo "======================================"
echo "AI Court Debate Agent - Starting"
echo "线上法庭智能答辩 AI Agent - 启动中"
echo "======================================"

# Get the directory of this script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
APP_DIR="$(dirname "$SCRIPT_DIR")"

cd "$APP_DIR"

# Check if the app binary exists
if [ ! -f "./bin/app" ]; then
    echo "Error: App binary not found. Please build the app first."
    echo "错误：应用程序二进制文件未找到。请先构建应用程序。"
    exit 1
fi

# Run the app
echo "Starting AI Court Debate Agent..."
echo "启动 AI 法庭辩论代理..."

./bin/app "$@"
