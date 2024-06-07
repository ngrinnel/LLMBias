import requests
import json
import os
import google.generativeai as genai
import time

# Configuration for API keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
CLAUDE_API_KEY = os.getenv("CLAUDE_API_KEY")
if not CLAUDE_API_KEY or not OPENAI_API_KEY:
    raise ValueError("API keys for OpenAI or CLAUDE are not set.")

# API Endpoints
OPENAI_API_ENDPOINT = "https://api.openai.com/v1/chat/completions"
CLAUDE_API_ENDPOINT = "https://api.anthropic.com/v1/messages"

# Function to load JSON data from file
def load_json(filename):
    with open(filename, 'r') as file:
        data = json.load(file)
    return data

# Function to generate prompts from the data
def generate_prompts(data):
    prompts_with_refs = []
    for item in data:
        context = item['context']
        prompt_text = f"{context}\n"
        prompts_with_refs.append({'prompt': prompt_text.strip()})
    return prompts_with_refs

# Function to send message using OpenAI's API
def send_message_openai(prompt):
    headers = {
        'Authorization': f'Bearer {OPENAI_API_KEY}',
        'Content-Type': 'application/json',
    }
    payload = json.dumps({
        "model": "gpt-4",
        "messages": [{"role": "user", "content": prompt}]
    })
    response = requests.post(OPENAI_API_ENDPOINT, headers=headers, data=payload)
    return response.json() if response.status_code == 200 else None

# Function to send message using Claude's API
def send_message_claude(prompt):
    headers = {
        "x-api-key": CLAUDE_API_KEY,
        "Content-Type": "application/json",
        "anthropic-version": "2023-06-01"
    }
    data = {
        "model": "claude-3-opus-20240229",
        "max_tokens": 2000,
        "messages": [{"role": "user", "content": prompt}]
    }
    response = requests.post(CLAUDE_API_ENDPOINT, headers=headers, json=data)
    return response.json()['content'][0].get('text', '') if response.status_code == 200 else None

# Function to send message using Gemini's API
def send_message_gemini(prompt, model):
    try:
        time.sleep(2)  # Manage rate limits
        response = model.generate_content(prompt)
        return response.text if response and hasattr(response, 'text') else None
    except Exception as e:
        print(f"Error with Gemini API: {e}")
        return None

# Main function to load data, generate prompts, and send messages
def main():
    data = load_json('HE_90_prompts.json')
    prompts_with_refs = generate_prompts(data)

    openai_responses, claude_responses, gemini_responses = [], [], []

    # Configure the Gemini model
    generation_config = {
        "temperature": 0,
        "top_p": 1,
        "top_k": 1,
        "max_output_tokens": 400
    }
    safety_settings = [
        {"category": "HARM_CATEGORY_DANGEROUS", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
    ]
    gemini_model = genai.GenerativeModel('gemini-pro', generation_config=generation_config, safety_settings=safety_settings)

    for prompt_ref in prompts_with_refs:
        conversation = prompt_ref['prompt']

        # Process with OpenAI
        response = send_message_openai(conversation)
        if response and 'choices' in response and len(response['choices']) > 0:
            chosen_response_text = response['choices'][0]['message']['content'].strip()
            openai_responses.append({'prompt': conversation, 'response': chosen_response_text})

        # Process with Claude
        generated_response = send_message_claude(conversation)
        if generated_response:
            claude_responses.append({'prompt': conversation, 'response': generated_response})

        # Process with Gemini
        gemini_response = send_message_gemini(conversation, gemini_model)
        if gemini_response:
            gemini_responses.append({'prompt': conversation, 'response': gemini_response})

    # Saving results
    with open('HE_openai_responses.json', 'w', encoding='utf-8') as outfile:
        json.dump(openai_responses, outfile, indent=4, ensure_ascii=False)
    with open('HE_claude_responses.json', 'w', encoding='utf-8') as outfile:
        json.dump(claude_responses, outfile, indent=4, ensure_ascii=False)
    with open('HE_gemini_responses.json', 'w', encoding='utf-8') as outfile:
        json.dump(gemini_responses, outfile, indent=4, ensure_ascii=False)

if __name__ == '__main__':
    main()
