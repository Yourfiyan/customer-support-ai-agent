import requests
import json
import os

# Load credentials
kaggle_json_path = os.path.expanduser('~/.kaggle/kaggle.json')
with open(kaggle_json_path) as f:
    creds = json.load(f)

username = creds['username']
key = creds['key']

# Create minimal notebook for testing
minimal_notebook = {
    "cells": [
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": ["# Customer Support AI Agent System\n", "\n", "**Kaggle Agents Intensive - Capstone Project**\n", "\n", "Multi-agent customer support system using Google Gemini AI.\n", "\n", "## System Overview\n", "\n", "- **4 Specialized Agents**: Classifier → Researcher → Writer → Validator\n", "- **Custom Tools**: FAQ search and email logging\n", "- **Quality Validation**: Automated response checking\n", "- **Production-Ready**: FastAPI server + web demo\n", "\n", "**GitHub**: https://github.com/Yourfiyan/customer-support-ai-agent"]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": ["# Install dependencies\n", "!pip install -q google-generativeai"]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": ["import google.generativeai as genai\n", "import json\n", "from datetime import datetime\n", "\n", "# Configure API\n", "GOOGLE_API_KEY = 'your-api-key-here'\n", "genai.configure(api_key=GOOGLE_API_KEY)\n", "\n", "print('✅ Setup complete!')"]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": ["## Architecture\n", "\n", "```\n", "Customer Question\n", "    ↓\n", "Classifier Agent (categorize)\n", "    ↓\n", "Research Agent (search FAQs)\n", "    ↓\n", "Writer Agent (craft response)\n", "    ↓\n", "Validator Agent (quality check)\n", "    ↓\n", "Send Response\n", "```\n", "\n", "**Full implementation**: https://github.com/Yourfiyan/customer-support-ai-agent"]
        }
    ],
    "metadata": {
        "kernelspec": {
            "display_name": "Python 3",
            "language": "python",
            "name": "python3"
        },
        "language_info": {
            "name": "python",
            "version": "3.12.0"
        }
    },
    "nbformat": 4,
    "nbformat_minor": 5
}

# Convert to string
notebook_str = json.dumps(minimal_notebook)

# Prepare payload
payload = {
    'id': f'{username}/customer-support-ai-agent',
    'slug': 'customer-support-ai-agent',
    'newTitle': 'Customer Support AI Agent - Multi-Agent System',
    'text': notebook_str,
    'language': 'python',
    'kernelType': 'notebook',
    'isPrivate': False,
    'enableGpu': False,
    'enableInternet': True,
    'categoryIds': [],
    'datasetDataSources': [],
    'competitionDataSources': [],
    'kernelDataSources': []
}

# Push to Kaggle
url = 'https://www.kaggle.com/api/v1/kernels/push'
response = requests.post(url, json=payload, auth=(username, key))

print(f'Status: {response.status_code}')
result = response.json()
print(f'Response: {json.dumps(result, indent=2)}')

if response.status_code == 200 and not result.get('hasError'):
    ref = result.get('ref', f"{username}/customer-support-ai-agent")
    print(f'\n✅ Success! View at: https://www.kaggle.com/code/{ref}')
else:
    print(f'\n❌ Error: {result.get("error", "Upload failed")}')
