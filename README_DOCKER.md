# mLLMCelltype Web 本地部署指南

本指南将帮助您在本地计算机上部署和运行 mLLMCelltype Web 应用，使用 Docker 容器技术。

## 前提条件

在开始之前，请确保您的计算机上已安装以下软件：

1. **Docker**：
   - Windows/Mac: [Docker Desktop](https://www.docker.com/products/docker-desktop)
   - Linux: [Docker Engine](https://docs.docker.com/engine/install/)

2. **API 密钥**（至少需要一个）：
   - [OpenAI API 密钥](https://platform.openai.com/account/api-keys)
   - [Anthropic API 密钥](https://console.anthropic.com/account/keys)
   - [Google Gemini API 密钥](https://ai.google.dev/)
   - [X.AI Grok API 密钥](https://x.ai/)
   - 其他支持的 API 密钥（可选）

## 快速开始

我们提供了简单的启动脚本，让您可以轻松运行应用：

### Windows 用户

1. 下载并解压 mLLMCelltype Web 应用包
2. 双击 `start.bat` 文件
3. 根据提示输入您的 API 密钥
4. 等待应用启动完成
5. 在浏览器中访问：http://localhost:8080

### macOS/Linux 用户

1. 下载并解压 mLLMCelltype Web 应用包
2. 打开终端，进入应用目录
3. 执行以下命令：
   ```bash
   chmod +x start.sh
   ./start.sh
   ```
4. 根据提示输入您的 API 密钥
5. 等待应用启动完成
6. 在浏览器中访问：http://localhost:8080

## 手动启动（高级用户）

如果您希望自定义启动参数，可以手动运行 Docker 命令：

```bash
# 创建数据目录
mkdir -p ./data/uploads
mkdir -p ./data/results
mkdir -p ./data/logs

# 运行容器
docker run -d --name mllmcelltype-web \
  -p 8080:8080 \
  -e OPENAI_API_KEY="your_openai_api_key" \
  -e ANTHROPIC_API_KEY="your_anthropic_api_key" \
  -e GEMINI_API_KEY="your_gemini_api_key" \
  -e GROK_API_KEY="your_grok_api_key" \
  -v "$(pwd)/data/uploads:/app/uploads" \
  -v "$(pwd)/data/results:/app/results" \
  -v "$(pwd)/data/logs:/app/logs" \
  cafferyyang777/mllmcelltype-web:latest
```

## 停止应用

### Windows 用户

双击 `stop.bat` 文件

### macOS/Linux 用户

```bash
chmod +x stop.sh
./stop.sh
```

## 配置选项

### 端口设置

默认情况下，应用在端口 8080 上运行。如果需要更改端口，请修改启动命令中的端口映射：

```bash
# 将应用映射到端口 3000
docker run -p 3000:8080 ...
```

然后在浏览器中访问：http://localhost:3000

### 环境变量

应用支持以下环境变量：

| 环境变量 | 描述 | 是否必需 |
|---------|------|---------|
| OPENAI_API_KEY | OpenAI API 密钥 | 至少需要一个 API 密钥 |
| ANTHROPIC_API_KEY | Anthropic API 密钥 | 至少需要一个 API 密钥 |
| GEMINI_API_KEY | Google Gemini API 密钥 | 至少需要一个 API 密钥 |
| QWEN_API_KEY | 通义千问 API 密钥 | 可选 |
| ZHIPU_API_KEY | 智谱 API 密钥 | 可选 |
| STEPFUN_API_KEY | StepFun API 密钥 | 可选 |
| MINIMAX_API_KEY | MiniMax API 密钥 | 可选 |
| MINIMAX_GROUP_ID | MiniMax 组 ID | 与 MINIMAX_API_KEY 一起使用 |
| GROK_API_KEY | X.AI Grok API 密钥 | 可选 |
| OPENROUTER_API_KEY | OpenRouter API 密钥 | 可选 |

### 数据卷

应用使用以下数据卷：

| 容器路径 | 描述 |
|---------|------|
| /app/uploads | 存储上传的文件 |
| /app/results | 存储处理结果 |
| /app/logs | 存储应用日志 |

## 使用指南

1. **上传文件**：
   - 支持 CSV、TSV 和 Excel 格式
   - 文件应包含集群 ID 和标记基因

2. **选择模型**：
   - 选择一个或多个 LLM 模型进行注释
   - 对于多模型共识，建议选择 2-4 个不同的模型

3. **设置参数**：
   - 物种：选择相关的物种（如人类、小鼠等）
   - 组织：选择相关的组织类型
   - 共识阈值：设置多模型共识的阈值（默认 0.7）
   - 最大讨论轮数：设置模型讨论的最大轮数（默认 3）

4. **开始注释**：
   - 点击"开始注释"按钮
   - 等待处理完成（可能需要几分钟到几十分钟，取决于数据大小和选择的模型）

5. **查看结果**：
   - 查看注释结果
   - 下载结果（CSV、Excel 或 TSV 格式）

## 故障排除

### 常见问题

1. **Docker 未安装或未运行**
   - 确保 Docker 已正确安装并运行
   - Windows/Mac: 检查 Docker Desktop 是否正在运行
   - Linux: 运行 `systemctl status docker` 检查 Docker 状态

2. **端口冲突**
   - 如果端口 8080 已被占用，请更改端口映射
   - 例如：`docker run -p 3000:8080 ...`

3. **API 密钥错误**
   - 确保至少提供了一个有效的 API 密钥
   - 检查 API 密钥是否正确，没有多余的空格或引号

4. **内存不足**
   - 如果 Docker 报告内存不足，请增加 Docker 的内存限制
   - Docker Desktop: 设置 > 资源 > 内存

5. **文件上传问题**
   - 确保上传的文件格式正确（CSV、TSV 或 Excel）
   - 检查文件大小是否超过限制（默认最大 20MB）

### 查看日志

如果遇到问题，查看应用日志可能会有所帮助：

```bash
# 查看容器日志
docker logs mllmcelltype-web

# 查看本地日志文件
cat ./data/logs/app.log  # Linux/macOS
type .\data\logs\app.log  # Windows
```

## 更新应用

要更新到最新版本：

1. 停止并删除现有容器：
   ```bash
   docker stop mllmcelltype-web
   docker rm mllmcelltype-web
   ```

2. 拉取最新镜像：
   ```bash
   docker pull cafferyyang777/mllmcelltype-web:latest
   ```

3. 重新启动应用（使用上述启动命令）

## 数据安全

- 所有数据都存储在您的本地计算机上
- API 密钥仅用于与 LLM 提供商通信，不会被永久存储
- 上传的文件和结果保存在本地 `./data` 目录中

## 获取帮助

如果您遇到任何问题或需要帮助，请访问我们的 GitHub 仓库提交 issue：
https://github.com/cafferychen777/mLLMCelltype/issues
