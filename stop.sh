#!/bin/bash
# mLLMCelltype Web 停止脚本 (macOS/Linux)

echo "停止 mLLMCelltype Web 应用..."
docker stop mllmcelltype-web
docker rm mllmcelltype-web

echo "应用已停止。"
