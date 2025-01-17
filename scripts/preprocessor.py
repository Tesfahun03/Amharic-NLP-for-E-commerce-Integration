import re
import sys
import os
sys.path.append(os.path.abspath('..'))


class RemoveUnwanted():
    """
    A class used to preprocess text data by removing unwanted elements such as special characters,
    URLs, and English words.
    Methods
    -------
    remove_special_character(messages)
        Removes emojis, URLs, and special characters from a list of messages.
    remove_english_words_from_text(text)
        Removes all English words from a given text.
    """
    def remove_special_character(messages):
        cleaned_data = []
        for message in messages:
            # Remove emojis, URLs, and special characters
            text = re.sub(r'http\S+|www\S+|https\S+', '', message)
            text = re.sub(r'[^\w\s]', '', text)
            cleaned_data.append(text)
        return cleaned_data

    def remove_english_words_from_text(text):
        # Replace all English words with an empty string
        return re.sub(r'\b[a-zA-Z]+\b', '', text)
