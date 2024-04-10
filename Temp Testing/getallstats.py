import os
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
    input_dir = './'  # Directory containing JSON files
    output_dir = './output_stats/'  # Directory to store output stats files
    
    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Process each JSON file in the input directory
    for filename in os.listdir(input_dir):
        if filename.endswith('.json'):
            # Load JSON data from file
            data = load_json(os.path.join(input_dir, filename))
            
            # Compute label counts
            label_counts = count_labels(data)
            
            # Create a DataFrame from the label counts
            df = pd.DataFrame(list(label_counts.items()), columns=['Label', 'Count'])
            
            # Write DataFrame to Excel file
            output_filename = os.path.splitext(filename)[0] + '_stats.xlsx'
            df.to_excel(os.path.join(output_dir, output_filename), index=False)

if __name__ == "__main__":
    main()