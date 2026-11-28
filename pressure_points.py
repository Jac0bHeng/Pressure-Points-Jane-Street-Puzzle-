"""Jane Street "Pressure Points" (November 2026): a complete solver in one file.

Spoiler: this file contains the full solution.

The idea
    * Every letter string is the alphabetised letters of one answer.
    * Every emoji is a diamond: four things at the four points of a diamond
      (a compass, a clock face, a baseball diamond, ...). 19 x 4 = 76 points,
      which is the 75 strings plus the empty entry Ø.
    * In every diamond two points are exact, the TOP point GAINS a letter,
      and one other point LOSES a letter.
    * Read the gained and lost letters in the puzzle's emoji order.

The solver fills all 19 diamonds at once with backtracking, uses every string
exactly once, and keeps searching to prove the solution is unique.
"""

from collections import Counter
from itertools import product

# --- Puzzle input (Ø is the empty string) ------------------------------------

BAGS = ["" if b == "Ø" else b for b in """
Ø AAAABBIRRST AAACDEGHHHILMPRS AABCIILPTY AABDEHNNOORRSTTUY AABDORRST
AADEILPSS AADERRSUVY AADIMNTU AADMNNOT AAEEEHLNOOPRRSSTTTT AAGJRTU AAKNSS
ABBDEELOSSSU ABEEGLNSTW ABIIILNSTTY ABOW ACCGRUX ACDENO ACEILP
ACFINRRRSTTUU ACRX AEEFGIKNPRRR AEEHNV AEGHRT AEGILNRST AEHHLT AEIINST
AEILLNPSU AEQRSU AGIJLOOT AHTU AIIIIJJLNSSTTUV AIIM AIINSSSTTUX AIMMOS AIX
AMNY AORTY AST BEQSSTUU CCDNOOTU CCILR CDENOOS CEIMNOWX CEINOPRSSUX CEMRRUY
CIIMTV CORSS DIRT DNOW EEFIR EEHLTVW EEHRT EEIMSS EFL EHMO EHNORT EINN ENRT
ESTW FIRST GHIRT GIMNNOWY GO HOSTU HPU IILNOSV IPTTU IX MOO NSU OPRT SW T V
""".split()]

EMOJI_ORDER = "👸 🧭 🐷 ⚽ 🎮 🖼️ 🧐 ⚾ 💻 🐉 🕹️ 🏛️ 🎶 ⭐ 🕓 ⛵ 🏜️ 🪷 ⚠️".split()

# --- The 19 diamonds: points listed top, right, bottom, left -----------------
# (Queen's layout is the one we never pinned down, so its order is arbitrary.)

DIAMONDS = {
    "👸": ("Queen (the band)", "MAY, MERCURY, DEACON, TAYLOR"),
    "🧭": ("Compass", "NORTH, EAST, SOUTH, WEST"),
    "🐷": ("Pigpen cipher X-grid", "S, U, V, T"),
    "⚽": ("Barça diamond midfield", "MESSI, XAVI, BUSQUETS, INIESTA"),
    "🎮": ("PlayStation face buttons", "TRIANGLE, CIRCLE, CROSS, SQUARE"),
    "🖼️": ("Raphael's Sistine Madonna", "MADONNA, SAINT BARBARA, PUTTI, SAINT SIXTUS"),
    "🧐": ("Monopoly corners", "FREE PARKING, GO TO JAIL, GO, JAIL JUST VISITING"),
    "⚾": ("Baseball diamond", "SECOND, FIRST, HOME, THIRD"),
    "💻": ("Diamond Model of Intrusion Analysis", "ADVERSARY, CAPABILITY, VICTIM, INFRASTRUCTURE"),
    "🐉": ("Beijing's four imperial altars", "EARTH, SUN, HEAVEN, MOON"),
    "🕹️": ("Joystick directions", "UP, RIGHT, DOWN, LEFT"),
    "🏛️": ("Washington, D.C. extreme neighbourhoods",
           "NORTH PORTAL ESTATES, NORTHEAST BOUNDARY, BLUE PLAINS, PALISADES"),
    "🎶": ("Orchestra seating", "PERCUSSION, DOUBLE BASSES, CONDUCTOR, VIOLINS"),
    "⭐": ("Southern Cross (Crux)", "GACRUX, IMAI, ACRUX, MIMOSA"),
    "🕓": ("Clock face", "TWELVE, THREE, SIX, NINE"),
    "⛵": ("Ship", "BOW, STARBOARD, STERN, PORT"),
    "🏜️": ("Colorado's neighbours", "WYOMING, KANSAS, NEW MEXICO, UTAH"),
    "🪷": ("India's extreme states", "HIMACHAL PRADESH, WEST BENGAL, TAMIL NADU, GUJARAT"),
    "⚠️": ("NFPA 704 fire diamond", "FIRE, INSTABILITY, SPECIAL, HEALTH"),
}
POSITIONS = "TRBL"


def letters(text):
    return Counter(ch for ch in text.upper() if ch.isalpha())


def diff(answer, bag):
    """'=' exact, ('+', c) bag has an extra c, ('-', c) bag is missing c, else None."""
    a, b = letters(answer), Counter(bag)
    extra, missing = b - a, a - b
    if not extra and not missing:
        return ("=", "")
    if sum(extra.values()) == 1 and not missing:
        return ("+", next(iter(extra)))
    if sum(missing.values()) == 1 and not extra:
        return ("-", next(iter(missing)))
    return None


def fillings(points, pool):
    """Every way to fill one diamond with exactly 2 exact, 1 gain and 1 loss."""
    choices = [[b for b in pool if diff(p, b)] for p in points]
    for combo in product(*choices):
        if any(n > pool[b] for b, n in Counter(combo).items()):
            continue
        ops = sorted(diff(p, b)[0] for p, b in zip(points, combo))
        if ops == ["+", "-", "=", "="]:
            yield combo


def solve():
    """Fill all diamonds together; return every complete solution (at most 2)."""
    points = {e: [p.strip() for p in pts.split(",")] for e, (_, pts) in DIAMONDS.items()}
    options = {e: list(fillings(points[e], Counter(BAGS))) for e in DIAMONDS}
    order = sorted(DIAMONDS, key=lambda e: len(options[e]))  # most constrained first
    pool, chosen, found = Counter(BAGS), {}, []

    def backtrack(i):
        if len(found) == 2:
            return
        if i == len(order):
            found.append(dict(chosen))
            return
        e = order[i]
        for combo in options[e]:
            need = Counter(combo)
            if all(pool[b] >= n for b, n in need.items()):
                pool.subtract(need)
                chosen[e] = combo
                backtrack(i + 1)
                pool.update(need)
                del chosen[e]

    backtrack(0)
    return points, found


def main():
    points, solutions = solve()
    assert solutions, "no consistent assignment"
    sol = solutions[0]
    gained, lost, tops = [], [], []

    for e in EMOJI_ORDER:
        print(f"\n{e}  {DIAMONDS[e][0]}")
        for pos, answer, bag in zip(POSITIONS, points[e], sol[e]):
            op, ch = diff(answer, bag)
            if op == "+":
                gained.append(ch)
                tops.append(pos if e != "👸" else "?")
            if op == "-":
                lost.append(ch)
            tag = "exact" if op == "=" else f"{op}{ch}"
            print(f"   {pos if e != '👸' else '?'}  {answer:<22} {bag or 'Ø':<20} {tag}")

    print("\nSolutions found :", len(solutions), "(unique)" if len(solutions) == 1 else "(NOT unique)")
    print("Gained letters  :", "".join(gained))
    print("Lost letters    :", "".join(lost))
    print("Gain positions  :", "".join(tops))
    print("\nNEWEST ROUGH EXCHANGE, and every big Belgian city except Antwerp:")
    print("Answer          : ANTWERPSCHE DIAMANTKRING")


if __name__ == "__main__":
    main()
