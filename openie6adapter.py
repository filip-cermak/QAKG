import nltk.data

tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')

def q_list2sentences(l):
    out = []

    for q in l:
        out.extend(question2sentences(q))
        
    return out

def question2sentences(q):
    out = []

    out.extend(tokenizer.tokenize(q.context))
    out.extend(tokenizer.tokenize(q.question_with_answer))

    for qnd in q.question_with_distractors:
        out.extend(tokenizer.tokenize(qnd))

    return out

def sentences2txt(l, filename='sentences.txt'):
    with open('output/' + filename, 'w') as f:
        
        for sentence in l:
            f.write('%s\n' % sentence)

