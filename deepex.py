import data_model

import nltk.data
import json
import ast
from tqdm import tqdm
import numpy as np

import embed
import util
from sentence_embed import sentence_embed

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

def filter_qna_triples(triples, list_of_ids, ids_with_questions):
    #this is the simples possible implementation, may prove as not enough
    #in the future

    #check whether this sentence is going to the distractor/answer
    if not util.check_if_triple_from_choices(list_of_ids):
        return triples

    #if yes, iterate through triples excluding the ones which don't include answer/distractor
    filtered_triples = []

    #check with only the first question
    question = ids_with_questions['%'.join((list_of_ids[0]).split('%')[0:2])]

    for triple in triples:
        try:
            triple_str = triple.to_string().lower()
        except:    
            triple_str = json_triple_to_triple(triple).to_string().lower()

        if question.answer.lower() in triple_str:
            filtered_triples.append(triple)
            print("1 - activated")
        elif question.distractors[0].lower() in triple_str:
            filtered_triples.append(triple)
            print("2 - activated")
        elif question.distractors[1].lower() in triple_str:
            filtered_triples.append(triple)
            print("3 - activated")
        elif question.distractors[2].lower() in triple_str:
            filtered_triples.append(triple)
            print("4 - activated")

    return filtered_triples

def json_to_questions_with_triples(filename, ids_with_questions, triple_filter = None):
    #this version has global sentence IDs included in JSON files

    with open(filename, "r") as f:
        s = json.load(f)

    for ids in tqdm(list(s.keys())):
        triple_list = []
        list_of_ids = ast.literal_eval(ids)

        #triple filter here
        if triple_filter != None:
            s[ids] = filter_qna_triples(s[ids], list_of_ids, ids_with_questions)
    
        # take only 2 top triple acording to the contrastive loss
        s[ids] = s[ids][:2]

        # turn json triple to object, also add embeddings
        for triple in s[ids]:
            triple_list.append(enrich_deepex_triple_with_embeddings(json_triple_to_triple(triple)))

        #now assing these tripels to the ids_with_questions
        for single_id in list_of_ids:
            decode_deepex_helper(single_id, triple_list, ids_with_questions)

    return ids_with_questions

def json_triple_to_triple(d):

    o = d['offset']
    subject_char_span = [d['subject_char_span'][0] - o, d['subject_char_span'][1] - o]
    object_char_span = [d['object_char_span'][0] - o, d['object_char_span'][1] - o]
    
    triple = data_model.Deepex_triple(
        d['subject'],
        subject_char_span,
        d['relation'],
        d['object'],
        object_char_span,
        d['sentence'][13:], # Deepex prepends a header to a sentence
        d['score'],
        d['contrastive_dis']
    )

    triple.subject_words = [subject_char_span]
    triple.object_words = [object_char_span]

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

def enrich_deepex_triple_with_embeddings(deepex_triple):

    chr_spans_with_embeds = embed.embed(deepex_triple.sentence)

    subject_embeds_chr_spans = embed.chr_spn_matcher(deepex_triple.subject_char_span,
                                             list(chr_spans_with_embeds.keys()))

    object_embeds_chr_spans = embed.chr_spn_matcher(deepex_triple.object_char_span,
                                             list(chr_spans_with_embeds.keys()))

    subject_embeds = [chr_spans_with_embeds[x] for x in subject_embeds_chr_spans]
    object_embeds = [chr_spans_with_embeds[x] for x in object_embeds_chr_spans]
    relation_embeds = sentence_embed(deepex_triple.sentence)

    deepex_triple.subject_embeds = subject_embeds
    deepex_triple.object_embeds = object_embeds
    deepex_triple.relation_embeds = relation_embeds

    if average_embeds(subject_embeds)[1] == 0 or average_embeds(object_embeds)[1] == 0:
        deepex_triple.matrix = None
    else:
        deepex_triple.matrix = [average_embeds(subject_embeds)[0], relation_embeds, average_embeds(object_embeds)[0]]

    return deepex_triple

def enrich_deepex_questions_with_embeddings(q):
    util.apply_function_to_all_question_triples(q, enrich_deepex_triple_with_embeddings)

def average_embeds(embeds):
    # no structure in the embeds array!
    if len(embeds) == 0:
        return None, 0

    return (np.mean(np.array(embeds), axis = 0), len(embeds))

def resolve_question(q):
    ct = q.context_triples

    if q.question_with_answer_triples == None:
        q.question_with_answer_triples = []

    [find_match(t, ct) for t in q.question_with_answer_triples]

    if q.question_with_distractors_triples == None:
        q.question_with_distractors_triples = [[], [], []]

    for t_list in q.question_with_distractors_triples:
        [find_match(t, ct) for t in t_list]

def find_match(triple, context_triples):

    closest = -3
    for triple_b in context_triples:
        #print(triple.matrix)
        #print(dst(triple, triple_b))
        if dst(triple, triple_b) > closest:
            triple.closest_triple = triple_b
            triple.closest_triple_dst = dst(triple, triple_b)
            closest = triple.closest_triple_dst

def dst(t_a, t_b):
    #add resulting 3 cos distances
    
    if t_a.matrix == None or t_b.matrix == None: 
        print("Flag triggered")
        return -3

    out = 0

    for i in range(3):
        out += np.dot(t_a.matrix[i], t_b.matrix[i])/(np.linalg.norm(t_a.matrix[i])*np.linalg.norm(t_b.matrix[i]))

    return out

def answer_question(q, threshold):
    # returns  1 if answered correctly
    # returns  0 if answered correctly
    # returns -1 if answered correctly

    # get closest triple to Q+A triples

    if len(q.question_with_answer_triples) > 0: 
        qna_max = max([t.closest_triple_dst for t in q.question_with_answer_triples])
    else:
        qna_max = -3

    # get closest triple to Q+D triples
    qnd_max_list = [0,0,0]

    for i in range(3):
        if len(q.question_with_distractors_triples[i]) > 0:
            qnd_max_list[i] = max([t.closest_triple_dst for t in q.question_with_distractors_triples[i]])
        else:
            qnd_max_list[i] = -3

    qnd_max = max(qnd_max_list)

    if qna_max > qnd_max and qna_max > threshold:
        return np.array([1,0,0])
    
    if qnd_max > qna_max and qnd_max > threshold:
        return np.array([0,1,0])
    
    return np.array([0,0,1])

def calculate_pnr(l):
    #return (prec,recall)
    return np.array([l[0]/(l[0]+l[1]), (l[0]+l[1])/(l[0]+l[1]+l[2])])

def pnr_calc(q_list, N = 10):
    threshold_min = -3
    threshold_max = 3

    pnr = []

    for thresh in np.linspace(threshold_min, threshold_max, N):
        res = [answer_question(q, thresh) for q in q_list]
        res_mat = np.asmatrix(np.stack(res))
        res_arr_T = np.transpose(np.matrix.sum(res_mat, axis = 0))
        pnr.append(calculate_pnr(res_arr_T))

    pnr_mat = np.asmatrix(np.stack(pnr))

    return pnr_mat