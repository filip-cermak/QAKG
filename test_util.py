import util
import data_model

def test_intersect():

    a = ["a", "b", "c", "d"]
    b = ["b", "c"]

    difference = set(util.intersect(a,b)) ^ set(["b", "c"])
    assert not difference

def test_intersect_len():

    a = ["a", "b", "c", "d"]
    b = ["b", "c"]

    assert util.intersect_len(a,b) == 2 

    a = ["a", "b", "c", "d"]
    b = ["b", "c", "d", "e", "f"]

    assert util.intersect_len(a,b) == 3

def test_compare_helper():

    a = ["a", "b", "c", "d"]
    b = ["b", "c"]

    assert util.compare_helper(a, b) == [0, 1, 1, 0]

def test_summarize_dict():

    input_dict = {1: [1,2,3], 2: [1], 3: [], 4: [1,2,3,4,5]}
    expected_dict = {1:3, 2:1, 3:0, 4:5}

    assert util.summarize_dict(input_dict) == expected_dict

def test_answer_joiner():

    assert util.question_answer_joiner("The oldest one is _.", "Peter") == "The oldest one is Peter."
    assert util.question_answer_joiner("Test question:", "Test answer") == "Test question: Test answer"
    assert util.question_answer_joiner("Test _, _", "Answer") == "Test _, _ Answer"

def test_merge_dicts():
    assert util.merge_dicts({"a" : 1, "b" : 23, "c" : 98}, {"a" : 2, "b" : -2, "c": 7}) == {"a" : 3, "b" : 21, "c" : 105}

def test_new_line_symbol_remover():
    assert util.new_line_symbol_remover("This is a test,\nhow about you") == "This is a test, how about you"
    assert util.new_line_symbol_remover("This \n, \n, hey") == "This  ,  , hey" 
    
def test_content_triple_filter():

    # Test case 1
    triple_list = [
        data_model.Triple("cat", "sat on", "mat"),
        data_model.Triple("dog", "is a sat", "mat"), #does not match is because too short
        data_model.Triple("animals", "such as", "cat and dog"),
        data_model.Triple("animals", "being social", "cat and dog"),
    ]

    text = "Cat is a very social animal"
    out = triple_list

    del(out[1])

    assert util.content_triple_filter(triple_list, text) == out

def test_word_matcher():

    assert util.word_matcher("cat sat on a mat", "cat on a mat") == True
    assert util.word_matcher("at at ", "at") == False

def test_fuzzy_dict_simplifier():

    out = util.fuzzy_dict_simplifier(
        {
            "full" : 1, 
            "lp" : 2, 
            "rp" : 3, 
            "sp" : 4, 
            "o" : 5, 
            "r" : 6, 
            "s" : 7, 
            "" : 8
        },
        option = 1)

    assert out == {
        "triple" : 1,
        "double" : 9,
        "single" : 18,
        "none" : 8,
        "option" : 1
        }

    out = util.fuzzy_dict_simplifier(
        {
            "full" : 1, 
            "lp" : 2, 
            "rp" : 3, 
            "sp" : 4, 
            "o" : 5, 
            "r" : 6, 
            "s" : 7, 
            "" : 8
        })

    assert out == {
        "triple" : 1,
        "double" : 9,
        "single" : 18,
        "none" : 8
        }