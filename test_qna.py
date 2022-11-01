import qna

def test_evaluator():

    test_case_1 = [
        {
            "triple" : 0,
            "double" : 0,
            "single" : 0,
            "none" : 25,
            "option" : 0

        },
        {
            "triple" : 0,
            "double" : 0,
            "single" : 0,
            "none" : 0,
            "option" : 1
        },
        {
            "triple" : 0,
            "double" : 0,
            "single" : 0,
            "none" : 1,
            "option" : 2
        },
        {
            "triple" : 0,
            "double" : 0,
            "single" : 0,
            "none" : 310,
            "option" : 3
        },
    ]

    assert [False, "no_matches", -1] == qna.evaluator(test_case_1)

    test_case_2 = [
        {
            "triple" : 1,
            "double" : 0,
            "single" : 0,
            "none" : 25,
            "option" : 0
        },
        {
            "triple" : 1,
            "double" : 0,
            "single" : 0,
            "none" : 25,
            "option" : 1
        },
        {
            "triple" : 1,
            "double" : 0,
            "single" : 0,
            "none" : 25,
            "option" : 2
        },
        {
            "triple" : 1,
            "double" : 0,
            "single" : 0,
            "none" : 25,
            "option" : 3
        },
    ]

    assert [False, "all_equivalent", -1] == qna.evaluator(test_case_2)

    test_case_3 = [
        {
            "triple" : 5,
            "double" : 0,
            "single" : 0,
            "none" : 25,
            "option" : 0
        },
        {
            "triple" : 5,
            "double" : 0,
            "single" : 0,
            "none" : 25,
            "option" : 1
        },
        {
            "triple" : 2,
            "double" : 0,
            "single" : 0,
            "none" : 23,
            "option" : 2
        },
        {
            "triple" : 1,
            "double" : 0,
            "single" : 2323,
            "none" : 23,
            "option" : 3
        },
    ]

    assert [False, "draw", -1] == qna.evaluator(test_case_3)

    test_case_4 = [
        {
            "triple" : 5,
            "double" : 0,
            "single" : 0,
            "none" : 25,
            "option" : 0
        },
        {
            "triple" : 5,
            "double" : 0,
            "single" : 0,
            "none" : 25,
            "option" : 1
        },
        {
            "triple" : 10,
            "double" : 0,
            "single" : 0,
            "none" : 23,
            "option" : 2
        },
        {
            "triple" : 1,
            "double" : 0,
            "single" : 2323,
            "none" : 23,
            "option" : 3
        },
    ]

    assert [True, "triple", 2] == qna.evaluator(test_case_4)

    test_case_5 = [
        {
            "triple" : 5,
            "double" : 0,
            "single" : 0,
            "none" : 25,
            "option" : 0
        },
        {
            "triple" : 5,
            "double" : 0,
            "single" : 0,
            "none" : 25,
            "option" : 1
        },
        {
            "triple" : 5,
            "double" : 0,
            "single" : 0,
            "none" : 23,
            "option" : 2
        },
        {
            "triple" : 5,
            "double" : 1,
            "single" : 2323,
            "none" : 23,
            "option" : 3
        },
    ]

    assert [True, "double", 3] == qna.evaluator(test_case_5)

    test_case_6 = [
        {
            "triple" : 5,
            "double" : 1,
            "single" : 1212121,
            "none" : 25243242432432,
            "option" : 0
        },
        {
            "triple" : 5,
            "double" : 1,
            "single" : 0,
            "none" : 25,
            "option" : 1
        },
        {
            "triple" : 5,
            "double" : 1,
            "single" : 1212120,
            "none" : 232432434224234,
            "option" : 2
        },
        {
            "triple" : 5,
            "double" : 1,
            "single" : 2323,
            "none" : 23,
            "option" : 3
        },
    ]

    assert [True, "single", 0] == qna.evaluator(test_case_6)