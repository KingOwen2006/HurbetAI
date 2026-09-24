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
    print(raw_text)
    print(len(raw_text)) 

# the amount of tokens in the text
results = re.split(r'([,.:;?_!"()\']|--|\s)', raw_text)
results = [item.strip() for item in results if item.strip()]

preprocessed_text = results

print(len(preprocessed_text))