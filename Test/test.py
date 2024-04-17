import json
import random

def load_json(filename):
    """Load JSON data from a file."""
    with open(filename, 'r') as file:
        data = json.load(file)
    return data

def filter_by_bias_type(data, bias_type, sample_size=100):
    """Filter data to only include items with a specific bias_type and randomly sample from them."""
    filtered_data = [item for item in data if item.get('bias_type') == bias_type]
    if len(filtered_data) < sample_size:
        print("Warning: Not enough data to sample 100 elements, sampling all available.")
        return filtered_data
    with open('inter_religion.json', 'w', encoding='utf-8') as outfile:
        json.dump(filtered_data, outfile, indent=4, ensure_ascii=False)
    print("Data written to testing.json successfully.")
    return random.sample(filtered_data, sample_size)

def main():
    # Set the random seed for reproducibility
    random_seed = 42  # You can change this value to any other integer
    random.seed(random_seed)

    # Load the data from the JSON file
    data = load_json('Intersentence_data.json')
    
    # Filter and sample data
    sampled_data = filter_by_bias_type(data, 'religion', 75)  # Specify the desired bias_type here

    # Print the length of the filtered data to verify the number of elements
    print(len(sampled_data))

    # Optionally, write the sampled data to a new JSON file
    with open('testing.json', 'w', encoding='utf-8') as outfile:
        json.dump(sampled_data, outfile, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    main()
