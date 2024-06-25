import re
import aiohttp
import yaml

async def analyze_textbook_content(textbook_content: str):
    lesson_plan = {
        "Objectives": extract_objectives(textbook_content),
        "Key Points": extract_key_points(textbook_content),
        "Summary": await extract_summary(textbook_content)
    }
    return lesson_plan

def extract_objectives(content):
    return re.findall(r'Objective:\s*(.+)', content)

def extract_key_points(content):
    return re.findall(r'Key Point:\s*(.+)', content)

async def extract_summary(content):
    config = load_config()
    return await get_summary_from_llama(content, config)

def load_config():
    with open('flows/textbook_synthesizer_flow.yaml', 'r') as file:
        return yaml.safe_load(file)

async def get_summary_from_llama(content, config):
    model = config['default_model']['model']
    api_base = config['default_model']['api_base']
    api_token = config['default_model']['auth_token']
    headers = {
        'Authorization': f'Bearer {api_token}',
        'Content-Type': 'application/json'
    }
    data = {
        'model': model,
        'content': content,
        'parameters': {
            'summary_length': 'short'
        }
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(f'{api_base}/v1/models/{model}/summarize', headers=headers, json=data) as response:
            if response.status == 200:
                response_data = await response.json()
                return response_data.get('summary', 'Summary could not be retrieved.')
            else:
                return 'Error: Unable to retrieve summary.'
