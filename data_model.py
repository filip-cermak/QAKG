import util
import numpy as np

class Question:

  def __init__(self, question, answer, distractors, context, id):
    self.question = question
    self.answer = answer
    self.distractors = distractors
    self.context = context
    self.id = id

    self.question_with_answer = util.question_answer_joiner(self.question, self.answer)
    self.question_with_distractors =[util.question_answer_joiner(self.question, d) for d in self.distractors]

    # Fields for text after the coreference is resolved
    self.context_cor_resolved = None
    self.question_with_answer_cor_resolved = None
    self.question_with_distractors_cor_resolved = None

    # Fields for triple generation
    self.context_triples = None
    self.question_with_answer_triples = None
    self.question_with_distractors_triples = None

  def print_question(self):

    print("#########################################")
    print("Context")
    print(self.context)
    print("-----------------------------------------")
    print("Question")
    print(self.question)
    print("-----------------------------------------")
    print("Answer")
    print(self.answer)
    print("-----------------------------------------")
    print("Distractors")
    print(self.distractors)
    print("#########################################")
    print("Context_triples")
    print(self.context_triples)
    print("-----------------------------------------")
    print("Answer_triples")
    print(self.question_with_answer_triples)
    print("-----------------------------------------")
    print("Distractors_triples")
    print(self.question_with_distractors_triples)
    print("#########################################")
    print("Context - coref resolved")
    print(self.context_cor_resolved)
    print("-----------------------------------------")
    print("Answer - coref resolved")
    print(self.question_with_answer_cor_resolved)
    print("-----------------------------------------")
    print("Distractors - coref resolved")
    print(self.question_with_distractors_cor_resolved)
    print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
  
class Entry:

  def __init__(self, answers, options, questions, article, id):
    # Default Params
    self.answers = answers
    self.options = options
    self.questions = questions
    self.article = article
    self.id = id

    # Computed Params
    self.answers_numeric = [ord(c)-65 for c in answers]

  def generate_questions(self):
    questions_list = []
    questions_count = len(self.questions)

    for i in range(questions_count):

      answer = self.options[i][self.answers_numeric[i]]
      distractors = self.options[i]
      distractors.remove(answer)     

      questions_list.append(
          Question(self.questions[i],
                   answer,
                   distractors,
                   self.article,
                   self.id
                   ))

    return questions_list

class Eval:
    
  def __init__(self, q):
    self.question = q
    self.id = q.id

    #composite eval

    self.correct_answer_matches = self.compare(q.question_with_answer_triples, q.context_triples)
    self.distractors_matches = [self.compare(d, q.context_triples) for d in q.question_with_distractors_triples]

    self.correct_answer_matches_summary = util.summarize_dict(self.correct_answer_matches)
    self.distractors_matches_summary = [util.summarize_dict(i) for i in self.distractors_matches] 

  def compare(self, triple_set_a, triple_set_b):
    """
    Picks triples from triple_set_a which match any triple from triple_set_b and
    assing type of a match
    """

    dictionary = {}
    match_types = ["full", "lp", "rp", "sp", "o", "r", "s", ""]
    
    for m in match_types:
      dictionary[m] = []

    if triple_set_a == "":
      return dictionary

    for triple_a in triple_set_a:
      longest_match = ""
      triple_match = None
      for triple_b in triple_set_b:
        match_type = triple_a.match(triple_b)

        if len(longest_match) < len(match_type):
          longest_match = match_type
          triple_match = triple_b

      if triple_match != "":
        dictionary[longest_match].append([triple_a, triple_match])
      else:
        dictionary[longest_match].append([triple_a, Triple("#", "#", "#")])
        
    return dictionary


class Triple: #todo - make a base Triple class and child triple classes

  def __init__(self, subject, relation, object, confidence = 1):
    self.subject = subject
    self.relation = relation
    self.object = object

    self.confidence = confidence

    #these lists contain dictionaries of the form {sentenceIndex:0, tokenIndex:1}
    self.subject_tokens = None 
    self.relation_tokens = None
    self.object_tokens = None

    #these lists contain pairs [x,y] where x is the first character of the word and
    #y is the first character after the word 
    self.subject_words = None 
    self.relation_words = None
    self.object_words = None

    #thise lists contain lists of vector embeddings, each embedding list corresponds to one word
    self.subject_embeds = [] 
    self.relation_embeds = []
    self.object_embeds = []
  
  """
  def __repr__(self):
    return self.subject + "-@-" + self.relation + "-@-" + self.object

  def __str__(self):
    return self.subject + "-@-" + self.relation + "-@-" + self.object
  """

  def to_string(self, sep = " "):
    return self.subject + sep + self.relation + sep + self.object

  def match(self, other):
    """Types of matches: full match - "full"
                         left pair - "lp"
                         right pair - "rp"
                         side pair - "sp"
                         subject - "s"
                         relation - "r"
                         object - "o"
                         none - ""
    """

    if self.subject == other.subject and self.relation == other.relation and self.object == other.object:
      return "full"

    if self.subject == other.subject and self.relation == other.relation:
      return "lp"

    if self.relation == other.relation and self.object == other.object:
      return "rp"

    if self.subject == other.subject and self.object == other.object:
      return "sp"

    if self.subject == other.subject:
      return "s"

    if self.relation == other.relation:
      return "r"

    if self.object == other.object:
      return "o"

    return ""

  def semantic_triple(self):
    return [self.subject_words, self.relation_words, self.object_words]

  def make_pickable(self):
    self.subject_tokens = None 
    self.relation_tokens = None
    self.object_tokens = None

class Deepex_triple(Triple):
  def __init__(self, subject, relation, object, score, contrastive_dis):
    Triple.__init__(self, subject, relation, object, 1)

    self.score = score
    self.contrastive_dis = contrastive_dis

class Semantic_triple():
  def __init__(self, triple):

    self.subject = triple.subject
    self.relation = triple.relation
    self.object = triple.object

    self.subject_embed, self.subject_embed_count = self.analyse_embeddings(triple.subject_embeds)
    self.relation_embed, self.relation_embed_count = self.analyse_embeddings(triple.relation_embeds)
    self.object_embed, self.object_embed_count =  self.analyse_embeddings(triple.object_embeds)

    self.matrix = None
    self.best_match_triple = None

    if self.subject_embed_count != 0 and self.relation_embed_count != 0 and self.object_embed_count != 0:
      self.matrix = np.row_stack((self.subject_embed, self.relation_embed, self.object_embed))

  def analyse_embeddings(self, embeds):

    #make a list of embeddings
    L = []

    for word in embeds:
      for embed in word:
        L.append(embed)

    if len(L) == 0:
      return None, 0

    return np.mean(np.array(L), axis = 0), len(L)

  def compare(self, semantic_triple):
    
    distances = np.zeros(3)

    A = self.matrix
    B = semantic_triple.matrix

    if type(A) == np.ndarray and type(B) == np.ndarray:
      for i in range(3):
        
        norm_A = np.linalg.norm(A[i, :])
        norm_B = np.linalg.norm(B[i, :])

        if norm_A == 0 or norm_B == 0:
          distances[i] = 0
          continue  
        
        #cosine similarity
        distances[i] = np.dot(A[i, :], B[i, :])/(np.linalg.norm(A[i, :])*np.linalg.norm(B[i, :]))

        #print("i:{}, dot:{}, A:{}, B:{}".format(distances[i], np.dot(A[i, :], B[i, :]), A[i, :], B[i, :]))

      return sum(distances)
    else:
      return "undefined"
  
  def pick_best_match(self, semantic_triple_list):
    triples_with_distances = []

    for triple in semantic_triple_list:
      dist = self.compare(triple)
      if dist != "undefined":
        triples_with_distances.append((self.compare(triple), Primitive_Triple(triple)))

    triples_with_distances_sorted = sorted(triples_with_distances, key= lambda x: x[0], reverse=True)

    self.best_match_triple = triples_with_distances_sorted[0][1]

class Primitive_Triple():
  def __init__(self, triple):
    self.subject = triple.subject
    self.relation = triple.relation
    self.object = triple.object