class MultilingualCharTokenizer:
    def __init__(self):
        self.char_to_id = {}
        self.id_to_char = {}
        self.next_id = 1

    def encode(self, text: str) -> list[int]:
        tokens = []
        for char in text:
            if char not in self.char_to_id:
                self.char_to_id[char] = self.next_id
                self.id_to_char[self.next_id] = char
                self.next_id += 1
            tokens.append(self.char_to_id[char])
        return tokens

    def decode(self, tokens: list[int]) -> str:
        chars = []
        for token in tokens:
            chars.append(self.id_to_char.get(token, "�"))  # Unknown character fallback
        return ''.join(chars)


if __name__ == "__main__":
    tokenizer = MultilingualCharTokenizer()

    text = "Hello Brother!"
    tokens = tokenizer.encode(text)
    print("Tokens:", tokens)

    decoded = tokenizer.decode(tokens)
    print("Decoded:", decoded)
