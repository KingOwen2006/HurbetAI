import os
import urllib.request
import re

if not os.path.exists('the-verdict.txt'):
    url = ("https://raw.githubusercontent.com/rasbt/"
            "LLMS-from-scratch/main/ch02/01_main-chapter-code/"
                "the-verdict.txt")
    file_path = 'the-verdict.txt'
    urllib.request.urlretrieve(url, file_path)

with open("the-verdict.txt", "r", encoding="utf-8") as f:
    raw_text = f.read()
    # print(raw_text)
    # print(len(raw_text)) 

# the amount of tokens in the text
results = re.split(r'([,.:;?_!"()\']|--|\s)', raw_text)
results = [item.strip() for item in results if item.strip()]

preprocessed_text = results

all_words = sorted(set(preprocessed_text))
print(all_words)
vocab_size = len(all_words)
len(all_words)

vocab = {token:integer for integer, token in enumerate(all_words)}

class simple_tokenizer:
    def __init__(self, vocab):
        self.str_to_int = vocab
        self.int_to_str = {i: s for s, i in vocab.items()}

    def encode(self, text):
        preprocessed_text = re.split(r'([,.:;?_!"()\']|--|\s)', text)

        preprocessed_text = [item.strip() for item in preprocessed_text if item.strip()]

        ids = [self.str_to_int[s] for s in preprocessed_text]
        return ids

    def decode(self, ids):
        text = "".join([self.int_to_str[i] for i in ids])

        text = re.sub(r'\s+([,.:;?_!"()\'])', r'\1', text)