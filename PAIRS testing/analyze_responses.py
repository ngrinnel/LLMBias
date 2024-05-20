import pandas as pd
from collections import Counter
from nltk.corpus import stopwords
from gensim.utils import simple_preprocess
from gensim.parsing.preprocessing import STOPWORDS
import numpy as np
import nltk

# Set NLTK data path
nltk.data.path.append('./nltk_data')

# Load responses from CSV file
response_file = "PAIRS.csv"
df = pd.read_csv(response_file)

# Define the LLM response columns
llms = ['ChatGPT4o', 'ChatGPT4', 'Claude3 Sonnet', 'Ernie']

# Function to preprocess text using Gensim
def preprocess(text):
    return [token for token in simple_preprocess(text) if token not in STOPWORDS and len(token) > 2]

# Function to compute PMI for a specific LLM
def compute_pmi_for_llm(df, llm):
    # Filter responses by image type
    black_men_responses = df[df['Image Type'] == 'black_man'][llm]
    black_women_responses = df[df['Image Type'] == 'black_woman'][llm]
    white_men_responses = df[df['Image Type'] == 'white_man'][llm]
    white_women_responses = df[df['Image Type'] == 'white_woman'][llm]

    # Tokenize and preprocess responses
    black_men_tokens = black_men_responses.apply(lambda x: preprocess(x)).explode()
    black_women_tokens = black_women_responses.apply(lambda x: preprocess(x)).explode()
    white_men_tokens = white_men_responses.apply(lambda x: preprocess(x)).explode()
    white_women_tokens = white_women_responses.apply(lambda x: preprocess(x)).explode()

    # Get word frequencies
    black_men_freq = Counter(black_men_tokens)
    black_women_freq = Counter(black_women_tokens)
    white_men_freq = Counter(white_men_tokens)
    white_women_freq = Counter(white_women_tokens)

    # Compute total tokens in each group
    total_black_men_tokens = len(black_men_tokens)
    total_black_women_tokens = len(black_women_tokens)
    total_white_men_tokens = len(white_men_tokens)
    total_white_women_tokens = len(white_women_tokens)
    total_all_tokens = total_black_men_tokens + total_black_women_tokens + total_white_men_tokens + total_white_women_tokens

    # Total word frequency across all groups
    def total_word_freq(word, freq_by_demo):
        return sum(freq_by_demo[demo][word] for demo in freq_by_demo)

    def compute_pmi(word, group_freq, total_group_tokens, total_all_tokens):
        freq_word_cd = group_freq[word]
        n_cd = total_group_tokens
        freq_word_t = total_word_freq(word, {'black_man': black_men_freq, 'black_woman': black_women_freq, 'white_man': white_men_freq, 'white_woman': white_women_freq})
        if freq_word_t == 0 or n_cd == 0:
            return -np.inf  # or handle zero probability in another way
        else:
            pmi = np.log2((freq_word_cd * total_all_tokens) / (freq_word_t * n_cd))
            return pmi

    # Compute PMI for each word and demographic group
    words = list(set(black_men_freq.keys()).union(black_women_freq.keys()).union(white_men_freq.keys()).union(white_women_freq.keys()))
    pmi_df = pd.DataFrame(index=words)

    for group, group_freq, total_group_tokens in [
        ('black_man', black_men_freq, total_black_men_tokens),
        ('black_woman', black_women_freq, total_black_women_tokens),
        ('white_man', white_men_freq, total_white_men_tokens),
        ('white_woman', white_women_freq, total_white_women_tokens)]:
        pmi_df[group] = pmi_df.index.to_series().apply(lambda word: compute_pmi(word, group_freq, total_group_tokens, total_all_tokens))

    return pmi_df

# Compute and save PMI scores for each LLM
for llm in llms:
    pmi_df = compute_pmi_for_llm(df, llm)
    output_file = f"pmi_scores_{llm.replace(' ', '_').lower()}.csv"
    pmi_df.to_csv(output_file)
