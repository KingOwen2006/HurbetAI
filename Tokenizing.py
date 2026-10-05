import os
from torch._tensor import Tensor
import urllib.request
import re
import tiktoken
import torch

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
# print(all_words)
vocab_size = len(all_words)
len(all_words)

vocab = {token:integer for integer, token in enumerate(all_words)}

# class simple_tokenizer:
#     def __init__(self, vocab):
#         self.str_to_int = vocab
#         self.int_to_str = {i: s for s, i in vocab.items()}

#     def encode(self, text):
#         preprocessed_text = re.split(r'([,.:;?_!"()\']|--|\s)', text)

#         preprocessed_text = [item.strip() for item in preprocessed_text if item.strip()]

#         ids = [self.str_to_int[s] for s in preprocessed_text]
#         return ids

#     def decode(self, ids):
#         text = "".join([self.int_to_str[i] for i in ids])

#         text = re.sub(r'\s+([,.:;?_!"()\'])', r'\1', text)


# tokenizer = simple_tokenizer(vocab)
# text = "Hello, world!"
# ids = tokenizer.encode(text)

# tokenizer.encode(text)

# print(ids)

all_tokens = sorted(list(set(preprocessed_text)))
all_tokens.extend(["<|endoftext|>", "<|unk|>"])

vocab = {token:integer for integer, token in enumerate(all_tokens)}

len(vocab.items())

for i, item in enumerate(list(vocab.items())[-5:]):
    print(item)

class simple_tokenizer2:
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

        tokenizer = simple_tokenizer2(vocab)

        tokenizer.encode(text)

        tokenizer.decode(tokenizer.encode(text))

tokenizer = tiktoken.get_encoding("gpt2")

tokenizer.encode("Hello, world!")

tokenizer.decode(tokenizer.encode("Hello, world!"))

text = ("Hello, world!")

tokenizer.encode(text, allowed_special={"<|endoftext|>"})

with open("the-verdict.txt", "r", encoding="utf-8") as f:
    raw_text = f.read()

enc_text = tokenizer.encode(raw_text)
print(len(enc_text))

enc_sample = enc_text[50:]

context_size = 4

x = enc_sample[:context_size]
y = enc_sample[1:context_size + 1]

print(f"x: {x}")
print(f"y: {y}")

for i in range(1, context_size+1):
    context = enc_sample[:i]
    desired = enc_sample[i]

    print(f"context: {context}")

from torch.utils.data import Dataset, DataLoader

class GPTDatasetV1(Dataset):
    def __init__(self, txt, tokenizer, max_length, stride):
        self.input_ids = []
        self.target_ids = []

        token_ids = tokenizer.encode(txt, allowed_special={"<|endoftext|>"})

        for i in range (0, len(token_ids) - max_length, stride):
            import_chunk = token_ids[i:i+max_length]
            target_chunk = token_ids[i+1:i+max_length+1]
            self.input_ids.append(import_chunk)
            self.target_ids.append(target_chunk)
        
    def __len__(self):
        return len(self.input_ids)

    def __getitem__(self, idx):
        return (
            torch.tensor(self.input_ids[idx], dtype=torch.long),
            torch.tensor(self.target_ids[idx], dtype=torch.long),
        )

def create_dataloader_V1(txt, batch_size=4, max_length=25, stride=128, shuffle=True, drop_last=True, num_workers=0):

    tokenizer = tiktoken.get_encoding("gpt2")

    dataset = GPTDatasetV1(txt, tokenizer, max_length, stride)

    dataloader = DataLoader (
        dataset,
        batch_size=batch_size,
        shuffle=shuffle,
        drop_last=drop_last,
        num_workers=num_workers
    )

    return dataloader

dataloader = create_dataloader_V1(raw_text, batch_size=4, max_length=4, stride=1, shuffle=False)

data_iter = iter(dataloader)
first_batch = next(data_iter)
print(first_batch)

second_batch = next(data_iter)
print(second_batch)

def create_dataloader_V1(txt, batch_size=8, max_length=4, stride=4, shuffle=True, drop_last=True, num_workers=0):

    tokenizer = tiktoken.get_encoding("gpt2")

    dataset = GPTDatasetV1(txt, tokenizer, max_length, stride)

    dataloader = DataLoader (
        dataset,
        batch_size=batch_size,
        shuffle=shuffle,
        drop_last=drop_last,
        num_workers=num_workers
    )

    return dataloader

dataloader = create_dataloader_V1(raw_text, batch_size=4, max_length=4, stride=1, shuffle=False)

data_iter = iter(dataloader)
first_batch = next(data_iter)
print(first_batch)

second_batch = next(data_iter)
print(second_batch)

input_ids = torch.tensor([2, 3, 4, 5])

vocab_size = 6
output_dim = 3

torch.manual_seed(123)
embedding_layer = torch.nn.Embedding(vocab_size, output_dim)

print(embedding_layer.weight)

print(embedding_layer(input_ids))

vocab_size = 50257
output_dim = 256

token_embedding_layer = torch.nn.Embedding(vocab_size, output_dim)

max_length = 4
dataloader = create_dataloader_V1(raw_text, batch_size=8, max_length=max_length, stride=max_length, shuffle=False)

dataloader_iter = iter(dataloader)
inputs, targets = next(dataloader_iter)

token_embeddings = token_embedding_layer(inputs)
print(token_embeddings.shape)

context_length = max_length
pos_embedding_layer = torch.nn.Embedding(context_length, output_dim)

pos_embeddings = pos_embedding_layer(torch.arange(max_length))
print(pos_embedding_layer.weight)

inputs = torch.tensor([
    [0.43, 0.15, 0.89],  # your
    [0.55, 0.87, 0.66],  # journey
    [0.57, 0.85, 0.64],  # starts
    [0.22, 0.58, 0.33],  # with
    [0.77, 0.25, 0.10],  # one
    [0.05, 0.80, 0.55],  # step
])

input_query = inputs[1]

input_1 = inputs[0]

print(torch.dot(input_query, input_1))

for ele in inputs[0]:
    print(ele)

# res = 0

i = 3
res = torch.dot(inputs[i], input_query)

for idx, element in enumerate(inputs[0]):
    res += element * input_query[idx]

print(res)

query = inputs[1]

attn_scores = torch.empty(inputs.shape[0])
for i, x_i in enumerate(inputs):
    attn_scores[i] = torch.dot(x_i, query)

print(attn_scores)

attn_weights_2_tmp = attn_scores / attn_scores.sum()

def softmax_native(x):
    return torch.exp(x) / torch.exp(x).sum(dim=0)

softmax_native(attn_scores)

torch.softmax(attn_scores, dim=0)