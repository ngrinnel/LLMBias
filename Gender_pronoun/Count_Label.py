import json

def count_labels(json_file, output_file):
    # Load JSON data
    with open(json_file, 'r') as file:
        data = json.load(file)
    
    # Initialize counters
    stereotype_count = 0
    anti_stereotype_count = 0
    ambiguous_count = 0
    
    # Count labels
    for item in data:
        label = item.get('label', '').lower()
        if label == 'stereotype':
            stereotype_count += 1
        elif label == 'anti-stereotype':
            anti_stereotype_count += 1
        elif label == 'ambiguous':
            ambiguous_count += 1
    
    # Write results to a file
    with open(output_file, 'w') as file:
        file.write(f"Stereotype: {stereotype_count}\n")
        file.write(f"Anti-stereotype: {anti_stereotype_count}\n")
        file.write(f"Ambiguous: {ambiguous_count}\n")

# Replace 'path_to_your_file.json' and 'output.txt' with the path to your JSON file and desired output file name
count_labels('Gemini/SHE_gemini_responses.json', 'SHE_gemini_responses_output.txt')
