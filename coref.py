def resolve_coreference(nlp_object, input_text):
  doc = nlp_object(input_text)
  output_text = doc._.coref_resolved
  return output_text

def resolve_question_list_coreference(nlp, question_list):
  
  l = len(question_list)
  print(f'Total number of questions: {l}')

  for i,q in enumerate(question_list):
    q.context_cor_resolved = resolve_coreference(nlp, q.context)
    q.question_with_answer_cor_resolved = resolve_coreference(nlp, q.question_with_answer)
    q.question_with_distractors_cor_resolved = [resolve_coreference(nlp, i) for i in q.question_with_distractors]

    print(f'Question {i} out of {l}')

  return question_list
