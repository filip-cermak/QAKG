import json
import glob

class Question:
  def __init__(self, question, answer, distractors, context, id):
    self.question = question
    self.answer = answer
    self.distractors = distractors
    self.context = context
    self.id = id

    self.question_with_answer = self.question + " " + self.answer
    self.question_with_distractors =[self.question + " " + d for d in self.distractors]

    # Fields for text after the coreference is resolved
    self.context_cor_resolved = None
    self.question_with_answer_cor_resolved = None
    self.question_with_distractors_cor_resolved = None

    # Fields for triple generation
    self.context_triples = None
    self.question_with_answer_triples = None
    self.question_with_distractors_triples = None

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

# Probably should create new class, but for now leaving like this:

def entry_builder(filename):
  j = json.load(open(filename)) 
  return Entry(j["answers"], j["options"], j["questions"], j["article"], filename) #filename used as id instead

def entry_list_builder():
  root_dir = "RACE"
  file_list = list(glob.iglob(root_dir + "/**/*.txt", recursive=True))
  entry_list = [entry_builder(filename) for filename in file_list]
  return entry_list

def question_list_builder():
  entry_list = entry_list_builder()

  question_list = []
  for entry in entry_list:
    question_list.extend(entry.generate_questions())

  return question_list