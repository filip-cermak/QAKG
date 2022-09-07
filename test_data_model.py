import data_model

def test_triple():

    # match()
    a = data_model.Triple("a", "b", "c")
    b = data_model.Triple("a", "b", "c")

    assert a.match(b) == "full"
    assert b.match(a) == "full"

    c = data_model.Triple("a", "b", "x")

    assert a.match(c) == "lp"
    assert c.match(a) == "lp"

    d = data_model.Triple("x", "b", "c")

    assert a.match(d) == "rp"
    assert d.match(a) == "rp"

    e = data_model.Triple("a", "x", "c")

    assert a.match(e) == "sp"
    assert e.match(a) == "sp"

    f = data_model.Triple("x", "x", "c")

    assert a.match(f) == "o"
    assert f.match(a) == "o"

    g = data_model.Triple("x", "b", "x")

    assert a.match(g) == "r"
    assert g.match(a) == "r"

    h = data_model.Triple("a", "x", "x")

    assert a.match(h) == "s"
    assert h.match(a) == "s"

    i = data_model.Triple("x", "x", "x")

    assert a.match(i) == ""
    assert i.match(a) == ""
    ###################################

def test_eval():
    in_q = data_model.Question(
        "placeholder",
        "placeholder",
        "placeholder",
        "placeholder",
        "placeholder"
    ) 

    in_q.context_triples = [
        data_model.Triple("a", "b", "c"),
        data_model.Triple("c", "d", "e"),
        data_model.Triple("x", "y", "z"),
    ]

    in_q.question_with_answer_triples = [
        data_model.Triple("a", "b", "c"), # full
        data_model.Triple("a", "b", "#"), # lp
        data_model.Triple("x", "y", "#"), # lp
        data_model.Triple("#", "b", "#"), # r
        data_model.Triple("x", "y", "z"), # full
    ] 

    in_q.question_with_distractors_triples = [
        [
            data_model.Triple("#", "#", "#"), # ""
            data_model.Triple("#", "#", "e"), # "o"
            data_model.Triple("x", "#", "#"), # "s"
        ],
        [data_model.Triple("#", "d", "e")], # rp
        [data_model.Triple("x", "#", "z")], # sp
    ]

    e = data_model.Eval(in_q)

    assert e.correct_answer_matches_summary == {
        '': 0, 
        'full': 2,
        'rp': 0, 
        'sp': 0, 
        'o': 0, 
        's': 0, 
        'r': 1, 
        'lp': 2
        }

    assert e.distractors_matches_summary == [
        {
        '': 1, 
        'full': 0,
        'rp': 0, 
        'sp': 0, 
        'o': 1, 
        's': 1, 
        'r': 0, 
        'lp': 0
        },
        {
        '': 0, 
        'full': 0,
        'rp': 1, 
        'sp': 0, 
        'o': 0, 
        's': 0, 
        'r': 0, 
        'lp': 0
        },
        {
        '': 0, 
        'full': 0,
        'rp': 0, 
        'sp': 1, 
        'o': 0, 
        's': 0, 
        'r': 0, 
        'lp': 0
        },
    ]