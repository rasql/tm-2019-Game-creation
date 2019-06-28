from platformer import *

map_str = """
0000002
0203000
1111113
"""

m = Map(map_str)

def test_map_dim():
    assert m.n == 3
    assert m.m == 7

def test_map_item():
    assert m.table[0][0] == 0
    assert m.table[2][0] == 1
    assert m.table[2][6] == 3
    assert m.table[0][6] == 2

def test_get_block():
    assert m.get_tile(20, 20) == 0
    assert m.get_tile(20, 100) == 1
    assert m.get_tile(270, 100) == 3
    
    
def test_get_index():
    assert m.get_index(50, 50) == (1, 1)
    assert m.get_index(1, 1) == (0, 0)
    assert m.get_index(0, 40) == (1, 0)

def test_get_rect():
    assert m.get_rect(0, 0) == Rect(0, 0, 40, 40)
    assert m.get_rect(1, 1) == Rect(40, 40, 40, 40)