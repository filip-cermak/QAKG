import embed
import data_model

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

    
