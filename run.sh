#!/bin/bash

# 创建必要的目录
mkdir -p uploads results logs

# 安装依赖
pip install -r requirements.txt

# 运行应用
python app.py
