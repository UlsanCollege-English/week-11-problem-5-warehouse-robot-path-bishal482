import pytest
from hw05.main import parse_grid, grid_shortest_path

def test_parse_finds_start_and_target():
    lines = [
        "S..",
        ".#.",
        "..T",
    ]
    g, s, t = parse_grid(lines)
    assert s == "0,0" and t == "2,2"
    assert "0,1" in g["0,0"]  # right neighbor
    assert "1,0" in g["0,0"]  # down neighbor
    assert "1,1" not in g  # blocked

def test_basic_path():
    lines = [
        "S..",
        ".#.",
        "..T",
    ]
    p = grid_shortest_path(lines)
    assert p[0] == "0,0" and p[-1] == "2,2"
    assert len(p) in (5, 5)  # fixed length for this layout

def test_unreachable_returns_none():
    lines = [
        "S#T",
    ]
    assert grid_shortest_path(lines) is None

def test_start_equals_target():
    lines = ["ST"]
    p = grid_shortest_path(lines)
    assert p == ['0,0', '0,1']

@pytest.mark.parametrize("grid, length", [
    (["S.T"], 3),
    (["S..T"], 4),
    (["S...T"], 5),
])
def test_straight_line_lengths(grid, length):
    assert len(grid_shortest_path(grid)) == length

def test_larger_maze():
    lines = [
        "S....",
        "##.#.",
        "...#T",
        ".#.##",
        ".....",
    ]
    p = grid_shortest_path(lines)
    assert p[0] == "0,0" and p[-1] == "2,4"
    # ensure all cells are open
    for cell in p:
        r, c = map(int, cell.split(','))
        assert lines[r][c] != '#'

def test_no_diagonals():
    lines = [
        "S#.",
        ".T.",
        "..."
    ]
    # diagonal S->T is blocked; must route around
    p = grid_shortest_path(lines)
    assert len(p) >= 3
