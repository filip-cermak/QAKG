import neuralcoref
import en_core_web_lg
import pickle

from data_model import question_list_builder
from coref import resolve_question_list_coreference
from triple_ex import extract_triples_from_question_list

nlp = en_core_web_lg.load()
neuralcoref.add_to_pipe(nlp)

question_list = question_list_builder()
question_list_subset = question_list[10000:20000]
resolve_question_list_coreference(nlp, question_list_subset)
extract_triples_from_question_list(question_list_subset)

with open('adjusted_question_list_2.pkl', 'wb') as out:
  pickle.dump(question_list_subset, out, pickle.HIGHEST_PROTOCOL)
