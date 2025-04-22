// 使用 serverless-http 包装 Flask 应用
const serverless = require('serverless-http');
const express = require('express');
const app = express();
const { exec } = require('child_process');
const path = require('path');

// 设置静态文件目录
app.use(express.static(path.join(__dirname, '..', '..', 'static')));

// 处理所有请求
app.all('*', (req, res) => {
  // 记录请求信息
  console.log(`Received request: ${req.method} ${req.path}`);
  console.log(`Headers: ${JSON.stringify(req.headers)}`);
  
  // 执行 Python 脚本处理请求
  const pythonScript = path.join(__dirname, 'flask_handler.py');
  
  // 构建命令行参数
  const args = [
    `--method=${req.method}`,
    `--path=${req.path}`,
    `--headers=${JSON.stringify(req.headers)}`,
    `--query=${JSON.stringify(req.query)}`,
    `--body=${JSON.stringify(req.body || {})}`
  ];
  
  // 执行 Python 脚本
  exec(`python ${pythonScript} ${args.join(' ')}`, (error, stdout, stderr) => {
    if (error) {
      console.error(`Error executing Python script: ${error}`);
      console.error(`stderr: ${stderr}`);
      return res.status(500).send('Internal Server Error');
    }
    
    try {
      // 解析 Python 脚本的输出
      const response = JSON.parse(stdout);
      
      // 设置响应头
      if (response.headers) {
        Object.entries(response.headers).forEach(([key, value]) => {
          res.set(key, value);
        });
      }
      
      // 设置状态码并发送响应
      res.status(response.status || 200).send(response.body || '');
    } catch (e) {
      console.error(`Error parsing Python response: ${e}`);
      console.error(`Python output: ${stdout}`);
      res.status(500).send('Error processing response');
    }
  });
});

// 导出处理函数
exports.handler = serverless(app);
