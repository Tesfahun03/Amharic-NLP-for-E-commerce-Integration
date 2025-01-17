import re

def tokenize_amharic(text):
    # Split by spaces and handle punctuation
    tokens = re.findall(r'\b\w+\b', text, re.UNICODE)
    return tokens
