import pandas as pd
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
    
    # Create a DataFrame from the label counts
    df = pd.DataFrame(list(label_counts.items()), columns=['Label', 'Count'])
    
    # Write DataFrame to Excel file
    df.to_excel('label_counts.xlsx', index=False)

if __name__ == "__main__":
    main()