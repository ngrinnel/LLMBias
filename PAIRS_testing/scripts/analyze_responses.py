import pandas as pd
import numpy as np
from collections import Counter
from nltk.corpus import stopwords
import nltk
from gensim.utils import simple_preprocess
from gensim.parsing.preprocessing import STOPWORDS

# Set NLTK data path
nltk.data.path.append('./nltk_data')

# Load responses from CSV file
response_file = "window.csv"
df = pd.read_csv(response_file)

# Define the LLM response columns
llms = ['ChatGPT4o', 'ChatGPT4', 'Claude3 Sonnet', 'Ernie']

# Function to preprocess text using Gensim
def preprocess(text):
    return [token for token in simple_preprocess(text, deacc=True, min_len=3) if token not in STOPWORDS]

# Function to compute PMI for a specific LLM
def compute_pmi_for_llm(df, llm):
    # Filter responses by image type
    groups = {
        'black_man': df[df['Image Type'] == 'black_man'][llm],
        'black_woman': df[df['Image Type'] == 'black_woman'][llm],
        'white_man': df[df['Image Type'] == 'white_man'][llm],
        'white_woman': df[df['Image Type'] == 'white_woman'][llm]
    }
    
    # Tokenize and preprocess responses, then flatten list
    tokens = {group: [token for sublist in group_df.apply(preprocess).tolist() for token in sublist] for group, group_df in groups.items()}
    
    # Calculate word frequencies within each demographic group
    freqs = {group: Counter(group_tokens) for group, group_tokens in tokens.items()}
    total_tokens = sum(len(tokens_list) for tokens_list in tokens.values())

    # Function to calculate total word frequency across all groups
    def total_word_freq(word):
        return sum(freq[word] for freq in freqs.values())

    def compute_pmi(word, group_freq, total_group_tokens, smooth=0.01):
        freq_word_cd = group_freq.get(word, 0) + smooth  # Add smoothing
        freq_word_t = total_word_freq(word) + smooth * len(freqs)  # Adjust total frequency with smoothing
        n_cd = total_group_tokens + smooth * len(freqs)  # Adjust total group tokens
        pmi = np.log2((freq_word_cd * total_tokens) / (freq_word_t * n_cd))
        return pmi


    words = set(word for group_freq in freqs.values() for word in group_freq)
    pmi_df = pd.DataFrame(index=list(words))

    for group, group_freq in freqs.items():
        pmi_df[group] = pmi_df.index.to_series().apply(lambda word: compute_pmi(word, group_freq, len(tokens[group])))

    return pmi_df

# Compute and save PMI scores for each LLM
for llm in llms:
    pmi_df = compute_pmi_for_llm(df, llm)
    output_file = f"window_pmi_scores_{llm.replace(' ', '_').lower()}.csv"
    pmi_df.to_csv(output_file)
