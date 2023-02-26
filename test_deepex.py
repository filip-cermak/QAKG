import deepex
import data_model
import nltk.data
import os
import json
import numpy as np
import lzma
import pickle
import util


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

    assert list(out.keys()) == ["a%0", "b%0", "b%1", "a%1", "c%0"]        

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

    """     deepex.export_dic_to_jsonl(
        {
            'a' : ['1', '2'],
            'b' : ['2'],
            'c' : ['4'],
            'd' : ['4'],
            'e' : ['4'],
            'f' : ['4'],
            'g' : ['4'],
        },
        True,
        3
    )

    """
    
def test_json_to_triples():

    sentences_with_ids = {
        'a' : ['q%0%context%0'],
        'b' : ['q%0%qnd-1%0']
        }

    out = deepex.json_to_triples('test_files/P0_result.json', sentences_with_ids)

def test_json_triple_to_triple():

    with open('test_files/P0_result.json', 'r') as f:
        s = json.load(f)

    triple = s['0000000000000000000000000000000000000001'][0]
    
    deepex_triple = deepex.json_triple_to_triple(triple)

def test_enrich_deepex_triple_with_embeddings():
    with open('test_files/deepex-test-output-2.json', 'r') as f:
        s = json.load(f)

    triple_dict = s["0000000000000000000000000000000000001736"][8]

    triple = deepex.json_triple_to_triple(triple_dict)

    deepex.enrich_deepex_triple_with_embeddings(triple)

def test_decode_deepex():
    #TODO
    pass
    #deepex.decode_deepex()

def test_decode_deepex_helper():
    #TODO
    """
    with open('test_files/P0_result.json', 'r') as f:
        s = json.load(f)

    question_list = []

    ids_with_questions = deepex.create_question_ids(question_list)


    triples = {
        ['q%0%context%0', 'q%0%qnd-1%0'] : deepex.json_triple_to_triple(s['0000000000000000000000000000000000000001'][0])
    }

    deepex.decode_deepex_helper(id, triples, ids_with_questions)

    """

def test_average_embeds():
    #test compare
    t_2 = data_model.Deepex_triple("", "", "", "", "", "", "", "")
    t_2.subject_embeds = [np.array([0,1]), np.array([-1,0]), np.array([1,0.5])]
    t_2.relation_embeds = [np.array([3,4]), np.array([3,4]), np.array([3,4])]
    t_2.object_embeds = [np.array([-5,3])]

    assert np.array_equal(deepex.average_embeds(t_2.subject_embeds)[0], np.array([0,0.5]))
    assert deepex.average_embeds(t_2.subject_embeds)[1] == 3

    assert np.array_equal(deepex.average_embeds(t_2.relation_embeds)[0], np.array([3,4]))
    assert deepex.average_embeds(t_2.relation_embeds)[1] == 3

    assert np.array_equal(deepex.average_embeds(t_2.object_embeds)[0], np.array([-5,3]))
    assert deepex.average_embeds(t_2.object_embeds)[1] == 1

def test_resolve_question():
    pass

def test_dst():
    # test on real data with one triple containing None
    with lzma.open("./test_files/deepex_match.pkl", "rb") as f:
        q_list = pickle.load(f)

    t_1 = q_list[0].context_triples[0]
    t_2 = q_list[0].question_with_answer_triples[0]
    #t_1.matrix[0] = np.nan

    #assert deepex.dst(t_2, t_1) == -3
    #assert deepex.dst(t_1, t_2) == -3

    t_1.matrix[0] = t_2.matrix[0] 

    assert deepex.dst(t_1, t_2) != -3
    assert deepex.dst(t_2, t_1) != -3

    # tests on mocked triples
    t_1.matrix = [np.array([1, 2, 3]), np.array([0, 0, 0, 1]), np.array([3])]
    t_2.matrix = [np.array([5, 6, 7]), np.array([1, 2, 3 ,4]), np.array([4])]

    correct_dist = 0.9683 + 0.730 + 1
    assert abs(deepex.dst(t_1, t_2) - correct_dist) < 0.01 

    #t_2.matrix = [np.nan, np.array([1, 2, 3 ,4]), np.array([4])]
    #assert deepex.dst(t_2, t_1) == -3

def test_find_match():

    triple_set = []

    for i in range(3):
        triple_set.append(data_model.Deepex_triple("", "", "", "", "", "", "", ""))

    triple_set[0].matrix = [np.array([1, 2, 3]), np.array([0, 0, 0, 1]), np.array([3])]
    triple_set[1].matrix = [np.array([1, 2, 3]), np.array([0, 10, 0, 1]), np.array([3])]
    triple_set[2].matrix = None
    
    ref_triple = data_model.Deepex_triple("", "", "", "", "", "", "", "")
    ref_triple.matrix = [np.array([1, 2, 3]), np.array([0, 0, 0, 1]), np.array([3])]
    
    deepex.find_match(ref_triple, triple_set)

    assert ref_triple.closest_triple_dst == 3

def test_resolve_question():
    q = data_model.Question("", "", "", "", "")

    triple_set = []
    for i in range(3):
        triple_set.append(data_model.Deepex_triple("", "", "", "", "", "", "", ""))

    triple_set[0].matrix = [np.array([1, 2, 3]), np.array([0, 0, 0, 1]), np.array([3])]
    triple_set[1].matrix = [np.array([1, 2, 3]), np.array([0, 10, 0, 1]), np.array([3])]
    triple_set[2].matrix = None

    q.context_triples = triple_set

    ref_triple = data_model.Deepex_triple("", "", "", "", "", "", "", "")
    ref_triple.matrix = [np.array([1, 2, 3]), np.array([0, 0, 0, 1]), np.array([3])]

    assert ref_triple.closest_triple_dst == None

    q.question_with_answer_triples = [ref_triple]
    q.question_with_distractors_triples = []

    deepex.resolve_question(q)

    assert ref_triple.closest_triple_dst == 3

def test_answer_question():

    with lzma.open("./test_files/0.pkl", "rb") as f:
        q_list = pickle.load(f)
    #load single question

    [deepex.answer_question(q, 2.7) for q in q_list]

def test_filter_qna_triples():
    
    #test case 1 
    triple_1 = util.mock_json_from_deepex_triple(data_model.Deepex_triple("cat", [], "sat", "on mat", [], "", "", ""))
    triple_2 = util.mock_json_from_deepex_triple(data_model.Deepex_triple("sat", [], "cat", "on mat", [], "", "", ""))
    triple_3 = util.mock_json_from_deepex_triple(data_model.Deepex_triple("dog", [], "sat", "on mat", [], "", "", ""))

    triples = [
        triple_1,
        triple_2,
        triple_3,
    ]
    
    list_of_ids = [
        'RACE/test/middle/6370.txt%0%asnwer%1', 
        'RACE/test/middle/6370.txt%1%context%1']
    
    ids_with_questions = {
        'RACE/test/middle/6370.txt%0' : data_model.Question("window", "tree", ["patch", "cat", "eight"], "", "")
        }

    output = deepex.filter_qna_triples(triples, list_of_ids, ids_with_questions)
    assert [triple_1, triple_2] == deepex.filter_qna_triples(triples, list_of_ids, ids_with_questions)
    
    #test case 2
    triple_1 = util.mock_json_from_deepex_triple(data_model.Deepex_triple("cat", [], "sat", "on mat", [], "", "", ""))
    triple_2 = util.mock_json_from_deepex_triple(data_model.Deepex_triple("sat", [], "cat", "on mat", [], "", "", ""))
    triple_3 = util.mock_json_from_deepex_triple(data_model.Deepex_triple("dog", [], "sat", "on mat", [], "", "", ""))

    triples = [
        triple_1,
        triple_2,
        triple_3,
    ]
    
    list_of_ids = [
        'RACE/test/middle/6370.txt%0%context%1', 
        'RACE/test/middle/6370.txt%1%context%1']
    
    ids_with_questions = {
        'RACE/test/middle/6370.txt%0' : data_model.Question("window", "tree", ["patch", "window", "eight"], "", "")
        }

    output = deepex.filter_qna_triples(triples, list_of_ids, ids_with_questions)
    assert [triple_1, triple_2, triple_3] == deepex.filter_qna_triples(triples, list_of_ids, ids_with_questions)

    #test case 3
    triple_1 = util.mock_json_from_deepex_triple(data_model.Deepex_triple("cat", [], "sat", "on mat", [], "", "", ""))
    triple_2 = util.mock_json_from_deepex_triple(data_model.Deepex_triple("sat", [], "cat", "on mat", [], "", "", ""))
    triple_3 = util.mock_json_from_deepex_triple(data_model.Deepex_triple("dog", [], "sat", "on mat", [], "", "", ""))

    triples = [
        triple_1,
        triple_2,
        triple_3,
    ]
    
    list_of_ids = [
        'RACE/test/middle/6370.txt%0%asnwer%1', 
        'RACE/test/middle/6370.txt%1%context%1']
    
    ids_with_questions = {
        'RACE/test/middle/6370.txt%0' : data_model.Question("window", "tree", ["patch", "window", "eight"], "", "")
        }

    output = deepex.filter_qna_triples(triples, list_of_ids, ids_with_questions)
    assert [] == deepex.filter_qna_triples(triples, list_of_ids, ids_with_questions)
