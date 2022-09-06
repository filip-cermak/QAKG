import json
import glob
import data_model

def entry_builder(filename):
  j = json.load(open(filename)) 
  return data_model.Entry(j["answers"], j["options"], j["questions"], j["article"], filename) #filename used as id instead

def entry_list_builder():
  """
  Only takes in test samples
  """
  root_dir = "RACE/test"
  file_list = list(glob.iglob(root_dir + "/**/*.txt", recursive=True))
  entry_list = [entry_builder(filename) for filename in file_list]
  return entry_list

def question_list_builder():
  entry_list = entry_list_builder()

  question_list = []
  for entry in entry_list:
    question_list.extend(entry.generate_questions())

  return question_list

def triple_str_to_triple(triple_str):
    triple_str_list = triple_str.split("-")

    if len(triple_str_list) != 3:
        print("*" + triple_str + "* contains more dashes than expected")

    return data_model.Triple(triple_str_list[0],
                             triple_str_list[1],
                             triple_str_list[2])

def convert_str_triple_list_to_obj_triple_list(str_triple_list):
    return [triple_str_to_triple(t) for t in str_triple_list]


def question_triple_transformer(q):

    out = data_model.Question(q.question, 
                              q.answer, 
                              q.distractors, 
                              q.context,
                              q.id)

    out.context_cor_resolved = q.context_cor_resolved
    out.question_with_answer_cor_resolved = q.question_with_answer_cor_resolved
    out.question_with_distractors_cor_resolved = q.question_with_distractors_cor_resolved

    out.context_triples = convert_str_triple_list_to_obj_triple_list(q.context_triples)
    out.question_with_answer_triples = convert_str_triple_list_to_obj_triple_list(q.question_with_answer_triples)

    out.question_with_distractors_triples = [convert_str_triple_list_to_obj_triple_list(l) for l in q.question_with_distractors_triples]

    return out