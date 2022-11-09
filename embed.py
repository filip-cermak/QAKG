from transformers import AutoTokenizer, AutoModel, pipeline

tokenizer = AutoTokenizer.from_pretrained("gpt2")
model = AutoModel.from_pretrained("gpt2")

tokenizer.add_special_tokens({'pad_token': '[PAD]'})
model.resize_token_embeddings(len(tokenizer))

def embed(s):
    pipe = pipeline('feature-extraction', model=model, tokenizer=tokenizer)
    
    tokens = tokenizer.tokenize(s)
    embeddings = pipe(s)

    return tokens, embeddings