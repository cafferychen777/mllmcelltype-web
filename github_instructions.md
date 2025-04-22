# GitHub 上传指南

请按照以下步骤将 mLLMCelltype-web 代码上传到 GitHub：

## 1. 创建 GitHub 仓库

1. 登录 GitHub 账户
2. 点击右上角的 "+" 图标，选择 "New repository"
3. 仓库名称填写 "mllmcelltype-web"
4. 描述填写 "Web interface for mLLMCelltype package"
5. 选择 "Public" 可见性
6. 不要初始化仓库（不要添加 README, .gitignore 或 License）
7. 点击 "Create repository"

## 2. 推送代码到 GitHub

在终端中执行以下命令：

```bash
# 进入项目目录
cd /Users/apple/Research/mLLMCelltype/mllmcelltype-web

# 添加远程仓库
git remote add origin https://github.com/cafferychen777/mllmcelltype-web.git

# 推送代码到 GitHub
git push -u origin main
```

## 3. 验证上传

1. 刷新 GitHub 仓库页面
2. 确认所有文件都已上传
3. 检查 README.md 是否正确显示

## 4. 设置 GitHub Pages（可选）

如果您想为项目创建一个简单的网站：

1. 在仓库页面，点击 "Settings"
2. 在左侧菜单中，点击 "Pages"
3. 在 "Source" 部分，选择 "main" 分支和 "/(root)" 文件夹
4. 点击 "Save"
5. 等待几分钟，您的网站将在 https://cafferychen777.github.io/mllmcelltype-web 上可用
