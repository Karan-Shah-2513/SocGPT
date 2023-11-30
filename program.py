from gpt4all import GPT4All
model = GPT4All("orca-mini-3b-gguf2-q4_0.gguf")
output = model.generate(
    'Who most populated country in the world?', max_tokens=100)
print(output)
