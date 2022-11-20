import deepex
import data_model
import nltk.data
import os


def test_create_question_ids():

    class Dummy_q:
        def __init__(self, id):
            self.id = id

    out = deepex.create_question_ids(
        [
            Dummy_q("a"), 
            Dummy_q("b"),
            Dummy_q("b"),
            Dummy_q("a"), 
            Dummy_q("c")
        ])

    assert out == ["a%0", "b%0", "b%1", "a%1", "c%0"]        

def test_sentence_assigner():

    out = {
        "a" : ["0"]
    }

    sentences = [
        "a",
        "b",
        "c"
    ]

    id_prefix = "q1%context"

    want = {
        "a" : ["0", "q1%context%0"],
        "b" : ["q1%context%1"],
        "c" : ["q1%context%2"]
    }

    assert deepex.sentence_assigner(sentences, id_prefix, out) == want


def test_prepare_for_deepex_helper():

    """     class Tok:
            def __init__(self, sentences):
                self.sentences = sentences

            def tokenize(self, _):
                return self.sentences
    """

    tok = nltk.data.load('tokenizers/punkt/english.pickle')

    q = data_model.Question("", "", "", "", "")
    q.context_cor_resolved = "Car. Dog."
    q.question_with_answer_cor_resolved = "Bike? Banana"
    q.question_with_distractors_cor_resolved = [
        "apple. On trees.",
        "orange. In a basket.",
        "cherry. "
    ]

    out = {}

    want = {
        'Banana' : ['q_0%qna%1'],
        'Bike?' : ['q_0%qna%0'],
        'Car.' : ['q_0%context%0'],
        'Dog.' : ['q_0%context%1'],

        'apple.' : ['q_0%qnd-0%0'],
        'On trees.' : ['q_0%qnd-0%1'],

        'orange.' : ['q_0%qnd-1%0'],
        'In a basket.' : ['q_0%qnd-1%1'],

        'cherry.' : ['q_0%qnd-2%0'],
    }

    assert want == deepex.prepare_for_deepex_helper(tok, q, "q_0", out)
    
    q_1 = data_model.Question("", "", "", "", "")
    q_1.context_cor_resolved = "Bike? Banana"
    q_1.question_with_answer_cor_resolved = "Car. Dog."
    q_1.question_with_distractors_cor_resolved = [
        "cherry. ",
        "orange. In a basket.",
        "orange. In a basket."
    ]

    want = {
        'Banana' : ['q_0%qna%1', 'q_1%context%1'],
        'Bike?' : ['q_0%qna%0', 'q_1%context%0'],
        'Car.' : ['q_0%context%0', 'q_1%qna%0'],
        'Dog.' : ['q_0%context%1', 'q_1%qna%1'],

        'apple.' : ['q_0%qnd-0%0'],
        'On trees.' : ['q_0%qnd-0%1'],

        'orange.' : ['q_0%qnd-1%0', 'q_1%qnd-1%0', 'q_1%qnd-2%0'],
        'In a basket.' : ['q_0%qnd-1%1', 'q_1%qnd-1%1', 'q_1%qnd-2%1'],

        'cherry.' : ['q_0%qnd-2%0', 'q_1%qnd-0%0'],
    }

    assert want == deepex.prepare_for_deepex_helper(tok, q_1, "q_1", out)


def test_export_dic_to_jsonl():
    deepex.export_dic_to_jsonl(
        {
            'a' : ['1', '2'],
            'b' : ['2'],
            'c' : ['4']
        }
    )

    os.remove("P0.jsonl")