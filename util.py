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
    
