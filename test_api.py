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

# 测试 OpenAI 模型
def test_openai():
    print("Testing OpenAI GPT-4.1 model...")

    # 准备文件上传
    files = {'file': open('uploads/sample_data.csv', 'rb')}

    # 准备表单数据
    data = {
        'provider': 'openai',
        'model': 'gpt-4.1',
        'species': 'human',
        'tissue': 'blood',
        'consensus_threshold': '0.7',
        'max_discussion_rounds': '3'
    }

    # 发送请求
    response = requests.post('http://127.0.0.1:8080/api/annotate', files=files, data=data)

    # 打印响应
    print(f"Status code: {response.status_code}")
    try:
        print(json.dumps(response.json(), indent=2))
    except:
        print(response.text)

# 测试 Anthropic 模型
def test_anthropic():
    print("\nTesting Anthropic Claude 3.7 Sonnet model...")

    # 准备文件上传
    files = {'file': open('uploads/sample_data.csv', 'rb')}

    # 准备表单数据
    data = {
        'provider': 'anthropic',
        'model': 'claude-3-7-sonnet-20250219',
        'species': 'human',
        'tissue': 'blood',
        'consensus_threshold': '0.7',
        'max_discussion_rounds': '3'
    }

    # 发送请求
    response = requests.post('http://127.0.0.1:8080/api/annotate', files=files, data=data)

    # 打印响应
    print(f"Status code: {response.status_code}")
    try:
        print(json.dumps(response.json(), indent=2))
    except:
        print(response.text)

# 测试 Gemini 模型
def test_gemini():
    print("\nTesting Google Gemini 2.5 Pro model...")

    # 准备文件上传
    files = {'file': open('uploads/sample_data.csv', 'rb')}

    # 准备表单数据
    data = {
        'provider': 'gemini',
        'model': 'gemini-2.5-pro-preview-03-25',
        'species': 'human',
        'tissue': 'blood',
        'consensus_threshold': '0.7',
        'max_discussion_rounds': '3'
    }

    # 发送请求
    response = requests.post('http://127.0.0.1:8080/api/annotate', files=files, data=data)

    # 打印响应
    print(f"Status code: {response.status_code}")
    try:
        print(json.dumps(response.json(), indent=2))
    except:
        print(response.text)

# 测试 Grok 模型
def test_grok():
    print("\nTesting X.AI Grok 3 Beta model...")

    # 准备文件上传
    files = {'file': open('uploads/sample_data.csv', 'rb')}

    # 准备表单数据
    data = {
        'provider': 'grok',
        'model': 'grok-3-beta',
        'species': 'human',
        'tissue': 'blood',
        'consensus_threshold': '0.7',
        'max_discussion_rounds': '3'
    }

    # 发送请求
    response = requests.post('http://127.0.0.1:8080/api/annotate', files=files, data=data)

    # 打印响应
    print(f"Status code: {response.status_code}")
    try:
        print(json.dumps(response.json(), indent=2))
    except:
        print(response.text)

# 测试多模型共识
def test_consensus():
    print("\nTesting multi-model consensus annotation...")

    # 准备文件上传
    files = {'file': open('uploads/sample_data.csv', 'rb')}

    # 准备表单数据
    data = {
        'models': ['gpt-4.1', 'claude-3-7-sonnet-20250219', 'gemini-2.5-pro-preview-03-25', 'grok-3-beta'],
        'species': 'human',
        'tissue': 'blood',
        'consensus_threshold': '0.7',
        'max_discussion_rounds': '3'
    }

    # 发送请求
    response = requests.post('http://127.0.0.1:8080/api/annotate', files=files, data=data)

    # 打印响应
    print(f"Status code: {response.status_code}")
    try:
        print(json.dumps(response.json(), indent=2))
    except:
        print(response.text)

if __name__ == "__main__":
    # 测试单个模型
    test_openai()
    test_anthropic()
    test_gemini()
    test_grok()

    # 测试多模型共识
    # test_consensus()
