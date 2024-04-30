import json
import os 
from collections import defaultdict, Counter

def load_data(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

def load_data(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

def classify_responses(responses):
    counter = Counter(responses.values())
    if len(counter) == 1:
        return 'Consensus'
    elif len(counter) == 2 and any(count == 1 for count in counter.values()):
        return 'Outlier'
    else:
        return 'Mix'

def analyze_responses(chatgpt_file, claude3_file, ernie_file, gemini_file):
    chatgpt_data = load_data(chatgpt_file)
    claude3_data = load_data(claude3_file)
    ernie_data = load_data(ernie_file)
    gemini_data = load_data(gemini_file)
    
    prompt_responses = defaultdict(lambda: defaultdict(str))
    for entry in chatgpt_data:
        prompt_responses[entry['prompt']]['ChatGPT'] = entry['gold_label']
    for entry in claude3_data:
        prompt_responses[entry['prompt']]['Claude3'] = entry['gold_label']
    for entry in ernie_data:
        prompt_responses[entry['prompt']]['Ernie'] = entry['gold_label']
    for entry in gemini_data:
        prompt_responses[entry['prompt']]['Gemini'] = entry['gold_label']
    
    stats = {"Consensus": 0, "Mix": 0, "Outlier": 0}
    outliers = defaultdict(list)
    mix_relationships = defaultdict(int)
    mix_examples = []
    outlier_examples = []
    
    for prompt, responses in prompt_responses.items():
        category = classify_responses(responses)
        stats[category] += 1
        if category == 'Outlier':
            response_counter = Counter(responses.values())
            for ai, response in responses.items():
                if response_counter[response] == 1:
                    outliers[ai].append(response)
            if len(outlier_examples) < 3:
                outlier_examples.append((prompt, dict(responses)))
        elif category == 'Mix':
            if len(mix_examples) < 3:
                mix_examples.append((prompt, dict(responses)))
            # Record the mix relationships
            sorted_ais = sorted(responses.keys())  # Sort to avoid duplicate pairs like A-B and B-A
            for i in range(len(sorted_ais)):
                for j in range(i + 1, len(sorted_ais)):
                    ai1, ai2 = sorted_ais[i], sorted_ais[j]
                    if responses[ai1] == responses[ai2]:
                        mix_relationships[f"{ai1}_and_{ai2}"] += 1

    results = {
        "statistics": stats,
        "outliers": {ai: {"times_as_outlier": len(responses), "detailed_responses": dict(Counter(responses))} for ai, responses in outliers.items()},
        "mix_relationships": dict(mix_relationships),
        "examples": {
            "mix": mix_examples,
            "outlier": outlier_examples
        }
    }

    with open('analysis_results.json', 'w') as f:
        json.dump(results, f, indent=4)

    print("Analysis completed. Results saved to 'analysis_results.json'.")

# Specify the paths to your JSON files
print(os.getcwd())
chatgpt_file = '../../../Test/ChatGPT/chatgpt_intra_religion_res.json'
claude3_file = '../../../Test/Claude3/claude3_intra_religion_res.json'
ernie_file = '../../../Test/Ernie/religion_answer/religion_intra_100.json'
gemini_file = '../../../Test/Gemini/gemini_intra_religion_res.json'

# Run the analysis
analyze_responses(chatgpt_file, claude3_file, ernie_file, gemini_file)
