import nltk.data
import re

tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')

def q_list2sentences(l):
    out = []

    for q in l:
        out.extend(question2sentences(q))
        
    return out

def question2sentences(q):
    out = []

    rx = r"\.(?=\S)"

    out.extend(tokenizer.tokenize(re.sub(rx, ". ", q.context)))
    out.extend(tokenizer.tokenize(re.sub(rx, ". ", q.question_with_answer)))

    for qnd in q.question_with_distractors:
        out.extend(tokenizer.tokenize(re.sub(rx, ". ", qnd)))

    return out

def sentences2txt(l, folder='output', filename='sentences.txt'):
    with open(folder + '/' + filename, 'w') as f:
        
        for sentence in l:
            f.write('%s\n' % sentence)

