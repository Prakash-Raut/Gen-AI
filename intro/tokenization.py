import tiktoken

encoder = tiktoken.encoding_for_model("gpt-4o")

print("Vocab size:", encoder.n_vocab)

text = "Hello, world!"

tokens = encoder.encode(text)

print("Tokens:", tokens) # [13225, 11, 2375, 0]

my_tokens = [13225, 11, 2375, 0]

decoded = encoder.decode(tokens)

print("Decoded:", decoded)