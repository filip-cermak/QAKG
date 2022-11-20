import nltk.data
import json

def prepare_for_deepex(question_list):
    
    out = {}
    ids = create_question_ids(question_list)
    tok = nltk.data.load('tokenizers/punkt/english.pickle')

    for id, q in zip(ids, question_list):
        out = prepare_for_deepex_helper(tok, q, id, out)

    return out

def prepare_for_deepex_helper(tok, question, id, out):

    ids_with_texts = [
        ("%context", question.context_cor_resolved),
        ("%qna", question.question_with_answer_cor_resolved),
        ("%qnd-0", question.question_with_distractors_cor_resolved[0]),
        ("%qnd-1", question.question_with_distractors_cor_resolved[1]),
        ("%qnd-2", question.question_with_distractors_cor_resolved[2])
    ]

    for id_suffix, text in ids_with_texts:
        out = sentence_assigner(tok.tokenize(text), id + id_suffix, out)

    return out

def sentence_assigner(sentences, id_prefix, out):

    for i, s in enumerate(sentences):
        if s in out:
            out[s].append(id_prefix + "%" + str(i))
        else:
            out[s] = [id_prefix + "%" + str(i)]

    return out



def create_question_ids(question_list):

    ref = {}
    out = [""]*len(question_list)

    for i, q in enumerate(question_list):

        if q.id in ref:
            ref[q.id] +=1
        else:
            ref[q.id] = 0

        out[i] = q.id + "%" + str(ref[q.id])

    return out

def export_dic_to_jsonl(dic):
    d_list = []

    with open("P0.jsonl", "w") as f:
        for i, s in enumerate(list(dic.keys())):
            f.write(json.dumps({"id" : i, "title" : i, "text" : s})) # ???? title
            f.write('\n')       
