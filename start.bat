@echo off
REM mLLMCelltype Web 启动脚本 (Windows)

REM 创建数据目录
mkdir .\data\uploads 2>nul
mkdir .\data\results 2>nul
mkdir .\data\logs 2>nul

REM 设置 API 密钥
set /p OPENAI_API_KEY=请输入 OpenAI API 密钥 (可选):
set /p ANTHROPIC_API_KEY=请输入 Anthropic API 密钥 (可选):
set /p GEMINI_API_KEY=请输入 Google Gemini API 密钥 (可选):
set /p GROK_API_KEY=请输入 X.AI Grok API 密钥 (可选):

REM 拉取最新镜像
echo 拉取最新的 mLLMCelltype Web 镜像...
docker pull cafferyyang777/mllmcelltype-web:latest

REM 运行容器
echo 启动 mLLMCelltype Web 应用...
docker run -d --name mllmcelltype-web ^
  -p 8080:8080 ^
  -e OPENAI_API_KEY="%OPENAI_API_KEY%" ^
  -e ANTHROPIC_API_KEY="%ANTHROPIC_API_KEY%" ^
  -e GEMINI_API_KEY="%GEMINI_API_KEY%" ^
  -e GROK_API_KEY="%GROK_API_KEY%" ^
  -v "%cd%\data\uploads:/app/uploads" ^
  -v "%cd%\data\results:/app/results" ^
  -v "%cd%\data\logs:/app/logs" ^
  cafferyyang777/mllmcelltype-web:latest

REM 检查容器是否成功启动
if %ERRORLEVEL% == 0 (
  echo mLLMCelltype Web 应用已成功启动！
  echo 请在浏览器中访问: http://localhost:8080
  echo 按 Ctrl+C 停止应用

  REM 显示日志
  docker logs -f mllmcelltype-web
) else (
  echo 启动失败，请检查错误信息。
  pause
)
