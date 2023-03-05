#######################Delete for deployment############################
import sys
# caution: path[0] is reserved for script path (or '' in REPL)
sys.path.insert(1, './QAKG')
#############################################################

import os
import pickle
import lzma
from tqdm import tqdm 
import util
import os

import deepex

#1########################################################
# assign triples to questions
print("Assigning triple started")

with lzma.open("../commons/eval_question_list_filtered_coref_resolved_2022-10-22 17:20:53.876724_0.pkl", "rb") as f:
    q_list_filtered = pickle.load(f)
    ids_with_questions = deepex.create_question_ids(q_list_filtered)

input_dir_name = '????'

for file_name in tqdm(sorted(os.listdir(input_dir_name))): 
    deepex.json_to_questions_with_triples(input_dir_name + '/' + file_name, ids_with_questions, triple_filter=deepex.filter_qna_triples)

#2########################################################
output_dir_name = '????'

[deepex.resolve_question(q) for q in tqdm(list(ids_with_questions.values()))]

print("Partitioning")
util.partition_and_save(list(ids_with_questions.values()), 100, output_dir_name)