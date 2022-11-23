from transformers import AutoTokenizer, AutoModel, pipeline
from tqdm import tqdm

tokenizer = AutoTokenizer.from_pretrained("gpt2")
model = AutoModel.from_pretrained("gpt2")

tokenizer.add_special_tokens({'pad_token': '[PAD]'})
model.resize_token_embeddings(len(tokenizer))

def embed(s):
    pipe = pipeline('feature-extraction', model=model, tokenizer=tokenizer)
    
    tokens = tokenizer.tokenize(s)
    embeddings = pipe(s)

    chr_spans_with_embeddings = {}

    for i, e in enumerate(embeddings[0]):
        start = tokenizer(s).token_to_chars(i).start
        end = tokenizer(s).token_to_chars(i).end
        chr_spans_with_embeddings[(start, end)] = e

    return chr_spans_with_embeddings

def chr_spn_matcher(ref_chr_spn, list_of_chr_spns):
    # returns all char_span-s from the list that match
    # the reference char_span
    # char span is just a length 2 tuple

    matching_chr_spns = [x for x in list_of_chr_spns if contains_chr_spn(ref_chr_spn, x)]
    return matching_chr_spns

def contains_chr_spn(ref_chr_spn, test_chr_spn):

    if (test_chr_spn[0] >= ref_chr_spn[0]) and (test_chr_spn[1] <= ref_chr_spn[1]):
        return True

    if (test_chr_spn[0]+1 >= ref_chr_spn[0]) and (test_chr_spn[1] <= ref_chr_spn[1]):
        return True

    return False

def add_embeddings_to_question_helper(q):

    #context
    chr_spans_with_embeddings = embed(q.context_cor_resolved)
    enrich_triples(q.context_triples, chr_spans_with_embeddings)

    #q+a
    chr_spans_with_embeddings = embed(q.context_cor_resolved)
    enrich_triples(q.question_with_answer_triples, chr_spans_with_embeddings)

    #q+d - 0/1/2
    for i in range(3):
        chr_spans_with_embeddings = embed(q.question_with_distractors_cor_resolved[i])
        enrich_triples(q.question_with_distractors_triples[i], chr_spans_with_embeddings)

def add_embeddings_to_questions(q_list):
    for q in tqdm(q_list):
        add_embeddings_to_question_helper(q)

def enrich_triples(triples, chr_spans_with_embeddings):
    for t in triples:
        for chr_spn in t.subject_words:
            t.subject_embeds.append([chr_spans_with_embeddings[k] for k in chr_spn_matcher(chr_spn, list(chr_spans_with_embeddings.keys()))])

        for chr_spn in t.relation_words:
            t.relation_embeds.append([chr_spans_with_embeddings[k] for k in chr_spn_matcher(chr_spn, list(chr_spans_with_embeddings.keys()))])

        for chr_spn in t.object_words:
            t.object_embeds.append([chr_spans_with_embeddings[k] for k in chr_spn_matcher(chr_spn, list(chr_spans_with_embeddings.keys()))])

