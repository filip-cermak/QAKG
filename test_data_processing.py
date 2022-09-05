import data_processing
import data_model

def test_question_triple_transformer():
    input_question = data_model.Question("a", "b", "c", "d", "e")

    input_question.context_triples = ["a-b-c"]
    input_question.question_with_answer_triples = ["d-e-f"]
    input_question.question_with_distractors_triples = [
        ["e-r-f", "t-y-u"], 
        ["d-f-s"], 
        []]

    output_question = data_processing.question_triple_transformer(input_question)

    assert output_question.context_triples[0] == data_model.Triple("a", "b", "c")

    assert output_question.question_with_distractors_triples[0][1] == data_model.Triple("t", "y", "u")
