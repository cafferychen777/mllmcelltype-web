import os
import requests
import json
from pprint import pprint

# 设置 API 密钥 - 请替换为您自己的 API 密钥
# 您可以通过环境变量设置 API 密钥，或者在此处直接设置
# 示例：
# os.environ["OPENAI_API_KEY"] = "your_openai_api_key_here"
# os.environ["ANTHROPIC_API_KEY"] = "your_anthropic_api_key_here"

# 为了测试，您需要设置至少一个 API 密钥
# 如果您没有设置 API 密钥，测试将失败

# 首先上传文件
def upload_file():
    print("Uploading file...")

    # 准备文件上传
    files = {'file': open('uploads/sample_data.csv', 'rb')}

    # 发送请求
    response = requests.post('http://127.0.0.1:8080/api/upload', files=files)

    # 检查响应
    if response.status_code == 200:
        print("File uploaded successfully")
        return response.json()
    else:
        print(f"Error uploading file: {response.status_code}")
        print(response.text)
        return None

# 测试 OpenAI 模型
def test_openai(upload_data):
    print("\nTesting OpenAI GPT-4.1 model...")

    # 准备请求数据
    data = {
        "task_id": upload_data["task_id"],
        "file_path": upload_data["file_path"],
        "species": "human",
        "tissue": "blood",
        "models": ["gpt-4.1"],
        "api_keys": {
            "openai": os.environ["OPENAI_API_KEY"]
        },
        "consensus_threshold": 0.7,
        "max_discussion_rounds": 3
    }

    # 发送请求
    headers = {'Content-Type': 'application/json'}
    response = requests.post('http://127.0.0.1:8080/api/annotate', json=data, headers=headers)

    # 打印响应
    print(f"Status code: {response.status_code}")
    try:
        print(json.dumps(response.json(), indent=2))
    except:
        print(response.text)

    return response.json()["task_id"] if response.status_code == 200 else None

# 测试 Anthropic 模型
def test_anthropic(upload_data):
    print("\nTesting Anthropic Claude 3.7 Sonnet model...")

    # 准备请求数据
    data = {
        "task_id": upload_data["task_id"],
        "file_path": upload_data["file_path"],
        "species": "human",
        "tissue": "blood",
        "models": ["claude-3-7-sonnet-20250219"],
        "api_keys": {
            "anthropic": os.environ["ANTHROPIC_API_KEY"]
        },
        "consensus_threshold": 0.7,
        "max_discussion_rounds": 3
    }

    # 发送请求
    headers = {'Content-Type': 'application/json'}
    response = requests.post('http://127.0.0.1:8080/api/annotate', json=data, headers=headers)

    # 打印响应
    print(f"Status code: {response.status_code}")
    try:
        print(json.dumps(response.json(), indent=2))
    except:
        print(response.text)

    return response.json()["task_id"] if response.status_code == 200 else None

# 测试 Gemini 模型
def test_gemini(upload_data):
    print("\nTesting Google Gemini 2.5 Pro model...")

    # 准备请求数据
    data = {
        "task_id": upload_data["task_id"],
        "file_path": upload_data["file_path"],
        "species": "human",
        "tissue": "blood",
        "models": ["gemini-2.5-pro-preview-03-25"],
        "api_keys": {
            "gemini": os.environ["GEMINI_API_KEY"]
        },
        "consensus_threshold": 0.7,
        "max_discussion_rounds": 3
    }

    # 发送请求
    headers = {'Content-Type': 'application/json'}
    response = requests.post('http://127.0.0.1:8080/api/annotate', json=data, headers=headers)

    # 打印响应
    print(f"Status code: {response.status_code}")
    try:
        print(json.dumps(response.json(), indent=2))
    except:
        print(response.text)

    return response.json()["task_id"] if response.status_code == 200 else None

# 测试 Grok 模型
def test_grok(upload_data):
    print("\nTesting X.AI Grok 3 Beta model...")

    # 准备请求数据
    data = {
        "task_id": upload_data["task_id"],
        "file_path": upload_data["file_path"],
        "species": "human",
        "tissue": "blood",
        "models": ["grok-3-beta"],
        "api_keys": {
            "grok": os.environ["GROK_API_KEY"]
        },
        "consensus_threshold": 0.7,
        "max_discussion_rounds": 3
    }

    # 发送请求
    headers = {'Content-Type': 'application/json'}
    response = requests.post('http://127.0.0.1:8080/api/annotate', json=data, headers=headers)

    # 打印响应
    print(f"Status code: {response.status_code}")
    try:
        print(json.dumps(response.json(), indent=2))
    except:
        print(response.text)

    return response.json()["task_id"] if response.status_code == 200 else None

# 测试多模型共识
def test_consensus(upload_data):
    print("\nTesting multi-model consensus annotation...")

    # 准备请求数据
    data = {
        "task_id": upload_data["task_id"],
        "file_path": upload_data["file_path"],
        "species": "human",
        "tissue": "blood",
        "models": ["gpt-4.1", "claude-3-7-sonnet-20250219", "gemini-2.5-pro-preview-03-25", "grok-3-beta"],
        "api_keys": {
            "openai": os.environ["OPENAI_API_KEY"],
            "anthropic": os.environ["ANTHROPIC_API_KEY"],
            "gemini": os.environ["GEMINI_API_KEY"],
            "grok": os.environ["GROK_API_KEY"]
        },
        "consensus_threshold": 0.7,
        "max_discussion_rounds": 3
    }

    # 发送请求
    headers = {'Content-Type': 'application/json'}
    response = requests.post('http://127.0.0.1:8080/api/annotate', json=data, headers=headers)

    # 打印响应
    print(f"Status code: {response.status_code}")
    try:
        print(json.dumps(response.json(), indent=2))
    except:
        print(response.text)

    return response.json()["task_id"] if response.status_code == 200 else None

# 检查任务状态
def check_task_status(task_id):
    print(f"\nChecking task status for {task_id}...")

    # 发送请求
    response = requests.get(f'http://127.0.0.1:8080/api/tasks/{task_id}')

    # 打印响应
    print(f"Status code: {response.status_code}")
    try:
        result = response.json()
        print(json.dumps(result, indent=2))
        return result["status"]
    except:
        print(response.text)
        return None

# 获取任务结果
def get_task_results(task_id):
    print(f"\nGetting results for task {task_id}...")

    # 发送请求
    response = requests.get(f'http://127.0.0.1:8080/api/results/{task_id}')

    # 打印响应
    print(f"Status code: {response.status_code}")
    try:
        print(json.dumps(response.json(), indent=2))
    except:
        print(response.text)

if __name__ == "__main__":
    # 上传文件
    upload_data = upload_file()

    if upload_data:
        # 测试单个模型
        task_id = test_openai(upload_data)

        if task_id:
            # 检查任务状态
            status = check_task_status(task_id)

            # 如果任务已完成，获取结果
            if status == "completed":
                get_task_results(task_id)
            else:
                print(f"Task is still {status}. Please check later.")

        # 也可以测试其他模型
        # test_anthropic(upload_data)
        # test_gemini(upload_data)
        # test_grok(upload_data)
        # test_consensus(upload_data)
