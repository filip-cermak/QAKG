import data_model

import nltk.data
import json
import ast

"""
Example usage:

import pickle
import data_model

with open('output/question_list_filtered_coref_resolved_2022-10-22 17:20:53.876724_0.pkl', 'rb') as f:
    q_list = pickle.load(f)


import deepex

out = deepex.prepare_for_deepex(q_list)
deepex.export_dic_to_jsonl(out, True)

"""
def prepare_for_deepex(question_list):
    
    out = {}
    ids = list(create_question_ids(question_list).keys())
    tok = nltk.data.load('tokenizers/punkt/english.pickle')

    for id, q in zip(ids, question_list):
        out = prepare_for_deepex_helper(tok, q, id, out)

    sentences_with_ids = out

    return sentences_with_ids #format {sentence : [id1,id2...], ...}

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
    out = {}

    for i, q in enumerate(question_list):

        if q.id in ref:
            ref[q.id] +=1
        else:
            ref[q.id] = 0

        out[q.id + "%" + str(ref[q.id])] = q

    ids_with_questions = out
    
    return ids_with_questions

def export_dic_to_jsonl(dic, partition = False, partition_length = 1000):
    d_list = []

    if not partition:
        with open("P0.jsonl", "w") as f:
            for i, s in enumerate(list(dic.keys())):
                f.write(json.dumps({"id" : str(dic[s]), "title" : str(dic[s]), "text" : s})) # ???? title
                f.write('\n')
    else:
        sentences = list(dic.keys())
        
        n = len(dic)//partition_length

        temp_list = []

        for i in range(n):
            temp_list.append(sentences[i*partition_length:(i+1)*partition_length])

        temp_list.append(sentences[(i+1)*partition_length:])

        counter = 0
        for i, l in enumerate(temp_list):
            with open("partitioned/" + str(i), "w") as f:            
                for s in l:
                    f.write(json.dumps({"id" : str(dic[s]), "title" : str(dic[s]), "text" : s})) # ???? title
                    f.write('\n')
                    counter += 1

def json_to_triples(filename, sentences_with_ids):
    ids_with_triples = {}

    with open(filename, "r") as f:
        s = json.load(f)

    for key in list(s.keys()):
        sentence = s[key][0]['sentence'][13:] # Deepex prepends a header to a sentence

        try:
            id_list = sentences_with_ids[sentence]
        except:
            print('Error: sentence could not be found: {}'.format(sentence))
            continue

        ids_with_triples[tuple(id_list)] = []

        for triple in s[key]:
            ids_with_triples[tuple(id_list)].append(json_triple_to_triple(triple))

    return ids_with_triples #format {[id1, id2...] : [triple1, triple2...], ...}

def json_to_questions_with_triples(filename, ids_with_questions):
    #this version has global sentence IDs included in JSON files

    with open(filename, "r") as f:
        s = json.load(f)

    for ids in list(s.keys()):
        triple_list = []
    
        for triple in s[ids]:
            triple_list.append(json_triple_to_triple(triple))

        #now assing these tripels to the ids_with_questions
        list_of_ids = ast.literal_eval(ids)

        for single_id in list_of_ids:
            decode_deepex_helper(single_id, triple_list, ids_with_questions)

    return ids_with_questions

def json_triple_to_triple(d):
    
    triple = data_model.Deepex_triple(
        d['subject'],
        d['relation'],
        d['object'],
        d['sentence'][13:], # Deepex prepends a header to a sentence
        d['score'],
        d['contrastive_dis']
    )

    triple.subject_words = [d['subject_char_span']]
    triple.object_words = [d['object_char_span']]

    return triple

def decode_deepex(ids_with_triples, ids_with_questions):

    for ids, triples in ids_with_triples.items():
        for id in ids:
            decode_deepex_helper(id, triples, ids_with_questions)

    return ids_with_questions

def decode_deepex_helper(id, triples, ids_with_questions):

    question = ids_with_questions['%'.join(id.split('%')[0:2])]

    if question.context_triples == None:
        question.context_triples = []

    if question.question_with_answer_triples == None:
        question.question_with_answer_triples = []

    if question.question_with_distractors_triples == None:
        question.question_with_distractors_triples = [[], [], []]

    part_of_question = id.split('%')[2]

    if part_of_question == 'context':
        question.context_triples.extend(triples)
    elif part_of_question == 'qna':
        question.question_with_answer_triples.extend(triples)
    elif part_of_question == 'qnd-0':
        question.question_with_distractors_triples[0].extend(triples)
    elif part_of_question == 'qnd-1':
        question.question_with_distractors_triples[1].extend(triples)
    elif part_of_question == 'qnd-2':
        question.question_with_distractors_triples[2].extend(triples)