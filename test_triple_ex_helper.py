import triple_ex_helper
import data_model

#Mock classes required for unit tests

class Dummy_extractor:
    def __init__(self, document):
        self.document = document
    def annotate(self, text):
        return self.document

class Document:
    def __init__(self, sentence):
        self.sentence = sentence #actually a list of sentences, did not name this

class Sentence:
    def __init__(self, token):
        self.token = token #actually a list of tokens, did not name this
        self.tokenOffsetBegin = 0

class Sentence_token:
    def __init__(self, token_begin_index, token_end_index, begin_char, end_char):
        self.tokenBeginIndex = token_begin_index
        self.tokenEndIndex = token_end_index
        self.beginChar = begin_char 
        self.endChar = end_char 
        self.openieTriple = []

class Triple_token:
    def __init__(self, sentence_index, token_index):
        self.tokenIndex = token_index
        self.SentenceIndex = sentence_index

class Openie_triple:
    # mock of the triple which is extracted by client.annotate()
    def __init__(self, subject, relation, object, subject_tokens, relation_tokens, object_tokens):
        self.subject = subject
        self.relation = relation
        self.object = object
        self.subjectTokens = subject_tokens
        self.relationTokens = relation_tokens
        self.objectTokens = object_tokens
        self.confidence = 1

def test_extract_triples():

    """     try:
            out = triple_ex.extract_triples("Adam has a new car. Eve has a red bike. They are married!")
            triple_ex.terminate()

            print([t.semantic_triple() for t in out])
        except:
            triple_ex.terminate()
    assert False
    """
    pass

def test_tokens2loc():
    triple = data_model.Triple("Adam", "has", "new car")
    triple.subject_tokens = [Triple_token(0, 0)]
    triple.relation_tokens = [Triple_token(0, 1)]
    triple.object_tokens = [Triple_token(0, 3), Triple_token(0, 4)]

    i = 0 

    sentence = Sentence([
        Sentence_token(0, 1, 0, 4), #Adam
        Sentence_token(1, 2, 5, 8), #has
        Sentence_token(2, 3, 9, 10), #a
        Sentence_token(3, 4, 11, 14), #new
        Sentence_token(4, 5, 15, 18), #car
        Sentence_token(5, 6, 18, 19) #.
        ])
    
    triple = triple_ex_helper.tokens2loc(triple, i, sentence)

    assert triple.semantic_triple() == [[[0, 4]], [[5, 8]], [[11, 14],[15, 18]]]

    triple = data_model.Triple("Adam", "has", "car")
    triple.subject_tokens = [Triple_token(0, 0)]
    triple.relation_tokens = [Triple_token(0, 1)]
    triple.object_tokens = [Triple_token(0, 4)]

    triple = triple_ex_helper.tokens2loc(triple, i, sentence)

    assert triple.semantic_triple() == [[[0, 4]], [[5, 8]], [[15, 18]]]

def test_extract_triples_helper():

    sentences = [
        Sentence([
            Sentence_token(0, 1, 0, 4), #Adam
            Sentence_token(1, 2, 5, 8), #has
            Sentence_token(2, 3, 9, 10), #a
            Sentence_token(3, 4, 11, 14), #new
            Sentence_token(4, 5, 15, 18), #car
            Sentence_token(5, 6, 18, 19) #.
        ]),
        Sentence([
            Sentence_token(6,7, 20, 23), #Eve
            Sentence_token(7,8, 24, 27), #has
            Sentence_token(8,9, 28, 29), #a
            Sentence_token(9,10, 30, 33), #red
            Sentence_token(10,11, 34, 38), #bike
            Sentence_token(11,12, 38, 39) #.
        ])
    ]

    triple_a = Openie_triple("Adam", "has", "car", 
        [Triple_token(0, 0)],
        [Triple_token(0, 1)],
        [Triple_token(0, 4)])

    triple_b = Openie_triple("Eve", "has", "red bike",
        [Triple_token(1, 0)],
        [Triple_token(1, 1)],
        [Triple_token(1, 3), Triple_token(1, 4)])

    #set OpenIE triples
    sentences[1].tokenOffsetBegin = 6
    sentences[0].openieTriple = [triple_a]
    sentences[1].openieTriple = [triple_b]

    document = Document(sentences)
    client = Dummy_extractor(document)
    triples = triple_ex_helper.extract_triples_helper("Placeholder text", client)

    assert len(triples) == 2
    assert triples[0].semantic_triple() == [[[0, 4]], [[5, 8]], [[15, 18]]]
    assert triples[1].semantic_triple() == [[[20, 23]], [[24, 27]], [[30, 33],[34, 38]]]