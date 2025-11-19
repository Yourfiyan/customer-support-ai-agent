import requests
import json
import os
import base64

# Load Kaggle credentials
kaggle_json_path = os.path.expanduser('~/.kaggle/kaggle.json')
with open(kaggle_json_path) as f:
    creds = json.load(f)

username = creds['username']
key = creds['key']

# Read notebook content
with open('kaggle_submission/kaggle_notebook.ipynb', 'r', encoding='utf-8') as f:
    notebook_content = f.read()

# Prepare the kernel push payload
kernel_metadata = {
    'id': f'{username}/customer-support-ai-agent-system',
    'slug': 'customer-support-ai-agent-system', 
    'newTitle': 'Customer Support AI Agent System',
    'text': notebook_content,
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

# Make API request
url = 'https://www.kaggle.com/api/v1/kernels/push'
response = requests.post(
    url,
    json=kernel_metadata,
    auth=(username, key),
    headers={'Content-Type': 'application/json'}
)

print(f'Status Code: {response.status_code}')
print(f'Response: {response.text}')

if response.status_code == 200:
    result = response.json()
    if not result.get('hasError', True):
        print(f\"\\n Success! Kernel URL: https://www.kaggle.com/code/{result.get('ref', kernel_metadata['id'])}\")
    else:
        print(f\"\\n Error: {result.get('error', 'Unknown error')}\")
else:
    print(f'\\n HTTP Error: {response.status_code}')
