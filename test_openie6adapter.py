import openie6adapter
import os
import data_model

def test_sentences2txt():
    """Not a proper unit test"""
    openie6adapter.sentences2txt(["test.", "test.", "test.", "test."], folder="test_files")
    os.remove("test_files/sentences.txt")

def test_question2sentences():
    """Not a proper unit test"""
    q = data_model.Question("_ is the tallest.", "Peter", ["Adam", "Martin"], "This is a long text, you should know this. Hello! Are you coming?", "1")

    #print(openie6adapter.question2sentences(q))

def test_q_list2sentences():
    """Not a proper unit test"""
    q_a = data_model.Question("_ is the tallest.", "Peter", ["Adam", "Martin"], "This is a long text, you should know this. Hello! Are you coming?", "1")
    q_b = data_model.Question("_ is the tallest.", "Peter", ["Adam", "Martin"], "This is a long text, you should know this. Hello! Are you coming?", "1")

    #print(openie6adapter.q_list2sentences([q_a, q_b]))