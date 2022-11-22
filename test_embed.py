import embed

def test_contains_chr_spn():

    assert embed.contains_chr_spn((1, 3), (1, 3)) == True
    assert embed.contains_chr_spn((1, 3), (1, 2)) == True
    assert embed.contains_chr_spn((1, 3), (0, 3)) == True 
    assert embed.contains_chr_spn((1, 3), (2, 3)) == True 
    assert embed.contains_chr_spn((5, 6), (6, 7)) == False
    assert embed.contains_chr_spn((5 , 8), (1 ,5)) == False

def test_chr_spn_matcher():
    assert embed.chr_spn_matcher((1,3), [(1,3), (1,2), (0,3), (3,4)]) == [(1,3), (1,2), (0,3)]
 