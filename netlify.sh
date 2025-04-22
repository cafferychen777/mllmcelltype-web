#!/bin/bash

# 安装依赖
pip install -r requirements.txt

# 如果需要，安装 mLLMCelltype 包
# pip install git+https://github.com/cafferychen777/mLLMCelltype.git

# 创建必要的目录
mkdir -p uploads results logs
chmod -R 777 uploads results logs

# 打印完成信息
echo "Netlify build completed successfully"
