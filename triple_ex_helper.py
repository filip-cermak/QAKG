import data_model

def triple2string(triple):
  return triple.subject + "-" + triple.relation + "-" + triple.object

def triple2object(triple):
  t_out = data_model.Triple(triple.subject, triple.relation, triple.object, triple.confidence)

  t_out.subject_tokens = triple.subjectTokens
  t_out.relation_tokens = triple.relationTokens
  t_out.object_tokens = triple.objectTokens

  return t_out

def extract_triples_helper(text, extractor_client):
 
  document = extractor_client.annotate(text)

  triples = []

  for i_s, s in enumerate(document.sentence):
    triples_temp = []

    for j_t, t in enumerate(s.openieTriple):
        triples_temp.append(triple2object(t))

    #convert tokens into word locations
    triples_temp = [tokens2loc(t, i_s, s) for t in triples_temp]

    triples.extend(triples_temp)

  return triples

def tokens2loc(triple, i, sentence):

  sentence_tokens = sentence.token

  resolve_dic = {}

  for t in sentence_tokens:
    resolve_dic[t.tokenBeginIndex-sentence.tokenOffsetBegin] = [t.beginChar, t.endChar] 
    
    if t.tokenBeginIndex + 1 != t.tokenEndIndex:  
      raise ValueError

  triple.subject_words = tokens2loc_helper(triple.subject_tokens, resolve_dic)
  triple.relation_words = tokens2loc_helper(triple.relation_tokens, resolve_dic)
  triple.object_words = tokens2loc_helper(triple.object_tokens, resolve_dic)

  #check whether all tokens from the current sentence
  token_check = triple.subject_tokens + triple.relation_tokens + triple.object_tokens
  test_out = [t for t in token_check if t.SentenceIndex != i]

  if len(test_out) > 0:
    raise ValueError

  return triple

def tokens2loc_helper(token_list, resolve_dic):
  
  return [resolve_dic[t.tokenIndex] for t in token_list]
