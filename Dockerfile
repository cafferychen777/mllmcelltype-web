FROM python:3.9-slim

WORKDIR /app

# 安装依赖
RUN apt-get update && apt-get install -y git && apt-get clean && rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制 mLLMCelltype 代码
COPY mLLMCelltype /app/mLLMCelltype

# 添加 mLLMCelltype 到 Python 路径
ENV PYTHONPATH="/app"

# 复制应用文件
COPY . .

# 创建必要的目录并设置权限
RUN mkdir -p uploads results logs && \
    chmod -R 777 uploads results logs

# 暴露端口
EXPOSE 8080

# 设置环境变量
ENV FLASK_APP=app.py
ENV FLASK_ENV=production
ENV PYTHONUNBUFFERED=1

# 运行应用
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "app:app", "--workers", "2", "--timeout", "120"]
