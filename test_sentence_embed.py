import sentence_embed 


def test_sentence_mebed():
    assert sentence_embed.sentence_embed("My name is Filip.").shape == (384,)
