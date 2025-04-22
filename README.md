# mLLMCelltype Web

A web interface for the [mLLMCelltype](https://github.com/cafferychen777/mLLMCelltype) package, enabling easy cell type annotation using multiple large language models.

[![Paper](https://img.shields.io/badge/bioRxiv-10.1101%2F2025.04.10.647852-blue)](https://www.biorxiv.org/content/10.1101/2025.04.10.647852v1)
[![GitHub](https://img.shields.io/github/stars/cafferychen777/mLLMCelltype?style=social)](https://github.com/cafferychen777/mLLMCelltype)
[![Docker](https://img.shields.io/docker/pulls/cafferyyang777/mllmcelltype-web)](https://hub.docker.com/r/cafferyyang777/mllmcelltype-web)

## Overview

mLLMCelltype Web provides a user-friendly interface for annotating cell types in single-cell RNA sequencing data using multiple large language models. It supports various LLM providers including OpenAI, Anthropic, Google (Gemini), X.AI (Grok), and OpenRouter.

## Features

- **Simple File Upload**: Support for CSV, TSV, and Excel formats
- **Multiple LLM Providers**: Use models from OpenAI, Anthropic, Google, X.AI, and more
- **Consensus Annotation**: Combine results from multiple models for higher accuracy
- **Interactive Discussion**: Models can discuss and refine annotations
- **Easy Result Download**: Export results in various formats
- **Local Deployment**: Run entirely on your local machine for data privacy

## Deployment Options

### Docker (Recommended)

The easiest way to run mLLMCelltype Web is using Docker:

```bash
# Pull the Docker image
docker pull cafferyyang777/mllmcelltype-web:latest

# Run the container
docker run -d --name mllmcelltype-web \
  -p 8080:8080 \
  -e OPENAI_API_KEY="your_openai_api_key" \
  -e ANTHROPIC_API_KEY="your_anthropic_api_key" \
  -e GEMINI_API_KEY="your_gemini_api_key" \
  -v "$(pwd)/data/uploads:/app/uploads" \
  -v "$(pwd)/data/results:/app/results" \
  -v "$(pwd)/data/logs:/app/logs" \
  cafferyyang777/mllmcelltype-web:latest
```

Visit http://localhost:8080 in your browser to access the application.

### Manual Setup

For those who prefer to run the application directly:

1. Clone this repository:
   ```bash
   git clone https://github.com/cafferychen777/mllmcelltype-web.git
   cd mllmcelltype-web
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   pip install git+https://github.com/cafferychen777/mLLMCelltype.git
   ```

3. Run the application:
   ```bash
   python app.py
   ```

## Usage Guide

1. **Upload Data**: Upload a CSV, TSV, or Excel file containing cluster IDs and marker genes
2. **Select Models**: Choose one or more LLM models for annotation
3. **Set Parameters**: Configure species, tissue, consensus threshold, and discussion rounds
4. **Start Annotation**: Click the "Start Annotation" button
5. **View Results**: Examine the annotation results and download in your preferred format

## Supported Models

| Provider | Models |
|----------|--------|
| OpenAI | GPT-4o, GPT-4-turbo, GPT-4, GPT-3.5-turbo |
| Anthropic | Claude 3 Opus, Claude 3 Sonnet, Claude 3 Haiku |
| Google | Gemini 1.5 Pro, Gemini 1.5 Flash, Gemini 1.0 Pro |
| X.AI | Grok-3 |
| OpenRouter | Various models from different providers |
| Others | MiniMax, Qwen, Zhipu, StepFun |

## API Keys

You'll need API keys from at least one of the supported LLM providers:

- [OpenAI](https://platform.openai.com/account/api-keys)
- [Anthropic](https://console.anthropic.com/account/keys)
- [Google AI Studio](https://ai.google.dev/)
- [X.AI](https://x.ai/)
- [OpenRouter](https://openrouter.ai/)

## Configuration

The application supports various environment variables for configuration:

| Variable | Description | Required |
|----------|-------------|----------|
| OPENAI_API_KEY | OpenAI API key | At least one API key required |
| ANTHROPIC_API_KEY | Anthropic API key | At least one API key required |
| GEMINI_API_KEY | Google Gemini API key | At least one API key required |
| GROK_API_KEY | X.AI Grok API key | Optional |
| OPENROUTER_API_KEY | OpenRouter API key | Optional |

## Data Privacy

- All data is processed locally on your machine
- API keys are only used to communicate with LLM providers and are not stored permanently
- Uploaded files and results are saved in local directories

## Troubleshooting

If you encounter issues:

1. Check that Docker is properly installed and running
2. Ensure you've provided at least one valid API key
3. Check for port conflicts (default port is 8080)
4. View logs with `docker logs mllmcelltype-web`

## Citation

If you use mLLMCelltype in your research, please cite:

```bibtex
@article{Yang2025.04.10.647852,
  author = {Yang, Chen and Zhang, Xianyang and Chen, Jun},
  title = {Large Language Model Consensus Substantially Improves the Cell Type Annotation Accuracy for scRNA-seq Data},
  elocation-id = {2025.04.10.647852},
  year = {2025},
  doi = {10.1101/2025.04.10.647852},
  publisher = {Cold Spring Harbor Laboratory},
  URL = {https://www.biorxiv.org/content/early/2025/04/17/2025.04.10.647852},
  journal = {bioRxiv}
}
```

You can also cite this in plain text format:

Yang, C., Zhang, X., & Chen, J. (2025). Large Language Model Consensus Substantially Improves the Cell Type Annotation Accuracy for scRNA-seq Data. *bioRxiv*. https://doi.org/10.1101/2025.04.10.647852

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Contact

For questions or support, please open an issue on GitHub or contact [cafferychen777@tamu.edu](mailto:cafferychen777@tamu.edu).
