# Pressure Points Solver

A Python solver for Jane Street's November 2026 puzzle, [Pressure Points](https://www.janestreet.com/puzzles/pressure-points-index/).

> **Spoiler warning:** this repo contains the full solution and answer.

## The puzzle

The puzzle page has no instructions. It shows only:

- an empty entry, `Ø`
- 75 strings of alphabetised letters, such as `AAKNSS`, `EHNORT` and `AAEEEHLNOOPRRSSTTTT`
- 19 emojis: 👸 🧭 🐷 ⚽ 🎮 🖼️ 🧐 ⚾ 💻 🐉 🕹️ 🏛️ 🎶 ⭐ 🕓 ⛵ 🏜️ 🪷 ⚠️
- the answer length, `(11 12)`

The page's URL ends in `pressure-points-index`, and the layout really is a sorted index. So the order on the page tells you nothing about how the entries group together.

## How it works

**1. Each string is a sorted "bag" of letters.**
`AAKNSS` is KANSAS. `HOSTU` is SOUTH. Most bags decode directly, but many are off by one letter. `EHNORT` is NORTH with an extra E, and `AST` is EAST missing an E.

**2. Each emoji is a diamond of four things.**
19 emojis × 4 points = 76, which is the 75 bags plus `Ø`. Every group is four things that sit at the four points of a diamond: a compass, a clock face, a baseball diamond, the PlayStation buttons, and so on. That's the "points" in the title.

**3. Every diamond follows the same rule.**
Two points are exact. One point **gains** a letter, and that point is always at the top of the diamond. One point **loses** a letter.

**4. Read the letters in emoji order.**

| | Letters |
|---|---|
| Gained | N E W E S T · R O U G H · E X C H A N G E |
| Lost | L E U V E N · G H E N T · B R U S S E L S |

"Newest rough exchange", with Leuven, Ghent and Brussels all named, which leaves out Belgium's other big city: Antwerp. The newest of Antwerp's four diamond bourses is the one dedicated to rough diamonds. And diamonds form under pressure.

**Answer: ANTWERPSCHE DIAMANTKRING** (11 12)

## The 19 diamonds

| Emoji | Diamond | Gains (top) | Loses |
|---|---|---|---|
| 👸 | Queen: Mercury, May, Taylor, Deacon | MAY +N | TAYLOR −L |
| 🧭 | Compass | NORTH +E | EAST −E |
| 🐷 | The X in the pigpen cipher: S, T, U, V | S +W | U −U (`Ø`) |
| ⚽ | Barça diamond midfield | MESSI +E | XAVI −V |
| 🎮 | PlayStation face buttons | TRIANGLE +S | CIRCLE −E |
| 🖼️ | Raphael's *Sistine Madonna* | MADONNA +T | SAINT BARBARA −N |
| 🧐 | Monopoly corners | FREE PARKING +R | JAIL / JUST VISITING −G |
| ⚾ | Baseball diamond | SECOND +O | THIRD −H |
| 💻 | Diamond Model of Intrusion Analysis | ADVERSARY +U | INFRASTRUCTURE −E |
| 🐉 | Beijing's four imperial altars | EARTH +G | MOON −N |
| 🕹️ | Joystick directions | UP +H | LEFT −T |
| 🏛️ | Washington, D.C.'s extreme neighbourhoods | NORTH PORTAL ESTATES +E | BLUE PLAINS −B |
| 🎶 | Orchestra seating | PERCUSSION +X | CONDUCTOR −R |
| ⭐ | Southern Cross | GACRUX +C | ACRUX −U |
| 🕓 | Clock face | TWELVE +H | SIX −S |
| ⛵ | Ship | BOW +A | STERN −S |
| 🏜️ | Colorado's neighbours | WYOMING +N | NEW MEXICO −E |
| 🪷 | India's extreme states | HIMACHAL PRADESH +G | TAMIL NADU −L |
| ⚠️ | NFPA 704 fire diamond | FIRE +E | SPECIAL −S |

## Usage

Requires Python 3.9+. The solver itself uses only the standard library. `wordfreq` is needed only for the `search` command.

```bash
pip install -r requirements.txt
```

**Solve the puzzle.** This assigns every bag, proves the assignment is unique and prints the extraction:

```bash
python -m pressure_points solve
```

**Test a theme.** This is the tool that actually cracked the hard groups. Guess a set, list its members, and see which bags they fit:

```bash
python -m pressure_points check "BLUE PLAINS" PALISADES PLEIADES
# BLUEPLAINS   AEILLNPSU (bag is missing B)
# PALISADES    AADEILPSS (exact)
# PLEIADES     no bag fits
```

**Search a bag** against a word list, allowing one letter gained or lost:

```bash
python -m pressure_points search AIIM ACRX
python -m pressure_points search AEILLNPSU --two-word
```

**Run the tests:**

```bash
python -m pytest
```

## How the solver works

- `letters.py`: `diff(word, bag)` decides whether a bag is an exact anagram of a word, has one extra letter, or is missing one.
- `diamonds.py`: the 19 diamonds, with each point's position (top, right, bottom, left).
- `solver.py`: for each diamond, lists every way to fill its four points that gives exactly *2 exact, 1 gain, 1 loss*. Then it backtracks across all 19 diamonds at once (most constrained first), so every bag is used exactly once. It searches for a second solution as well, to prove the first is unique.
- `search.py`: the discovery tools used while the groups were still unknown.

## What I learned

- **Brute force alone fails on the long bags.** Dictionary searches for `AAEEEHLNOOPRRSSTTTT` gave nonsense like "talent stratosphere". The real answers were proper names (SAINT SIXTUS, NORTH PORTAL ESTATES), and they only appeared once the theme was known.
- **Find the pattern first, then verify in code.** Spotting the diamond structure and the "2 exact, 1 gain, 1 loss" rule made every later guess checkable in seconds.
- **The counts are a constraint.** With 76 points and a fixed number of gains and losses, the leftover bags told us what kind of answer each remaining slot needed.
- **The title is the biggest hint.** Pressure Points: points of a diamond, and diamonds formed under pressure.

## Credits

Puzzle by [Jane Street](https://www.janestreet.com/puzzles/). Solved by Jacky Chow, working with Claude.

## License

MIT
