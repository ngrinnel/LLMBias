import json

def load_json(filename):
    """Load JSON data from a file."""
    with open(filename, 'r') as file:
        data = json.load(file)
    return data

def count_labels(data):
    """Count the labels in the data."""
    # Initialize counters for each label
    counts = {
        "stereotype": 0,
        "anti-stereotype": 0,
        "unrelated": 0,
        "unknown": 0  # Assuming you want to count 'unknown' labels too
    }
    
    # Iterate through each item in the data and increment the appropriate counter
    for item in data:
        label = item.get("gold_label", "unknown").lower()  # Default to 'unknown' if 'gold_label' is missing
        if label in counts:
            counts[label] += 1
        else:
            # If the label is something other than the expected values, count it as 'unknown'
            counts["unknown"] += 1
    
    return counts

def main():
    # Load the data from the JSON file
    data = load_json('Ernie_Inter_100.json')
    label_counts = count_labels(data)
    
    # Print the counts
    for label, count in label_counts.items():
        print(f"{label}: {count}")
    #first_100_elements = data[:100]
    #print(len(data))

    '''with open('100_intra.json', 'w', encoding='utf-8') as outfile: #name of the output json file
        json.dump(first_100_elements, outfile, indent=4, ensure_ascii=False)'''

if __name__ == "__main__":
    main()