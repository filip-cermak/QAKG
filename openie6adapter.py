import nltk.data
import re

tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')

def q_list2sentences(l):
    out = []

    for i, q in enumerate(l):
        out.extend(question2sentences(i, q))
        
    return out

def question2sentences(id, q):
    out = []

    rx = r"\.(?=\S)"

    out.extend(["Context number {}!".format(id)])
    out.extend(tokenizer.tokenize(re.sub(rx, ". ", q.context_cor_resolved)))

    out.extend(["Answer number {}!".format(id)])
    out.extend(tokenizer.tokenize(re.sub(rx, ". ", q.question_with_answer_cor_resolved)))

    for i, qnd in enumerate(q.question_with_distractors_cor_resolved):
        out.extend(["Distractor number {} {}!".format(id, i)])
        out.extend(tokenizer.tokenize(re.sub(rx, ". ", qnd)))

    return out

def sentences2txt(l, folder='output', filename='sentences.txt'):
    with open(folder + '/' + filename, 'w') as f:
        
        for sentence in l:
            f.write('%s\n' % sentence)

