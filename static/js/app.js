// mLLMCelltype Web 应用

new Vue({
    el: '#app',
    data: {
        // 语言设置
        currentLang: 'en', // 默认英文

        // 页面控制
        currentPage: 'upload',

        // 上传相关
        isDragover: false,
        isUploading: false,
        uploadError: '',

        // 任务相关
        taskId: null,
        filePath: null,
        taskStatus: 'Preparing',
        processingError: '',

        // 数据预览
        dataPreview: [],
        dataColumns: [],

        // 配置参数
        species: 'human',
        tissue: '',
        consensusThreshold: 0.7,
        maxDiscussionRounds: 3,

        // 语言翻译
        translations: {
            en: {
                // 导航栏
                paper: 'Paper',
                github: 'GitHub',

                // 上传页面
                uploadTitle: 'Upload Data File',
                uploadDescription: 'Upload a file containing marker genes for cell type annotation.',
                dragDropText: 'Drag and drop file here or click to select',
                selectFile: 'Select File',
                uploadingText: 'Uploading, please wait...',
                supportedFormats: 'Supported formats: CSV, TSV, Excel',
                downloadSample: 'Download Sample Data',

                // 配置页面
                configTitle: 'Configure Annotation Parameters',
                dataPreviewTitle: 'Data Preview:',
                speciesLabel: 'Species',
                tissueLabel: 'Tissue Type',
                tissuePlaceholder: 'e.g., Blood, Brain, Lung',
                tissueHelp: 'Providing tissue context can improve annotation accuracy',
                modelSelectionLabel: 'Model Selection',
                modelLabel: 'Model',
                apiKeyLabel: 'API Key',
                apiKeyPlaceholder: 'Enter API Key',
                apiKeyHelp: 'API keys are only used in the current session and will not be stored',
                modelWarning: 'Please select at least one model provider',
                advancedOptionsLabel: 'Advanced Options',
                consensusThresholdLabel: 'Consensus Threshold',
                consensusThresholdHelp: 'Minimum proportion for models to reach consensus (0.1-1.0)',
                maxRoundsLabel: 'Max Discussion Rounds',
                maxRoundsHelp: 'Maximum number of discussion rounds between models (1-5)',
                backButton: 'Back',
                startAnnotationButton: 'Start Annotation',

                // 处理页面
                processingTitle: 'Processing',
                processingDescription: 'Annotating cell types using selected models...',

                // 结果页面
                resultsTitle: 'Annotation Results',
                resultsDescription: 'Annotation complete! Below are the annotation results for each cell type.',
                clusterHeader: 'Cluster',
                cellTypeHeader: 'Cell Type',
                consensusHeader: 'Consensus Proportion (CP)',
                entropyHeader: 'Entropy (H)',
                newAnnotationButton: 'New Annotation',
                downloadCSV: 'Download CSV',
                downloadExcel: 'Download Excel',
                downloadTSV: 'Download TSV',

                // 状态文本
                statusQueued: 'Queued',
                statusProcessing: 'Processing',
                statusCompleted: 'Completed',
                statusFailed: 'Failed',

                // 错误消息
                fileTypeError: 'Unsupported file type: {fileExt}. Please upload CSV, TSV or Excel file.',
                fileSizeError: 'File is too large, please upload a file smaller than 16MB.',
                uploadError: 'Upload failed, please try again.',
                annotationError: 'Failed to start annotation task, please try again.',
                processingError: 'Processing failed, please try again.',
                statusCheckError: 'Failed to check task status, please refresh the page and try again.',
                resultsNotReady: 'Results are not ready yet, please try again later.',
                resultsError: 'Failed to get results, please try again.',

                // 页脚
                footerText: 'based on',
                lightweightInterface: 'lightweight Web interface'
            },
            zh: {
                // 导航栏
                paper: 'Paper',
                github: 'GitHub',

                // 上传页面
                uploadTitle: '上传数据文件',
                uploadDescription: '上传包含标记基因的文件进行细胞类型注释。',
                dragDropText: '拖放文件到此处或点击选择文件',
                selectFile: '选择文件',
                uploadingText: '上传中，请稍候...',
                supportedFormats: '支持的格式: CSV, TSV, Excel',
                downloadSample: '下载示例数据',

                // 配置页面
                configTitle: '配置注释参数',
                dataPreviewTitle: '数据预览:',
                speciesLabel: '物种',
                tissueLabel: '组织类型',
                tissuePlaceholder: '例如: 血液, 大脑, 肺',
                tissueHelp: '提供组织上下文可以提高注释准确性',
                modelSelectionLabel: '模型选择',
                modelLabel: '模型',
                apiKeyLabel: 'API 密钥',
                apiKeyPlaceholder: '输入 API 密钥',
                apiKeyHelp: 'API 密钥仅在当前会话中使用，不会被存储',
                modelWarning: '请至少选择一个模型提供商',
                advancedOptionsLabel: '高级选项',
                consensusThresholdLabel: '共识阈值',
                consensusThresholdHelp: '模型间达成共识的最小比例 (0.1-1.0)',
                maxRoundsLabel: '最大讨论轮数',
                maxRoundsHelp: '模型间讨论的最大轮数 (1-5)',
                backButton: '返回',
                startAnnotationButton: '开始注释',

                // 处理页面
                processingTitle: '处理中',
                processingDescription: '正在使用选定的模型进行细胞类型注释...',

                // 结果页面
                resultsTitle: '注释结果',
                resultsDescription: '注释完成！下面是每个细胞类型的注释结果。',
                clusterHeader: '集群',
                cellTypeHeader: '细胞类型',
                consensusHeader: '共识比例 (CP)',
                entropyHeader: '熵 (H)',
                newAnnotationButton: '新的注释',
                downloadCSV: '下载 CSV',
                downloadExcel: '下载 Excel',
                downloadTSV: '下载 TSV',

                // 状态文本
                statusQueued: '排队中',
                statusProcessing: '处理中',
                statusCompleted: '已完成',
                statusFailed: '失败',

                // 错误消息
                fileTypeError: '不支持的文件类型: {fileExt}。请上传 CSV, TSV 或 Excel 文件。',
                fileSizeError: '文件太大，请上传小于 16MB 的文件。',
                uploadError: '上传失败，请重试。',
                annotationError: '启动注释任务失败，请重试。',
                processingError: '处理失败，请重试。',
                statusCheckError: '检查任务状态失败，请刷新页面重试。',
                resultsNotReady: '结果尚未准备好，请稍后再试。',
                resultsError: '获取结果失败，请重试。',

                // 页脚
                footerText: '基于',
                lightweightInterface: '的轻量级 Web 界面'
            }
        },

        // 模型提供商
        availableProviders: [
            {
                id: 'openai',
                name: 'OpenAI',
                selected: true,
                apiKey: '',
                selectedModel: 'gpt-4o',
                models: [
                    // GPT-4.1 系列
                    { id: 'gpt-4.1', name: 'GPT-4.1' },
                    { id: 'gpt-4.1-mini', name: 'GPT-4.1 Mini' },
                    { id: 'gpt-4.1-nano', name: 'GPT-4.1 Nano' },
                    // GPT-4o 系列
                    { id: 'gpt-4o', name: 'GPT-4o' },
                    { id: 'gpt-4o-mini', name: 'GPT-4o Mini' },
                    // o 系列
                    { id: 'o4-mini', name: 'o4 Mini' },
                    { id: 'o3', name: 'o3' },
                    // 其他
                    { id: 'gpt-4-turbo', name: 'GPT-4 Turbo' },
                    { id: 'gpt-4', name: 'GPT-4' },
                    { id: 'gpt-3.5-turbo', name: 'GPT-3.5 Turbo' }
                ]
            },
            {
                id: 'anthropic',
                name: 'Anthropic',
                selected: false,
                apiKey: '',
                selectedModel: 'claude-3-7-sonnet-20250219',
                models: [
                    // Claude 3.7 系列
                    { id: 'claude-3-7-sonnet-20250219', name: 'Claude 3.7 Sonnet' },

                    // Claude 3.5 系列
                    { id: 'claude-3-5-sonnet-20241022', name: 'Claude 3.5 Sonnet (New)' },
                    { id: 'claude-3-5-sonnet-20240620', name: 'Claude 3.5 Sonnet (Old)' },
                    { id: 'claude-3-5-haiku-20241022', name: 'Claude 3.5 Haiku' },

                    // Claude 3 系列
                    { id: 'claude-3-opus-20240229', name: 'Claude 3 Opus' },
                    { id: 'claude-3-haiku-20240307', name: 'Claude 3 Haiku' }
                ]
            },
            {
                id: 'gemini',
                name: 'Google (Gemini)',
                selected: false,
                apiKey: '',
                selectedModel: 'gemini-2.5-pro-preview-03-25',
                models: [
                    // Gemini 2.5 系列
                    { id: 'gemini-2.5-pro-preview-03-25', name: 'Gemini 2.5 Pro Preview' },
                    { id: 'gemini-2.5-flash-preview-04-17', name: 'Gemini 2.5 Flash Preview' },
                    // Gemini 2.0 系列
                    { id: 'gemini-2.0-flash', name: 'Gemini 2.0 Flash' },
                    { id: 'gemini-2.0-flash-001', name: 'Gemini 2.0 Flash 001' },
                    { id: 'gemini-2.0-flash-lite', name: 'Gemini 2.0 Flash Lite' },
                    // Gemini 1.5 系列
                    { id: 'gemini-1.5-pro', name: 'Gemini 1.5 Pro' },
                    { id: 'gemini-1.5-pro-latest', name: 'Gemini 1.5 Pro Latest' },
                    { id: 'gemini-1.5-flash', name: 'Gemini 1.5 Flash' },
                    { id: 'gemini-1.5-flash-latest', name: 'Gemini 1.5 Flash Latest' },
                    { id: 'gemini-1.5-flash-8b', name: 'Gemini 1.5 Flash 8B' }
                ]
            },
            {
                id: 'openrouter',
                name: 'OpenRouter',
                selected: false,
                apiKey: '',
                selectedModel: 'openai/gpt-4.1',
                models: [
                    // OpenAI
                    { id: 'openai/gpt-4.1', name: 'OpenAI GPT-4.1' },
                    { id: 'openai/o3', name: 'OpenAI o3' },
                    { id: 'openai/o4-mini', name: 'OpenAI o4 Mini' },
                    { id: 'openai/gpt-4o', name: 'OpenAI GPT-4o' },
                    // Anthropic
                    { id: 'anthropic/claude-3.7-sonnet', name: 'Anthropic Claude 3.7 Sonnet' },
                    { id: 'anthropic/claude-3.5-sonnet', name: 'Anthropic Claude 3.5 Sonnet' },
                    { id: 'anthropic/claude-3-opus', name: 'Anthropic Claude 3 Opus' },
                    // Meta
                    { id: 'meta-llama/llama-4-maverick', name: 'Meta Llama 4 Maverick' },
                    { id: 'meta-llama/llama-4-scout', name: 'Meta Llama 4 Scout' },
                    { id: 'meta-llama/llama-3.3-70b-instruct', name: 'Meta Llama 3.3 70B' },
                    // Mistral
                    { id: 'mistralai/mistral-large', name: 'Mistral Large' },
                    // Google
                    { id: 'google/gemini-2.5-pro-preview-03-25', name: 'Google Gemini 2.5 Pro' },
                    // X.AI
                    { id: 'x-ai/grok-3-beta', name: 'X.AI Grok 3' }
                ]
            },
            {
                id: 'grok',
                name: 'X.AI (Grok)',
                selected: false,
                apiKey: '',
                selectedModel: 'grok-3-beta',
                models: [
                    // Grok 3 系列
                    { id: 'grok-3-beta', name: 'Grok 3 Beta' },
                    { id: 'grok-3-mini-beta', name: 'Grok 3 Mini Beta' },
                    { id: 'grok-3-fast-beta', name: 'Grok 3 Fast Beta' },
                    { id: 'grok-3-mini-fast-beta', name: 'Grok 3 Mini Fast Beta' },
                    // Grok 2 系列
                    { id: 'grok-2-1212', name: 'Grok 2' },
                    { id: 'grok-2-vision-1212', name: 'Grok 2 Vision' },
                    { id: 'grok-2-image-1212', name: 'Grok 2 Image' },
                    // Grok 1 系列
                    { id: 'grok-beta', name: 'Grok Beta' },
                    { id: 'grok-vision-beta', name: 'Grok Vision Beta' }
                ]
            },
            {
                id: 'deepseek',
                name: 'DeepSeek',
                selected: false,
                apiKey: '',
                selectedModel: 'deepseek-chat',
                models: [
                    { id: 'deepseek-chat', name: 'DeepSeek Chat' },
                    { id: 'deepseek-v3-0324', name: 'DeepSeek V3 0324' },
                    { id: 'deepseek-r1', name: 'DeepSeek R1' },
                    { id: 'deepseek-r1-zero', name: 'DeepSeek R1 Zero' }
                ]
            },
            {
                id: 'minimax',
                name: 'MiniMax',
                selected: false,
                apiKey: '',
                selectedModel: 'MiniMax-Text-01',
                models: [
                    { id: 'MiniMax-Text-01', name: 'MiniMax Text 01' }
                ]
            },
            {
                id: 'qwen',
                name: 'Qwen (Alibaba)',
                selected: false,
                apiKey: '',
                selectedModel: 'qwen-max-2025-01-25',
                models: [
                    // Qwen 2.5 系列
                    { id: 'qwen-max-2025-01-25', name: 'Qwen Max' },
                    { id: 'qwen-plus', name: 'Qwen Plus' },
                    { id: 'qwen-turbo', name: 'Qwen Turbo' },
                    // Qwen 2.5 VL 系列
                    { id: 'qwen-vl-max', name: 'Qwen VL Max' },
                    { id: 'qwen-vl-plus', name: 'Qwen VL Plus' },
                    // Qwen 2.5 Coder 系列
                    { id: 'qwen2.5-coder-7b-instruct', name: 'Qwen 2.5 Coder 7B' },
                    { id: 'qwen-2.5-coder-32b-instruct', name: 'Qwen 2.5 Coder 32B' }
                ]
            },
            {
                id: 'stepfun',
                name: 'StepFun',
                selected: false,
                apiKey: '',
                selectedModel: 'step-2-16k',
                models: [
                    // 极速版大模型
                    { id: 'step-1-flash', name: 'Step-1-Flash (8k)' },
                    { id: 'step-2-mini', name: 'Step-2-Mini (32k)' },
                    // 万亿参数大模型
                    { id: 'step-2-16k', name: 'Step-2-16k' },
                    { id: 'step-2-16k-exp', name: 'Step-2-16k-Exp' },
                    // 千亿超高性价比系列
                    { id: 'step-1-8k', name: 'Step-1-8k' },
                    { id: 'step-1-32k', name: 'Step-1-32k' },
                    // 千亿超长上下文系列
                    { id: 'step-1-128k', name: 'Step-1-128k' },
                    { id: 'step-1-256k', name: 'Step-1-256k' }
                ]
            },
            {
                id: 'zhipu',
                name: 'ZhipuAI',
                selected: false,
                apiKey: '',
                selectedModel: 'glm-4',
                models: [
                    { id: 'glm-4', name: 'GLM-4' },
                    { id: 'glm-4-plus', name: 'GLM-4 Plus' },
                    { id: 'glm-4-vision', name: 'GLM-4 Vision' },
                    { id: 'glm-3-turbo', name: 'GLM-3 Turbo' },
                    { id: 'glm-z1-32b', name: 'GLM Z1 32B' }
                ]
            }
        ],

        // 结果
        results: {},

        // 轮询计时器
        pollTimer: null
    },

    computed: {
        // 获取当前语言的翻译
        t() {
            return (key) => {
                return this.translations[this.currentLang][key] || key;
            };
        },

        hasSelectedProviders() {
            return this.availableProviders.some(provider => provider.selected);
        },

        canStartAnnotation() {
            // 检查是否至少选择了一个提供商
            if (!this.hasSelectedProviders) return false;

            // 检查选中的提供商是否都有 API 密钥
            const selectedProviders = this.availableProviders.filter(provider => provider.selected);
            return selectedProviders.every(provider => provider.apiKey.trim() !== '');
        },

        selectedModels() {
            const models = [];
            this.availableProviders.forEach(provider => {
                if (provider.selected) {
                    if (provider.id === 'openrouter') {
                        // OpenRouter 使用 provider/model 格式
                        models.push(provider.selectedModel);
                    } else {
                        // 其他提供商使用模型名称
                        models.push(provider.selectedModel);
                    }
                }
            });
            return models;
        },

        apiKeys() {
            const keys = {};
            this.availableProviders.forEach(provider => {
                if (provider.selected && provider.apiKey.trim() !== '') {
                    keys[provider.id] = provider.apiKey.trim();
                }
            });
            return keys;
        }
    },

    methods: {
        // 文件上传处理
        onFileDrop(event) {
            this.isDragover = false;
            const files = event.dataTransfer.files;
            if (files.length > 0) {
                this.handleFile(files[0]);
            }
        },

        onFileChange(event) {
            const files = event.target.files;
            if (files.length > 0) {
                this.handleFile(files[0]);
            }
        },

        handleFile(file) {
            // 检查文件类型
            const validExtensions = ['.csv', '.tsv', '.xls', '.xlsx'];
            const fileExt = file.name.substring(file.name.lastIndexOf('.')).toLowerCase();

            if (!validExtensions.includes(fileExt)) {
                this.uploadError = this.t('fileTypeError').replace('{fileExt}', fileExt);
                return;
            }

            // 检查文件大小 (限制为 16MB)
            if (file.size > 16 * 1024 * 1024) {
                this.uploadError = this.t('fileSizeError');
                return;
            }

            this.isUploading = true;
            this.uploadError = '';

            const formData = new FormData();
            formData.append('file', file);

            axios.post('/api/upload', formData)
                .then(response => {
                    this.taskId = response.data.task_id;
                    this.filePath = response.data.file_path;
                    this.dataPreview = response.data.preview;
                    this.dataColumns = response.data.columns;

                    // 切换到配置页面
                    this.currentPage = 'configure';
                })
                .catch(error => {
                    console.error('Upload error:', error);
                    this.uploadError = error.response?.data?.error || this.t('uploadError');
                })
                .finally(() => {
                    this.isUploading = false;
                });
        },

        // 下载示例数据
        downloadSample() {
            window.location.href = '/api/sample';
        },

        // 开始注释
        startAnnotation() {
            if (!this.canStartAnnotation) return;

            const payload = {
                task_id: this.taskId,
                file_path: this.filePath,
                species: this.species,
                tissue: this.tissue,
                models: this.selectedModels,
                api_keys: this.apiKeys,
                consensus_threshold: this.consensusThreshold,
                max_discussion_rounds: this.maxDiscussionRounds
            };

            axios.post('/api/annotate', payload)
                .then(response => {
                    // 切换到处理页面
                    this.currentPage = 'processing';
                    this.taskStatus = '排队中';
                    this.processingError = '';

                    // 开始轮询任务状态
                    this.startPolling();
                })
                .catch(error => {
                    console.error('Annotation error:', error);
                    this.processingError = error.response?.data?.error || this.t('annotationError');
                });
        },

        // 轮询任务状态
        startPolling() {
            // 清除现有计时器
            if (this.pollTimer) {
                clearInterval(this.pollTimer);
            }

            // 设置新计时器
            this.pollTimer = setInterval(() => {
                this.checkTaskStatus();
            }, 2000); // 每 2 秒检查一次
        },

        checkTaskStatus() {
            if (!this.taskId) return;

            axios.get(`/api/tasks/${this.taskId}`)
                .then(response => {
                    const status = response.data.status;
                    this.taskStatus = this.formatStatus(status);

                    if (status === 'completed') {
                        // 任务完成，获取结果
                        this.getResults();
                        clearInterval(this.pollTimer);
                    } else if (status === 'failed') {
                        // 任务失败
                        this.processingError = response.data.error || this.t('processingError');
                        clearInterval(this.pollTimer);
                    }
                })
                .catch(error => {
                    console.error('Status check error:', error);
                    this.processingError = this.t('statusCheckError');
                    clearInterval(this.pollTimer);
                });
        },

        formatStatus(status) {
            switch (status) {
                case 'queued': return this.t('statusQueued');
                case 'processing': return this.t('statusProcessing');
                case 'completed': return this.t('statusCompleted');
                case 'failed': return this.t('statusFailed');
                default: return status;
            }
        },

        // 获取结果
        getResults() {
            axios.get(`/api/results/${this.taskId}`)
                .then(response => {
                    if (response.data.status === 'completed') {
                        this.results = response.data.results;
                        this.currentPage = 'results';
                    } else {
                        this.processingError = response.data.error || this.t('resultsNotReady');
                    }
                })
                .catch(error => {
                    console.error('Results error:', error);
                    this.processingError = this.t('resultsError');
                });
        },

        // 下载结果
        downloadResults(format) {
            if (!this.taskId) return;

            window.location.href = `/api/download/${this.taskId}/${format}`;
        },

        // 切换语言
        toggleLanguage() {
            this.currentLang = this.currentLang === 'en' ? 'zh' : 'en';

            // 更新状态文本
            if (this.taskStatus === '排队中' || this.taskStatus === 'Queued') {
                this.taskStatus = this.t('statusQueued');
            } else if (this.taskStatus === '处理中' || this.taskStatus === 'Processing') {
                this.taskStatus = this.t('statusProcessing');
            } else if (this.taskStatus === '已完成' || this.taskStatus === 'Completed') {
                this.taskStatus = this.t('statusCompleted');
            } else if (this.taskStatus === '失败' || this.taskStatus === 'Failed') {
                this.taskStatus = this.t('statusFailed');
            } else if (this.taskStatus === '准备中' || this.taskStatus === 'Preparing') {
                this.taskStatus = this.currentLang === 'en' ? 'Preparing' : '准备中';
            }
        },

        // 获取提供商图标
        getProviderIcon(providerId) {
            switch (providerId) {
                case 'openai': return 'fab fa-openai';
                case 'anthropic': return 'fas fa-comment-dots';
                case 'gemini': return 'fab fa-google';
                case 'openrouter': return 'fas fa-random';
                case 'grok': return 'fab fa-twitter';
                case 'deepseek': return 'fas fa-brain';
                case 'minimax': return 'fas fa-microchip';
                case 'qwen': return 'fab fa-alipay';
                case 'stepfun': return 'fas fa-shoe-prints';
                case 'zhipu': return 'fas fa-lightbulb';
                default: return 'fas fa-robot';
            }
        },

        // 获取提供商图标颜色类
        getProviderIconClass(providerId) {
            switch (providerId) {
                case 'openai': return 'has-text-success';
                case 'anthropic': return 'has-text-danger';
                case 'gemini': return 'has-text-info';
                case 'openrouter': return 'has-text-warning';
                case 'grok': return 'has-text-link';
                case 'deepseek': return 'has-text-primary';
                case 'minimax': return 'has-text-info';
                case 'qwen': return 'has-text-warning';
                case 'stepfun': return 'has-text-success';
                case 'zhipu': return 'has-text-danger';
                default: return 'has-text-grey';
            }
        },

        // 重置并开始新的注释
        resetAndStartNew() {
            // 重置状态
            this.taskId = null;
            this.filePath = null;
            this.dataPreview = [];
            this.dataColumns = [];
            this.results = {};
            this.uploadError = '';
            this.processingError = '';

            // 返回上传页面
            this.currentPage = 'upload';
        }
    },

    // 组件销毁时清除计时器
    beforeDestroy() {
        if (this.pollTimer) {
            clearInterval(this.pollTimer);
        }
    }
});
