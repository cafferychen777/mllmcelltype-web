#!/bin/bash
# mLLMCelltype Web 启动脚本 (macOS/Linux)

# 创建数据目录
mkdir -p ./data/uploads
mkdir -p ./data/results
mkdir -p ./data/logs

# 设置 API 密钥
# 如果环境变量未设置，则使用默认值或提示用户输入
OPENAI_API_KEY=${OPENAI_API_KEY:-""}
ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY:-""}
GEMINI_API_KEY=${GEMINI_API_KEY:-""}
QWEN_API_KEY=${QWEN_API_KEY:-""}
ZHIPU_API_KEY=${ZHIPU_API_KEY:-""}
STEPFUN_API_KEY=${STEPFUN_API_KEY:-""}
MINIMAX_API_KEY=${MINIMAX_API_KEY:-""}
MINIMAX_GROUP_ID=${MINIMAX_GROUP_ID:-""}
GROK_API_KEY=${GROK_API_KEY:-""}
OPENROUTER_API_KEY=${OPENROUTER_API_KEY:-""}

# 如果 API 密钥未设置，提示用户输入
if [ -z "$OPENAI_API_KEY" ]; then
  echo -n "请输入 OpenAI API 密钥 (可选): "
  read OPENAI_API_KEY
fi

if [ -z "$ANTHROPIC_API_KEY" ]; then
  echo -n "请输入 Anthropic API 密钥 (可选): "
  read ANTHROPIC_API_KEY
fi

if [ -z "$GEMINI_API_KEY" ]; then
  echo -n "请输入 Google Gemini API 密钥 (可选): "
  read GEMINI_API_KEY
fi

if [ -z "$GROK_API_KEY" ]; then
  echo -n "请输入 X.AI Grok API 密钥 (可选): "
  read GROK_API_KEY
fi

# 拉取最新镜像
echo "拉取最新的 mLLMCelltype Web 镜像..."
docker pull cafferyyang777/mllmcelltype-web:latest

# 运行容器
echo "启动 mLLMCelltype Web 应用..."
docker run -d --name mllmcelltype-web \
  -p 8080:8080 \
  -e OPENAI_API_KEY="$OPENAI_API_KEY" \
  -e ANTHROPIC_API_KEY="$ANTHROPIC_API_KEY" \
  -e GEMINI_API_KEY="$GEMINI_API_KEY" \
  -e QWEN_API_KEY="$QWEN_API_KEY" \
  -e ZHIPU_API_KEY="$ZHIPU_API_KEY" \
  -e STEPFUN_API_KEY="$STEPFUN_API_KEY" \
  -e MINIMAX_API_KEY="$MINIMAX_API_KEY" \
  -e MINIMAX_GROUP_ID="$MINIMAX_GROUP_ID" \
  -e GROK_API_KEY="$GROK_API_KEY" \
  -e OPENROUTER_API_KEY="$OPENROUTER_API_KEY" \
  -v "$(pwd)/data/uploads:/app/uploads" \
  -v "$(pwd)/data/results:/app/results" \
  -v "$(pwd)/data/logs:/app/logs" \
  cafferyyang777/mllmcelltype-web:latest

# 检查容器是否成功启动
if [ $? -eq 0 ]; then
  echo "mLLMCelltype Web 应用已成功启动！"
  echo "请在浏览器中访问: http://localhost:8080"
  echo "按 Ctrl+C 停止应用"

  # 显示日志
  docker logs -f mllmcelltype-web
else
  echo "启动失败，请检查错误信息。"
fi
