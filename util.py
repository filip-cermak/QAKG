from asynchat import simple_producer
import pickle
import lzma


def intersect(a, b):
    fst, snd = (a, b) if len(a) < len(b) else (b, a)
    return list(set(fst).intersection(snd))

def intersect_len(a, b):
    return len(intersect(a,b))

def fuzzy_pair_intersect(a, b):
    pass

def compare_helper(a, b):
    out = [0]*len(a)

    for i in range(len(a)):
        if a[i] in b:
            out[i] = 1

    return out

def summarize_dict(dictionary):
    out = {}

    for key in list(dictionary.keys()):
        out[key] = len(dictionary[key])

    return out

def question_answer_joiner(question, answer):
    underscore_count = question.count("_")

    if underscore_count == 1:
        return question.replace("_", answer)
    elif underscore_count > 1:
        print("Multiple underscores, cannot resolve")
    
    return question + " " + answer
    
def merge_dicts(main_dic, add_dic):
    for key in main_dic.keys():
        main_dic[key] += add_dic[key]

    return main_dic

def new_line_symbol_remover(s):
    return s.replace("\n", " ")

def content_triple_filter(triple_list, text, verbose = False):
    """Filter out all triples that do not share a word with the text"""
    triple_list_out = []

    for triple in triple_list:  
        if word_matcher(triple.to_string(), text):
            triple_list_out.append(triple)

    if verbose:
        print([x.to_string() for x in list(set(triple_list) - set(triple_list_out))])

    return triple_list_out

def word_matcher(a, b):
    """if at least one word of lenght 3 or more matches, return true"""

    for word in a.lower().split():
        if (word in b.lower().split()) and len(word) >=3:
            return True

    return False

def relativize(d):
    net = sum(d.values())
    out = {}
    for k, v in d.items():
        out[k] = v/net

    return out

def analyse(e_list):
    # Make statistics - xx% of triple generated from Q+A were found in the context, xx%
    qna_def = {"full" : 0, "lp" : 0, "rp" : 0, "sp" : 0, "o" : 0, "r" : 0, "s" : 0, "" : 0}
    dna_def = {"full" : 0, "lp" : 0, "rp" : 0, "sp" : 0, "o" : 0, "r" : 0, "s" : 0, "" : 0}

    for e in e_list:
        qna = e.correct_answer_matches_summary
        dnas = e.distractors_matches_summary

        qna_def = merge_dicts(qna_def, qna)

        for dna in dnas:
            dna_def = merge_dicts(dna_def, dna)

    return qna_def, relativize(qna_def), dna_def, relativize(dna_def)

def fuzzy_dict_simplifier(complicated_dic, option = None):
    """
    Simple match aggregator for downstream analysis
    """

    simpler_dic = {
        "triple": complicated_dic["full"], 
        "double": complicated_dic["lp"] + complicated_dic["rp"] + complicated_dic["sp"], 
        "single": complicated_dic["o"] + complicated_dic["r"] + complicated_dic["s"], 
        "none": complicated_dic[""] 
        }

    if option != None:
        simpler_dic["option"] = option

    return simpler_dic


def analyse_simple(e_list):
    # Make statistics - xx% of triple generated from Q+A were found in the context, xx%
    qna_def = {"full" : 0, "lp" : 0, "rp" : 0, "sp" : 0, "o" : 0, "r" : 0, "s" : 0, "" : 0}
    qnd_def = {"full" : 0, "lp" : 0, "rp" : 0, "sp" : 0, "o" : 0, "r" : 0, "s" : 0, "" : 0}

    for e in e_list:
        qna = e.correct_answer_matches_summary
        qnds = e.distractors_matches_summary

        qna_def = merge_dicts(qna_def, qna)

        for dna in qnds:
            qnd_def = merge_dicts(qnd_def, dna)

    output_qna = fuzzy_dict_simplifier(qna_def)
    output_qnd = fuzzy_dict_simplifier(qnd_def)

    return output_qna, relativize(output_qna), output_qnd, relativize(output_qnd)

def filter_triples(question_list):

    #filter answer triples
    for q in question_list:
        q.question_with_answer_triples = content_triple_filter(q.question_with_answer_triples, q.answer)

    #filter distractor triples 
    for q in question_list:
        for i in range(len(q.question_with_distractors_triples)):
            q.question_with_distractors_triples[i] = content_triple_filter(q.question_with_distractors_triples[i], q.distractors[i])

    return question_list

def compare_matches(a, b):

    if a["triple"] == b["triple"] and a["double"] == b["double"] and a["single"] == b["single"]:
        return True

    return False

def summarize_list(l):

    out = {}

    for el in l:
        if el not in out:
            out[el] = 1
        else:
            out[el] += 1

    return out

def partition_and_save(list_of_objects, objects_per_partition, folder):

    n = len(list_of_objects)//objects_per_partition

    for i in range(n):
        with lzma.open(folder + "/" + str(i) + ".pkl", "wb") as f:
            pickle.dump(list_of_objects[i*objects_per_partition:(i+1)*objects_per_partition], f)

def apply_function_to_all_question_triples(q, fn):

    """
    print("start")
    print("Triple counts, context: {}, Q+A: {}".format(len(q.context_triples), len(q.question_with_answer_triples)))
    print("{}, {}, {}".format(len(q.question_with_distractors_triples[0]), len(q.question_with_distractors_triples[1]), len(q.question_with_distractors_triples[2])))
    """
    
    [fn(t) for t in q.context_triples]
    [fn(t) for t in q.question_with_answer_triples]

    for t_list in q.question_with_distractors_triples:
        [fn(t) for t in t_list]
    print("end")