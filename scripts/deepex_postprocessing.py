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

for file_name in tqdm(sorted(os.listdir('partitioned-results-mini'))): 
    deepex.json_to_questions_with_triples('partitioned-results-mini/' + file_name, ids_with_questions)

#2########################################################
dir_name_1 = 'partitioned-mini-deepex-postprocessing-1'
#dir_name_2 = 'partitioned-mini-deepex-postprocessing-2'

[deepex.resolve_question(q) for q in tqdm(list(ids_with_questions.values()))]

print("Partitioning")
util.partition_and_save(list(ids_with_questions.values()), 100, dir_name_1)