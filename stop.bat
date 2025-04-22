@echo off
REM mLLMCelltype Web 停止脚本 (Windows)

echo 停止 mLLMCelltype Web 应用...
docker stop mllmcelltype-web
docker rm mllmcelltype-web

echo 应用已停止。
pause
