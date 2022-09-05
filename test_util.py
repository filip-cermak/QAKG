import util

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