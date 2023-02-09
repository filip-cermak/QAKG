import embed
import data_model

import pickle

def test_contains_chr_spn():

    assert embed.contains_chr_spn((1, 3), (1, 3)) == True
    assert embed.contains_chr_spn((1, 3), (1, 2)) == True
    assert embed.contains_chr_spn((1, 3), (0, 3)) == True 
    assert embed.contains_chr_spn((1, 3), (2, 3)) == True 
    assert embed.contains_chr_spn((5, 6), (6, 7)) == False
    assert embed.contains_chr_spn((5 , 8), (1 ,5)) == False

def test_chr_spn_matcher():
    assert embed.chr_spn_matcher((1,3), [(1,3), (1,2), (0,3), (3,4)]) == [(1,3), (1,2), (0,3)]
 
def test_enrich_triples():
    triples = [
        data_model.Triple("", "", ""),
        data_model.Triple("", "", "")
    ]

    triples[0].subject_words = [[0,1], [1,2]]
    triples[0].relation_words = [[0,1]]
    triples[0].object_words = [[0,1]]

    triples[1].subject_words = [[3,6]]
    triples[1].relation_words = [[3,6]]
    triples[1].object_words = [[3,4], [5,8]]

    chr_spans_with_embeddings = {
        (0,1) : [0],
        (1,2) : [1],
        (3,4) : [2],
        (2,5) : [3],
        (7,8) : [4],
    }

    embed.enrich_triples(triples, chr_spans_with_embeddings)

    assert triples[0].subject_embeds == [[[0]], [[0], [1]]]
    assert triples[0].relation_embeds == [[[0]]]
    assert triples[0].object_embeds == [[[0]]]

    assert triples[1].subject_embeds == [[[2], [3]]]
    assert triples[1].relation_embeds == [[[2], [3]]]
    assert triples[1].object_embeds == [[[2]], [[4]]]


    ####### TEST CASE 2 ########

    triples = [data_model.Triple("Jane 's mother", "leaves", "note")]

    triples[0].subject_words = [[0, 4], [4, 6], [7, 13]]
    triples[0].relation_words = [[15, 21]]
    triples[0].object_words = [[27, 31]]

    chr_spans_with_embeddings = {
        (0, 4) : [0],
        (4, 6) : [1],
        (6, 13) : [2],
        (13, 14) : [3],
        (14, 21) : [4],
        (21, 22) : [5],
        (22, 26) : [6],
        (26, 31) : [7],
        (31, 33) : [8]
    }

    embed.enrich_triples(triples, chr_spans_with_embeddings)

    assert triples[0].subject_embeds == [[[0]], [[1]], [[2]]]
    assert triples[0].relation_embeds == [[[4]]]
    assert triples[0].object_embeds == [[[7]]]

def test_add_embeddings_to_questions():
    
    #load question
    with open("test_files/question_without_embed.pkl", "rb") as f:
        q_list = pickle.load(f)[:1]

    assert q_list[0].question_with_answer_triples[1].object == 'note'

    #apply embed
    embed.add_embeddings_to_questions(q_list)

    assert q_list[0].question_with_answer_triples[1].object_embeds != [[]]

def test_add_embeddings_to_questions_helper():
    #load question
    with open("test_files/question_without_embed.pkl", "rb") as f:
        q = pickle.load(f)[0]

    assert q.question_with_answer_triples[1].object == 'note'

    #apply embed
    embed.add_embeddings_to_question_helper(q)

    assert q.question_with_answer_triples[1].object_embeds != [[]]

def test_embed():
    out = embed.embed('A bird in the tree is watching Han Mei and Lu Lu.')
    
    assert list(out.keys()) = 