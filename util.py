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

def content_triple_filter(triple_list, text):
    """Filter out all triples that do not share a word with the text"""
    triple_list_out = []

    for triple in triple_list:  
        if word_matcher(triple.to_string(), text):
            triple_list_out.append(triple)

    return triple_list_out

def word_matcher(a, b):
    """if at least one word of lenght 3 or more matches, return true"""

    for word in a.lower().split():
        if (word in b.lower().split()) and len(word) >=3:
            return True

    return False
