from collections import Counter

from pressure_points.diamonds import DIAMONDS
from pressure_points.letters import EXACT, GAIN, LOSS, diff, key
from pressure_points.puzzle import BAGS, EMOJI_ORDER
from pressure_points.search import check_theme
from pressure_points.solver import extract, gain_positions, solve


def test_input_shape():
    assert len(BAGS) == 76
    assert len(EMOJI_ORDER) == len(DIAMONDS) == 19
    assert sum(len(points) for _, points in DIAMONDS.values()) == 76


def test_diff():
    assert key("Saint Sixtus") == "AIINSSSTTUX"
    assert diff("SAINT SIXTUS", "AIINSSSTTUX") == (EXACT, "")
    assert diff("NORTH", "EHNORT") == (GAIN, "E")
    assert diff("EAST", "AST") == (LOSS, "E")
    assert diff("U", "") == (LOSS, "U")
    assert diff("NORTH", "AST") is None


def test_unique_solution_uses_every_bag():
    solutions = solve(max_solutions=2)
    assert len(solutions) == 1
    used = Counter(p.bag for group in solutions[0].values() for p in group)
    assert used == Counter(BAGS)


def test_every_diamond_has_two_exact_one_gain_one_loss():
    sol = solve()[0]
    for emoji, group in sol.items():
        assert sorted(p.op for p in group) == sorted([EXACT, EXACT, GAIN, LOSS]), emoji


def test_extraction():
    gained, lost = extract(solve()[0])
    assert gained == "NEWESTROUGHEXCHANGE"
    assert lost == "LEUVENGHENTBRUSSELS"


def test_gained_letter_is_always_on_top():
    positions = gain_positions(solve()[0])
    assert set(positions) <= {"T", "?"}


def test_check_theme():
    fits = check_theme(["GACRUX", "PLEIADES"])
    assert fits["GACRUX"] == [("ACCGRUX", GAIN, "C")]
    assert fits["PLEIADES"] == []
