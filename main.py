import neuralcoref
import en_core_web_lg
import pickle

from datetime import datetime

from data_processing import question_list_builder
from coref import resolve_question_list_coreference
from triple_ex import extract_triples_from_question_list

nlp = en_core_web_lg.load()
neuralcoref.add_to_pipe(nlp)

question_list = question_list_builder()

print("The total number of questions: ", len(question_list))

print("Resolve Coreference")
resolve_question_list_coreference(nlp, question_list)

# Delete special characters from all strings, except for .,!?:, also omit \* characters like \n

print("Extract triples")
extract_triples_from_question_list(question_list)

with open('output/adjusted_question_list_' + str(datetime.now(tz=None)) + '_' + str(0) + '.pkl', 'wb') as out:
  pickle.dump(question_list, out, pickle.HIGHEST_PROTOCOL)

""" n = 1000
for i in range(0,30):
  question_list_subset = question_list[i*n:(i+1)*n]

  resolve_question_list_coreference(nlp, question_list_subset)
  extract_triples_from_question_list(question_list_subset)

  with open('output/adjusted_question_list_' + str(datetime.now(tz=None)) + '_' + str(i) + '.pkl', 'wb') as out:
    pickle.dump(question_list_subset, out, pickle.HIGHEST_PROTOCOL) """