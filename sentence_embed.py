from sentence_transformers import SentenceTransformer

model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

def sentence_embed(sentence):
    embedding = model.encode(sentence)
    return embedding #returns format (384,)