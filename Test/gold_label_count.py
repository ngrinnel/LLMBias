import json

def compare_llms(llm1_files, llm2_files):
    total_same = 0
    stereotype_count = 0
    anti_stereotype_count = 0
    unrelated_count = 0
    unknown_count = 0

    for file1, file2 in zip(llm1_files, llm2_files):
        with open(file1, 'r') as f1, open(file2, 'r') as f2:
            data1 = json.load(f1)
            data2 = json.load(f2)

            if len(data1) != len(data2):
                print(f"Files {file1} and {file2} have different number of entries.")
                continue

            for i in range(len(data1)):
                if data1[i]['gold_label'] == data2[i]['gold_label']:
                    total_same += 1
                    label = data1[i]['gold_label']
                    if label == "stereotype":
                        stereotype_count += 1
                    elif label == "anti-stereotype":
                        anti_stereotype_count += 1
                    elif label == "unrelated":
                        unrelated_count += 1
                    elif label == "Unknown":
                        unknown_count += 1

    return total_same, stereotype_count, anti_stereotype_count, unrelated_count, unknown_count

# Define file paths
file_paths = {
    "Ernie": ["Ernie/ernie_inter_profession_res.json", "Ernie/ernie_intra_profession_res.json"],
    "ChatGPT": ["ChatGPT/chatgpt_inter_profession_res.json", "ChatGPT/chatgpt_intra_profession_res.json"],
    "Claude3": ["Claude3/claude3_inter_profession_res.json", "Claude3/claude3_intra_profession_res.json"],
    "Gemini": ["Gemini/gemini_inter_profession_res.json", "Gemini/gemini_intra_profession_res.json"]
}

# Dictionary to store individual results
individual_results = {}

# Total prompts
total_prompts = 200

# Open a file for writing
with open("profession_llm_comparison.txt", "w") as outfile:
    # Compare each pair of LLMs
        # Compare each pair of LLMs
    for idx, (llm1, llm1_files) in enumerate(file_paths.items()):
        for llm2, llm2_files in list(file_paths.items())[idx + 1:]:
            outfile.write(f"Comparing {llm1} and {llm2}:\n")
            total_same_inter, stereotype_inter, anti_stereotype_inter, unrelated_inter, unknown_inter = compare_llms(llm1_files[:1], llm2_files[:1])
            total_same_intra, stereotype_intra, anti_stereotype_intra, unrelated_intra, unknown_intra = compare_llms(llm1_files[1:], llm2_files[1:])
            individual_results[(llm1, llm2)] = {
                "inter": {
                    "total_same": total_same_inter,
                    "stereotype": stereotype_inter,
                    "anti_stereotype": anti_stereotype_inter,
                    "unrelated": unrelated_inter,
                    "unknown": unknown_inter
                },
                "intra": {
                    "total_same": total_same_intra,
                    "stereotype": stereotype_intra,
                    "anti_stereotype": anti_stereotype_intra,
                    "unrelated": unrelated_intra,
                    "unknown": unknown_intra
                }
            }
            outfile.write(f"Individual results for 'inter' files:\n")
            outfile.write(f"Total times they answered the same (inter): {total_same_inter}\n")
            outfile.write(f"Stereotype label percentage (inter): {stereotype_inter / total_same_inter * 100:.2f}%\n")
            outfile.write(f"Anti-stereotype label percentage (inter): {anti_stereotype_inter / total_same_inter * 100:.2f}%\n")
            outfile.write(f"Unrelated label percentage (inter): {unrelated_inter / total_same_inter * 100:.2f}%\n")
            outfile.write(f"Unknown label percentage (inter): {unknown_inter / total_same_inter * 100:.2f}%\n")
            outfile.write("\n")
            outfile.write(f"Individual results for 'intra' files:\n")
            outfile.write(f"Total times they answered the same (intra): {total_same_intra}\n")
            outfile.write(f"Stereotype label percentage (intra): {stereotype_intra / total_same_intra * 100:.2f}%\n")
            outfile.write(f"Anti-stereotype label percentage (intra): {anti_stereotype_intra / total_same_intra * 100:.2f}%\n")
            outfile.write(f"Unrelated label percentage (intra): {unrelated_intra / total_same_intra * 100:.2f}%\n")
            outfile.write(f"Unknown label percentage (intra): {unknown_intra / total_same_intra * 100:.2f}%\n")
            outfile.write("\n")

    # Print total results
    outfile.write("Total results:\n")
    for pair, results in individual_results.items():
        total_same_inter = results["inter"]["total_same"]
        total_same_intra = results["intra"]["total_same"]
        total_prompts_inter = 100  # Each 'inter' file contains 100 prompts
        total_prompts_intra = 100  # Each 'intra' file contains 100 prompts
        stereotype_total = results["inter"]["stereotype"] + results["intra"]["stereotype"]
        anti_stereotype_total = results["inter"]["anti_stereotype"] + results["intra"]["anti_stereotype"]
        unrelated_total = results["inter"]["unrelated"] + results["intra"]["unrelated"]
        unknown_total = results["inter"]["unknown"] + results["intra"]["unknown"]
        outfile.write(f"{pair[0]} vs {pair[1]}:\n")
        outfile.write(f"Total times they answered the same: {total_same_inter + total_same_intra} ({(total_same_inter + total_same_intra) / (total_prompts_inter + total_prompts_intra) * 100:.2f}%)\n")
        outfile.write(f"Stereotype label percentage: {stereotype_total / (total_same_inter + total_same_intra) * 100:.2f}%\n")
        outfile.write(f"Anti-stereotype label percentage: {anti_stereotype_total / (total_same_inter + total_same_intra) * 100:.2f}%\n")
        outfile.write(f"Unrelated label percentage: {unrelated_total / (total_same_inter + total_same_intra) * 100:.2f}%\n")
        outfile.write(f"Unknown label percentage: {unknown_total / (total_same_inter + total_same_intra) * 100:.2f}%\n")
        outfile.write("\n")

