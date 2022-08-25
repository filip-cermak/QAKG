import pickle

#with open("output/adjusted_question_list_2022-08-25 21:49:21.033880_4.pkl", 'rb') as input:
with open("output/adjusted_question_list_2022-08-25 21:48:49.690137_2.pkl", 'rb') as input:
  q = pickle.load(input)

print(q[0].context_triples)