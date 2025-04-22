#!/bin/bash
# 构建并发布 Docker 镜像

# 设置变量
IMAGE_NAME="cafferychen777/mllmcelltype-web"
TAG="latest"

# 构建镜像
echo "构建 Docker 镜像: $IMAGE_NAME:$TAG"
docker build -t $IMAGE_NAME:$TAG .

# 检查构建是否成功
if [ $? -ne 0 ]; then
  echo "构建失败，退出"
  exit 1
fi

# 推送到 Docker Hub
echo "推送镜像到 Docker Hub: $IMAGE_NAME:$TAG"
docker push $IMAGE_NAME:$TAG

# 检查推送是否成功
if [ $? -eq 0 ]; then
  echo "镜像已成功推送到 Docker Hub"
  echo "用户现在可以使用以下命令拉取镜像:"
  echo "docker pull $IMAGE_NAME:$TAG"
else
  echo "推送失败"
fi
