#!/usr/bin/env python3
"""
mLLMCelltype Web - 轻量级 Web 界面
用于细胞类型注释的 Web 应用程序
"""

from flask import Flask, request, jsonify, send_file, render_template, url_for, redirect
from werkzeug.utils import secure_filename
import pandas as pd
import numpy as np
import csv
import json
import uuid
import os
import threading
import time
import json
import logging
import shutil
from datetime import datetime, timedelta
import sys

# 添加 mLLMCelltype 到 Python 路径
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../python')))

# 导入 mLLMCelltype 函数
try:
    from mllmcelltype import annotate_clusters, interactive_consensus_annotation, setup_logging
    MLLMCELLTYPE_AVAILABLE = True
    print("Successfully imported mLLMCelltype package.")
except ImportError as e:
    print(f"Warning: mLLMCelltype package import error: {str(e)}")
    print("Python path:")
    for p in sys.path:
        print(f"  - {p}")
    print("Attempting to import directly from python directory...")
    try:
        sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../python')))
        from mllmcelltype import annotate_clusters, interactive_consensus_annotation, setup_logging
        MLLMCELLTYPE_AVAILABLE = True
        print("Successfully imported mLLMCelltype package from python directory.")
    except ImportError as e2:
        print(f"Failed to import mLLMCelltype: {str(e2)}")
        MLLMCELLTYPE_AVAILABLE = False
        print("Running in demo mode.")

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(os.path.join('logs', 'app.log')),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# 修改 Jinja2 分隔符，避免与 Vue.js 冲突
app.jinja_env.variable_start_string = '{[{'
app.jinja_env.variable_end_string = '}]}'

app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 限制上传文件大小为 16MB
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['RESULTS_FOLDER'] = 'results'
app.config['ALLOWED_EXTENSIONS'] = {'csv', 'tsv', 'xls', 'xlsx'}

# 存储任务状态
tasks = {}

# 确保目录存在
for folder in [app.config['UPLOAD_FOLDER'], app.config['RESULTS_FOLDER'], 'logs']:
    os.makedirs(folder, exist_ok=True)

def allowed_file(filename):
    """检查文件是否为允许的类型"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def create_user_folder(task_id):
    """为每个任务创建隔离的文件夹"""
    upload_folder = os.path.join(app.config['UPLOAD_FOLDER'], task_id)
    results_folder = os.path.join(app.config['RESULTS_FOLDER'], task_id)

    os.makedirs(upload_folder, exist_ok=True)
    os.makedirs(results_folder, exist_ok=True)

    return upload_folder, results_folder

def process_annotation_task(task_id, file_path, species, tissue, models, api_keys,
                           consensus_threshold, max_discussion_rounds):
    """后台处理注释任务"""
    try:
        tasks[task_id]["status"] = "processing"
        logger.info(f"Processing task {task_id}")

        # 设置API密钥环境变量
        original_env = {}
        for provider, key in api_keys.items():
            env_var = f"{provider.upper()}_API_KEY"
            # 保存原始环境变量（如果存在）
            if env_var in os.environ:
                original_env[env_var] = os.environ[env_var]
            os.environ[env_var] = key

        # 创建结果目录
        results_folder = os.path.join(app.config['RESULTS_FOLDER'], task_id)

        try:
            # 读取数据
            if file_path.endswith('.csv'):
                df = pd.read_csv(file_path)
            elif file_path.endswith('.tsv'):
                df = pd.read_csv(file_path, sep='\t')
            elif file_path.endswith(('.xls', '.xlsx')):
                df = pd.read_excel(file_path)

            # 提取标记基因
            marker_genes = {}

            # 尝试检测数据格式
            if len(df.columns) >= 2:
                # 假设第一列是集群ID，其余列是基因
                for _, row in df.iterrows():
                    cluster_id = str(row.iloc[0])
                    genes = [gene for gene in row.iloc[1:] if pd.notna(gene) and str(gene).strip()]
                    if genes:
                        marker_genes[cluster_id] = genes

            # 如果没有检测到标记基因，尝试另一种格式
            if not marker_genes and 'cluster' in df.columns.str.lower() and 'genes' in df.columns.str.lower():
                # 假设有 'cluster' 和 'genes' 列
                cluster_col = df.columns[df.columns.str.lower() == 'cluster'][0]
                genes_col = df.columns[df.columns.str.lower() == 'genes'][0]

                for _, row in df.iterrows():
                    cluster_id = str(row[cluster_col])
                    genes_str = row[genes_col]
                    if pd.notna(genes_str):
                        # 尝试分割基因字符串（可能是逗号分隔的）
                        genes = [g.strip() for g in str(genes_str).split(',') if g.strip()]
                        if genes:
                            marker_genes[cluster_id] = genes

            if not marker_genes:
                raise ValueError("无法从文件中提取标记基因。请检查文件格式。")

            logger.info(f"Extracted marker genes for {len(marker_genes)} clusters")

            # 运行注释
            if MLLMCELLTYPE_AVAILABLE:
                try:
                    if len(models) == 1:
                        # 单模型注释
                        if '/' in models[0]:
                            provider = 'openrouter'
                            model = models[0]
                            logger.info(f"Using OpenRouter with model: {model}")
                        else:
                            provider, model = 'openai', models[0]  # 默认使用 OpenAI

                            # 尝试从模型名称推断提供商
                            if 'claude' in model.lower():
                                provider = 'anthropic'
                            elif 'gemini' in model.lower():
                                provider = 'gemini'
                            elif 'grok' in model.lower():
                                provider = 'grok'
                            elif 'glm' in model.lower():
                                provider = 'zhipu'
                            elif 'qwen' in model.lower():
                                provider = 'qwen'
                            elif 'deepseek' in model.lower():
                                provider = 'deepseek'
                            elif 'minimax' in model.lower():
                                provider = 'minimax'
                            elif 'step' in model.lower():
                                provider = 'stepfun'

                            logger.info(f"Inferred provider '{provider}' from model name: {model}")

                        logger.info(f"Running single model annotation with {provider}/{model}")

                        # 检查 API 密钥
                        env_var = f"{provider.upper()}_API_KEY"
                        if env_var in os.environ and os.environ[env_var]:
                            logger.info(f"Found API key for {provider}")
                        else:
                            logger.warning(f"No API key found for {provider} in environment variable {env_var}")

                        results = annotate_clusters(
                            marker_genes=marker_genes,
                            species=species,
                            tissue=tissue,
                            provider=provider,
                            model=model
                        )
                        # 转换为统一格式
                        formatted_results = {
                            "consensus": results,
                            "consensus_proportion": {k: 1.0 for k in results},
                            "entropy": {k: 0.0 for k in results},
                            "model_predictions": {model: results}
                        }
                    else:
                        # 多模型共识注释
                        logger.info(f"Running consensus annotation with {len(models)} models: {', '.join(models)}")

                        # 检查所有模型的 API 密钥
                        for model in models:
                            if '/' in model:
                                provider = 'openrouter'
                            else:
                                provider = 'openai'  # 默认
                                if 'claude' in model.lower():
                                    provider = 'anthropic'
                                elif 'gemini' in model.lower():
                                    provider = 'gemini'
                                elif 'grok' in model.lower():
                                    provider = 'grok'
                                elif 'glm' in model.lower():
                                    provider = 'zhipu'
                                elif 'qwen' in model.lower():
                                    provider = 'qwen'
                                elif 'deepseek' in model.lower():
                                    provider = 'deepseek'
                                elif 'minimax' in model.lower():
                                    provider = 'minimax'
                                elif 'step' in model.lower():
                                    provider = 'stepfun'

                            env_var = f"{provider.upper()}_API_KEY"
                            if env_var in os.environ and os.environ[env_var]:
                                logger.info(f"Found API key for {provider} (model: {model})")
                            else:
                                logger.warning(f"No API key found for {provider} (model: {model}) in environment variable {env_var}")

                        formatted_results = interactive_consensus_annotation(
                            marker_genes=marker_genes,
                            species=species,
                            tissue=tissue,
                            models=models,
                            consensus_threshold=consensus_threshold,
                            max_discussion_rounds=max_discussion_rounds,
                            verbose=True
                        )
                except Exception as e:
                    logger.error(f"Error during annotation: {str(e)}", exc_info=True)
                    raise
            else:
                # 演示模式 - 生成模拟结果
                logger.warning("Running in demo mode with simulated results")
                cell_types = ["T cells", "B cells", "Monocytes", "NK cells", "Dendritic cells",
                             "Macrophages", "Neutrophils", "Plasma cells"]

                results = {}
                for cluster_id in marker_genes.keys():
                    results[cluster_id] = np.random.choice(cell_types)

                formatted_results = {
                    "consensus": results,
                    "consensus_proportion": {k: round(np.random.uniform(0.7, 1.0), 2) for k in results},
                    "entropy": {k: round(np.random.uniform(0.0, 0.5), 2) for k in results},
                    "model_predictions": {model: {k: np.random.choice(cell_types) for k in results} for model in models}
                }

            # 保存结果
            result_path = os.path.join(results_folder, "results.json")
            with open(result_path, "w") as f:
                json.dump(formatted_results, f)

            # 创建CSV结果
            csv_result_path = os.path.join(results_folder, "results.csv")
            result_df = pd.DataFrame({
                "Cluster": list(formatted_results["consensus"].keys()),
                "Cell Type": list(formatted_results["consensus"].values()),
                "Consensus Proportion": [formatted_results["consensus_proportion"].get(k, "N/A")
                                        for k in formatted_results["consensus"]],
                "Entropy": [formatted_results["entropy"].get(k, "N/A")
                           for k in formatted_results["consensus"]]
            })
            result_df.to_csv(csv_result_path, index=False)

            # 创建Excel结果
            excel_result_path = os.path.join(results_folder, "results.xlsx")
            result_df.to_excel(excel_result_path, index=False)

            # 创建TSV结果
            tsv_result_path = os.path.join(results_folder, "results.tsv")
            result_df.to_csv(tsv_result_path, sep='\t', index=False)

            tasks[task_id]["status"] = "completed"
            tasks[task_id]["results"] = formatted_results
            tasks[task_id]["result_paths"] = {
                "json": result_path,
                "csv": csv_result_path,
                "excel": excel_result_path,
                "tsv": tsv_result_path
            }
            logger.info(f"Task {task_id} completed successfully")

        finally:
            # 恢复原始环境变量
            for env_var, value in original_env.items():
                os.environ[env_var] = value

            # 删除不再需要的环境变量
            for provider in api_keys.keys():
                env_var = f"{provider.upper()}_API_KEY"
                if env_var not in original_env and env_var in os.environ:
                    del os.environ[env_var]

    except Exception as e:
        logger.error(f"Error processing task {task_id}: {str(e)}", exc_info=True)
        tasks[task_id]["status"] = "failed"
        tasks[task_id]["error"] = str(e)

@app.route('/')
def index():
    """主页"""
    return render_template('index.html')

@app.route('/api/upload', methods=['POST'])
def upload_file():
    """处理文件上传"""
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if not allowed_file(file.filename):
        return jsonify({"error": "Unsupported file format. Please upload CSV, TSV, or Excel file."}), 400

    # 生成唯一ID
    task_id = str(uuid.uuid4())

    # 创建用户文件夹
    upload_folder, _ = create_user_folder(task_id)

    # 保存上传的文件
    filename = secure_filename(file.filename)
    file_path = os.path.join(upload_folder, filename)
    file.save(file_path)

    logger.info(f"File uploaded: {file_path} for task {task_id}")

    # 读取并预览数据
    try:
        if file.filename.endswith('.csv'):
            df = pd.read_csv(file_path)
        elif file.filename.endswith('.tsv'):
            df = pd.read_csv(file_path, sep='\t')
        elif file.filename.endswith(('.xls', '.xlsx')):
            df = pd.read_excel(file_path)

        # 限制预览大小
        preview_df = df.head(5)

        # 转换为可序列化的格式
        preview = preview_df.to_dict(orient='records')
        columns = df.columns.tolist()

    except Exception as e:
        logger.error(f"Error reading file: {str(e)}", exc_info=True)
        # 删除上传的文件
        os.remove(file_path)
        return jsonify({"error": f"Failed to read file: {str(e)}"}), 400

    # 记录任务
    tasks[task_id] = {
        "status": "uploaded",
        "created_at": time.time(),
        "file_path": file_path,
        "filename": filename
    }

    # 返回预览和任务ID
    return jsonify({
        "task_id": task_id,
        "file_path": file_path,
        "preview": preview,
        "columns": columns
    })

@app.route('/api/annotate', methods=['POST'])
def start_annotation():
    """开始注释任务"""
    data = request.json
    task_id = data.get("task_id")
    file_path = data.get("file_path")
    species = data.get("species")
    tissue = data.get("tissue")
    models = data.get("models", [])
    api_keys = data.get("api_keys", {})
    consensus_threshold = float(data.get("consensus_threshold", 0.7))
    max_discussion_rounds = int(data.get("max_discussion_rounds", 3))

    if not all([task_id, file_path, species, models]):
        return jsonify({"error": "Missing required parameters"}), 400

    if task_id not in tasks:
        return jsonify({"error": "Invalid task ID"}), 404

    if not os.path.exists(file_path):
        return jsonify({"error": "File not found"}), 404

    # 更新任务状态
    tasks[task_id].update({
        "status": "queued",
        "species": species,
        "tissue": tissue,
        "models": models,
        "consensus_threshold": consensus_threshold,
        "max_discussion_rounds": max_discussion_rounds
    })

    logger.info(f"Starting annotation task {task_id} with models: {models}")

    # 启动后台线程处理任务
    thread = threading.Thread(
        target=process_annotation_task,
        args=(task_id, file_path, species, tissue, models, api_keys,
              consensus_threshold, max_discussion_rounds)
    )
    thread.daemon = True
    thread.start()

    return jsonify({"task_id": task_id, "status": "queued"})

@app.route('/api/tasks/<task_id>', methods=['GET'])
def get_task_status(task_id):
    """获取任务状态"""
    if task_id not in tasks:
        return jsonify({"error": "Task not found"}), 404

    task_info = {
        "task_id": task_id,
        "status": tasks[task_id]["status"],
        "created_at": tasks[task_id]["created_at"]
    }

    if "error" in tasks[task_id]:
        task_info["error"] = tasks[task_id]["error"]

    return jsonify(task_info)

@app.route('/api/results/<task_id>', methods=['GET'])
def get_results(task_id):
    """获取任务结果"""
    if task_id not in tasks:
        return jsonify({"error": "Task not found"}), 404

    if tasks[task_id]["status"] != "completed":
        return jsonify({
            "task_id": task_id,
            "status": tasks[task_id]["status"],
            "error": tasks[task_id].get("error")
        }), 200

    return jsonify({
        "task_id": task_id,
        "status": "completed",
        "results": tasks[task_id]["results"]
    })

@app.route('/api/download/<task_id>/<format>', methods=['GET'])
def download_results(task_id, format):
    """下载结果文件"""
    if task_id not in tasks:
        return jsonify({"error": "Task not found"}), 404

    if tasks[task_id]["status"] != "completed":
        return jsonify({"error": "Task not completed yet"}), 400

    if format not in ["csv", "excel", "tsv"]:
        return jsonify({"error": "Unsupported format"}), 400

    if "result_paths" not in tasks[task_id]:
        return jsonify({"error": "Result files not found"}), 404

    file_path = tasks[task_id]["result_paths"][format]

    if not os.path.exists(file_path):
        return jsonify({"error": "Result file not found"}), 404

    # 设置文件名
    filename = f"mLLMCelltype_results_{task_id}"
    if format == "csv":
        filename += ".csv"
        mimetype = "text/csv"
    elif format == "excel":
        filename += ".xlsx"
        mimetype = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    elif format == "tsv":
        filename += ".tsv"
        mimetype = "text/tab-separated-values"

    return send_file(file_path, mimetype=mimetype, as_attachment=True, download_name=filename)

@app.route('/api/sample', methods=['GET'])
def get_sample_data():
    """获取示例数据"""
    sample_data = {
        "1": ["CD3D", "CD3E", "CD3G", "CD2", "IL7R", "TCF7"],
        "2": ["CD19", "MS4A1", "CD79A", "CD79B", "HLA-DRA", "CD74"],
        "3": ["CD14", "LYZ", "CSF1R", "ITGAM", "CD68", "FCGR3A"]
    }

    # 创建示例CSV
    df = pd.DataFrame()
    df['Cluster'] = list(sample_data.keys())

    # 找出最长的基因列表
    max_genes = max(len(genes) for genes in sample_data.values())

    # 添加基因列
    for i in range(max_genes):
        df[f'Gene_{i+1}'] = [genes[i] if i < len(genes) else "" for genes in sample_data.values()]

    # 创建临时文件
    temp_file = os.path.join(app.config['UPLOAD_FOLDER'], "sample_data.csv")
    df.to_csv(temp_file, index=False)

    return send_file(temp_file, mimetype="text/csv", as_attachment=True, download_name="mLLMCelltype_sample_data.csv")

def cleanup_old_tasks():
    """清理过期任务"""
    current_time = time.time()
    for task_id in list(tasks.keys()):
        # 24小时后删除任务
        if current_time - tasks[task_id]["created_at"] > 86400:  # 24小时
            logger.info(f"Cleaning up old task {task_id}")

            # 删除任务文件夹
            upload_folder = os.path.join(app.config['UPLOAD_FOLDER'], task_id)
            results_folder = os.path.join(app.config['RESULTS_FOLDER'], task_id)

            if os.path.exists(upload_folder):
                shutil.rmtree(upload_folder)

            if os.path.exists(results_folder):
                shutil.rmtree(results_folder)

            # 删除任务记录
            del tasks[task_id]

# 启动定期清理任务
def start_cleanup_scheduler():
    """启动定期清理任务"""
    def run_cleanup():
        while True:
            cleanup_old_tasks()
            time.sleep(3600)  # 每小时运行一次

    cleanup_thread = threading.Thread(target=run_cleanup)
    cleanup_thread.daemon = True
    cleanup_thread.start()

def check_mllmcelltype_installation():
    """Check if mLLMCelltype is properly installed and available"""
    if MLLMCELLTYPE_AVAILABLE:
        logger.info("mLLMCelltype package is available and will be used for annotations.")
        # Log available providers
        try:
            from mllmcelltype.functions import get_provider
            providers = [
                "openai", "anthropic", "gemini", "deepseek", "qwen",
                "zhipu", "minimax", "grok", "openrouter", "stepfun"
            ]
            available_providers = []
            for provider in providers:
                try:
                    get_provider(provider)
                    available_providers.append(provider)
                except Exception as e:
                    logger.warning(f"Provider {provider} not available: {str(e)}")

            logger.info(f"Available providers: {', '.join(available_providers)}")
        except Exception as e:
            logger.error(f"Error checking available providers: {str(e)}")
    else:
        logger.warning("mLLMCelltype package is not available. Running in demo mode.")
        logger.warning("Annotations will be simulated and not use actual LLM APIs.")

if __name__ == '__main__':
    start_cleanup_scheduler()
    # Check mLLMCelltype installation after logger is configured
    check_mllmcelltype_installation()
    app.run(debug=True, host='0.0.0.0', port=8080)
