import re
import os
import sys
import pandas as pd

sys.path.append(os.path.abspath('..'))


def data_labeler():
    """Labels tokens in a text file with predefined categories and saves the labeled data to a CSV file.
    The function reads tokens from a text file, labels them based on predefined categories (Product, PRICE, LOC),
    and saves the labeled tokens to a CSV file.
    The predefined categories and their corresponding keywords are:
        - Product: ['የፀጉር', 'እስቲመር', 'ጭን', 'ትሪትመንት', 'ጸጉር', 'ፖፖ', 'የልጆች', 'ምግብ', 'መፍጫ', 'ቦል']
        - PRICE: ['ብር', '800', 'ዋጋ', '1200', '400', '4500', '1000']
        - LOC: ['ቁ1መገናኛ', 'ፒያሳ', 'ገርጂ', '4ኪሎ', 'ቅድስት', 'ስላሴ', 'ህንፃ', 'ኢምፔሪያል', 'ከሳሚ', 'ጊዮርጊስ', 'አደባባይ', 'ራመት_ታቦር_ኦዳ_ህንፃ']
        None
    """
    # Load data from the text file
    with open('../data/tokens.txt', 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # Define keywords for each category
    entities = {
        "Product": ['የፀጉር', 'እስቲመር', 'ጭን', 'ትሪትመንት', 'ጸጉር', 'ፖፖ', 'የልጆች' 'ምግብ' 'መፍጫ', 'ቦል'],
        "PRICE": ['ብር', '800', 'ዋጋ', '1200', '400', '4500', '1000'],
        "LOC": ['ቁ1መገናኛ', 'ፒያሳ', 'ገርጂ', '4ኪሎ', 'ቅድስት', 'ስላሴ', 'ህንፃ', 'ኢምፔሪያል', 'ከሳሚ' 'ጊዮርጊስ', 'አደባባይ', 'ራመት_ታቦር_ኦዳ_ህንፃ']
    }

    # Function to label tokens

    def label_tokens(tokens, entities):
        labeled = []
        for token in tokens:
            label = "O"  # Default label
            for entity, keywords in entities.items():
                if token in keywords:
                    label = f"B-{entity}" if label == "O" else f"I-{entity}"
            labeled.append((token, label))
        return labeled

    # Process each line in the file
    labeled_data = []
    for line in lines:
        tokens = re.findall(r"[\w\d]+", line)  # Tokenize using regex
        labeled_data.extend(label_tokens(tokens, entities))

    # Convert labeled data to a DataFrame
    df = pd.DataFrame(labeled_data, columns=["Token", "Label"])

    # Save labeled data to a CSV file
    output_file = "../data/labeled_ner_data.csv"
    df.to_csv(output_file, index=False, encoding='utf-8')

    print(f"Labeled data has been saved to {output_file}.")
