#!/bin/bash
# 使用 Docker Compose 启动 mLLMCelltype Web 应用 (macOS/Linux)

# 创建数据目录
mkdir -p ./data/uploads
mkdir -p ./data/results
mkdir -p ./data/logs

# 设置 API 密钥
# 如果环境变量未设置，则提示用户输入
if [ -z "$OPENAI_API_KEY" ]; then
  echo -n "请输入 OpenAI API 密钥 (可选): "
  read OPENAI_API_KEY
  export OPENAI_API_KEY
fi

if [ -z "$ANTHROPIC_API_KEY" ]; then
  echo -n "请输入 Anthropic API 密钥 (可选): "
  read ANTHROPIC_API_KEY
  export ANTHROPIC_API_KEY
fi

if [ -z "$GEMINI_API_KEY" ]; then
  echo -n "请输入 Google Gemini API 密钥 (可选): "
  read GEMINI_API_KEY
  export GEMINI_API_KEY
fi

if [ -z "$GROK_API_KEY" ]; then
  echo -n "请输入 X.AI Grok API 密钥 (可选): "
  read GROK_API_KEY
  export GROK_API_KEY
fi

# 拉取最新镜像
echo "拉取最新的 mLLMCelltype Web 镜像..."
docker-compose pull

# 启动应用
echo "启动 mLLMCelltype Web 应用..."
docker-compose up -d

# 检查容器是否成功启动
if [ $? -eq 0 ]; then
  echo "mLLMCelltype Web 应用已成功启动！"
  echo "请在浏览器中访问: http://localhost:8080"
  echo "按 Ctrl+C 停止查看日志（应用将继续在后台运行）"
  
  # 显示日志
  docker-compose logs -f
else
  echo "启动失败，请检查错误信息。"
fi
