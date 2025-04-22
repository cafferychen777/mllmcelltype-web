import os
import requests
import json
import time
from pprint import pprint

# 设置 API 密钥 - 请替换为您自己的 API 密钥
# 您可以通过环境变量设置 API 密钥，或者在此处直接设置
# 示例：
# os.environ["OPENAI_API_KEY"] = "your_openai_api_key_here"
# os.environ["ANTHROPIC_API_KEY"] = "your_anthropic_api_key_here"
# os.environ["GEMINI_API_KEY"] = "your_gemini_api_key_here"
# os.environ["QWEN_API_KEY"] = "your_qwen_api_key_here"
# os.environ["ZHIPU_API_KEY"] = "your_zhipu_api_key_here"
# os.environ["STEPFUN_API_KEY"] = "your_stepfun_api_key_here"
# os.environ["MINIMAX_API_KEY"] = "your_minimax_api_key_here"
# os.environ["MINIMAX_GROUP_ID"] = "your_minimax_group_id_here"
# os.environ["GROK_API_KEY"] = "your_grok_api_key_here"
# os.environ["OPENROUTER_API_KEY"] = "your_openrouter_api_key_here"

# 为了测试，您需要设置至少一个 API 密钥
# 如果您没有设置 API 密钥，测试将失败

# 定义要测试的模型（不包含 DeepSeek）
MODELS_TO_TEST = [
    {"provider": "openai", "model": "gpt-4.1", "name": "OpenAI GPT-4.1"},
    {"provider": "anthropic", "model": "claude-3-7-sonnet-20250219", "name": "Anthropic Claude 3.7 Sonnet"},
    {"provider": "gemini", "model": "gemini-2.5-pro-preview-03-25", "name": "Google Gemini 2.5 Pro"},
    {"provider": "grok", "model": "grok-3-beta", "name": "X.AI Grok 3 Beta"},
    {"provider": "qwen", "model": "qwen-max-2025-01-25", "name": "Qwen Max"},
    {"provider": "zhipu", "model": "glm-4", "name": "ZhipuAI GLM-4"},
    {"provider": "minimax", "model": "minimax-text-01", "name": "MiniMax Text"},
    {"provider": "stepfun", "model": "step-2-16k", "name": "StepFun 2-16k"}
]

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

# 测试单个模型
def test_model(upload_data, provider, model, name):
    print(f"\n{'='*50}")
    print(f"Testing {name} ({provider}/{model})")
    print(f"{'='*50}")

    # 准备请求数据
    data = {
        "task_id": upload_data["task_id"],
        "file_path": upload_data["file_path"],
        "species": "human",
        "tissue": "blood",
        "models": [model],
        "api_keys": {
            provider: os.environ[f"{provider.upper()}_API_KEY"]
        },
        "consensus_threshold": 0.7,
        "max_discussion_rounds": 3
    }

    # 如果是 MiniMax，添加 GROUP_ID
    if provider == "minimax":
        data["api_keys"]["minimax_group_id"] = os.environ["MINIMAX_GROUP_ID"]

    # 发送请求
    headers = {'Content-Type': 'application/json'}
    response = requests.post('http://127.0.0.1:8080/api/annotate', json=data, headers=headers)

    # 打印响应
    print(f"Status code: {response.status_code}")
    try:
        result = response.json()
        print(json.dumps(result, indent=2))
        return result["task_id"] if response.status_code == 200 else None
    except:
        print(response.text)
        return None

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
        result = response.json()
        print(json.dumps(result, indent=2))
        return result
    except:
        print(response.text)
        return None

# 等待任务完成
def wait_for_task_completion(task_id, timeout=60):
    print(f"\nWaiting for task {task_id} to complete...")

    start_time = time.time()
    while time.time() - start_time < timeout:
        status = check_task_status(task_id)
        if status == "completed":
            print(f"Task {task_id} completed successfully!")
            return True
        elif status == "failed":
            print(f"Task {task_id} failed!")
            return False

        print(f"Task status: {status}. Waiting 5 seconds...")
        time.sleep(5)

    print(f"Timeout waiting for task {task_id} to complete!")
    return False

# 测试多模型共识
def test_consensus(upload_data):
    print("\n\n" + "="*80)
    print("TESTING MULTI-MODEL CONSENSUS")
    print("="*80)

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
        result = response.json()
        print(json.dumps(result, indent=2))
        return result["task_id"] if response.status_code == 200 else None
    except:
        print(response.text)
        return None

if __name__ == "__main__":
    # 上传文件
    upload_data = upload_file()

    if upload_data:
        results = {}

        # 测试每个模型
        for model_info in MODELS_TO_TEST:
            provider = model_info["provider"]
            model = model_info["model"]
            name = model_info["name"]

            task_id = test_model(upload_data, provider, model, name)

            if task_id:
                # 等待任务完成
                if wait_for_task_completion(task_id):
                    # 获取结果
                    result = get_task_results(task_id)
                    if result and result["status"] == "completed":
                        results[name] = result["results"]["consensus"]
                        print(f"\nSuccessfully annotated with {name}:")
                        for cluster, cell_type in result["results"]["consensus"].items():
                            print(f"  Cluster {cluster}: {cell_type}")

            # 暂停一下，避免过快发送请求
            time.sleep(2)

        # 打印所有结果的比较
        print("\n\n" + "="*80)
        print("COMPARISON OF RESULTS FROM ALL MODELS")
        print("="*80)

        # 获取所有集群
        all_clusters = set()
        for model_results in results.values():
            all_clusters.update(model_results.keys())

        # 打印表头
        print(f"{'Cluster':<10}", end="")
        for model_info in MODELS_TO_TEST:
            name = model_info["name"]
            if name in results:
                print(f"{name:<25}", end="")
        print()

        # 打印分隔线
        print("-" * (10 + 25 * len(results)))

        # 打印每个集群的结果
        for cluster in sorted(all_clusters):
            print(f"{cluster:<10}", end="")
            for model_info in MODELS_TO_TEST:
                name = model_info["name"]
                if name in results:
                    cell_type = results[name].get(cluster, "N/A")
                    print(f"{cell_type:<25}", end="")
            print()

        # 测试多模型共识
        consensus_task_id = test_consensus(upload_data)

        if consensus_task_id:
            # 等待任务完成
            if wait_for_task_completion(consensus_task_id):
                # 获取结果
                consensus_result = get_task_results(consensus_task_id)
                if consensus_result and consensus_result["status"] == "completed":
                    print("\nConsensus Results:")
                    for cluster, cell_type in consensus_result["results"]["consensus"].items():
                        proportion = consensus_result["results"]["consensus_proportion"][cluster]
                        print(f"  Cluster {cluster}: {cell_type} (Consensus: {proportion*100:.1f}%)")

                    print("\nIndividual Model Predictions:")
                    for model, predictions in consensus_result["results"]["model_annotations"].items():
                        print(f"  {model}:")
                        for cluster, cell_type in predictions.items():
                            print(f"    Cluster {cluster}: {cell_type}")
