#!/usr/bin/python
"""
Filename: tournament.py
Authors: Yoshi Fu
Project: Probability Calculations for Tournament Settings
Date: March 2025

Summary:
Compute the odds of a certain event happening in a tournament bracket.
"""


from dataclasses import dataclass
from enum import StrEnum, auto
from math import prod
from typing import Any, Callable, Generator, Iterable, List, Optional, Tuple


class Region(StrEnum):
    """StrEnum with the different regions in League of Legends pro play."""

    LEC = auto()
    LCS = auto()
    LCK = auto()
    LPL = auto()
    OTHER = auto()


@dataclass(frozen=True)
class Team:
    """Class representing a team in League of Legends."""

    region: Region = Region.OTHER
    tag: str = ""
    full_name: str = ""

    def __str__(self) -> str:
        return self.tag


# LCK Teams. cSpell: disable
BRO: Team = Team(Region.LCK, "BRO", "BRION")
DK: Team = Team(Region.LCK, "DK ", "Dplus Kia")
DRX: Team = Team(Region.LCK, "DRX", "DRX")
FX: Team = Team(Region.LCK, "FX ", "FEARX")
DNF: Team = Team(Region.LCK, "DNF", "Freecs")
GEN: Team = Team(Region.LCK, "GEN", "Gen.G Esports")
HLE: Team = Team(Region.LCK, "HLE", "Hanwha Life Esports")
KT: Team = Team(Region.LCK, "KT ", "KT Rolster")
NS: Team = Team(Region.LCK, "NS ", "Nongshim RedForce")
T1: Team = Team(Region.LCK, "T1 ", "T1")

# LEC Teams.
BDS: Team = Team(Region.LEC, "BDS", "Team BDS")
FNC: Team = Team(Region.LEC, "FNC", "Fnatic")
G2: Team = Team(Region.LEC, "G2 ", "G2 Esports")
GX: Team = Team(Region.LEC, "GX ", "GiantX")
HR: Team = Team(Region.LEC, "HR ", "Team Heretics")
KC: Team = Team(Region.LEC, "KC ", "Karmine Corp")
KOI: Team = Team(Region.LEC, "KOI", "KOI")
RGE: Team = Team(Region.LEC, "RGE", "Rogue")
SK: Team = Team(Region.LEC, "SK ", "SK Gaming")
VIT: Team = Team(Region.LEC, "VIT", "Team Vitality")

# LPL Teams.
AL: Team = Team(Region.LPL, "AL ", "Anyone's Legend")
BLG: Team = Team(Region.LPL, "BLG", "Bilibili Gaming")
EDG: Team = Team(Region.LPL, "EDG", "Edward Gaming")
FPX: Team = Team(Region.LPL, "FPX", "FunPlus Phoenix")
IG: Team = Team(Region.LPL, "IG ", "Invictus Gaming")
JDG: Team = Team(Region.LPL, "JDG", "JD Gaming")
LNG: Team = Team(Region.LPL, "LNG", "LNG Esports")
NIP: Team = Team(Region.LPL, "NIP", "Ninjas in Pyjamas")
OMG: Team = Team(Region.LPL, "OMG", "Oh My God")
RNG: Team = Team(Region.LPL, "RNG", "Royal Never Give Up")
WE: Team = Team(Region.LPL, "WE ", "Team WE")
TOP: Team = Team(Region.LPL, "TOP ", "Top Esports")
WBG: Team = Team(Region.LPL, "WBG", "Weibo Gaming")

# LCS Teams. cSpell: enable
C9: Team = Team(Region.LCS, "C9 ", "Cloud9")
FLY: Team = Team(Region.LCS, "FLY", "FlyQuest")
DSG: Team = Team(Region.LCS, "DSG", "Disguised")
TL: Team = Team(Region.LCS, "TL ", "Team Liquid")


def choose_matchup(
    teams: List[Team], rules: List[Callable[[Team, Team], bool]]
) -> Generator[Tuple[List[Tuple[Team, Team]], List[Team]], None, None]:
    """Choose a matchup from a list of teams.

    Args:
        teams (List[Team]):
            List of teams in the bracket.
        rules (List[Callable[[Team, Team], bool]]):
            List of rules that all have to be satisfied.

    Yields:
        out (Generator[Tuple[List[Tuple[Team, Team]], List[Team]], None, None]):
            - A possible matchup
            - A list with the remaining teams.
    """
    team1: Team = teams[0]
    other_teams: List[Team] = teams[1:]
    for i, team2 in enumerate(other_teams):
        if all(rule(team1, team2) for rule in rules):
            yield [(team1, team2)], other_teams[:i] + other_teams[(i + 1) :]


def generate_brackets(
    teams: List[Team], rules: Optional[List[Callable[[Team, Team], bool]]] = None
) -> Generator[List[Tuple[Team, Team]], None, None]:
    """Generate all possible events that can form inside a bracket.

    Args:
        teams (List[Team]):
            List of teams in the bracket.
        rules (Optional[List[Callable[[Team, Team], bool]]], optional):
            List of rules that all have to be satisfied. Defaults to None.

    Yields:
        out (Generator[List[Tuple[Team, Team]], None, None]):
            A possible bracket given the list of teams.
    """
    if rules is None:
        rules = []

    match len(teams):
        case 0:  # There is no team left to match with.
            return
        case 1:  # Yield the only team left over.
            yield [(teams[0], Team())]
        case 2:  # If the only matchup is valid, yield it.
            if all(rule(teams[0], teams[1]) for rule in rules):
                yield [(teams[0], teams[1])]
        case _:  # Otherwise choose a matchup. Recursively repeat.
            for matchup, other_teams in choose_matchup(teams, rules):
                for other_matchup in generate_brackets(other_teams, rules):
                    yield matchup + other_matchup


def diff_region(a: Team, b: Team) -> bool:
    """Check if the region of two teams is different

    Args:
        a (Team): Team A
        b (Team): Team B

    Returns:
        bool: True if the regions are different, False otherwise.
    """
    return a.region != b.region


def invalid_matchup(a: Team, b: Team) -> Callable[[Team, Team], bool]:
    """Create and return a function that takes two teams and returns True when
    given two teams that are not a and b.

    Args:
        a (Team): Team A
        b (Team): Team B

    Returns:
        out (Callable[[Team, Team], bool]):
            Function that returns True if it does not see a and b again, False otherwise.
    """
    return lambda x, y: not ((x == a and y == b) or (x == b and y == a))


def prod_odd_to(n: int) -> int:
    """Get the product of all odd numbers up to n.

    Args:
        n (int): Upper limit of the odd numbers to multiply.

    Returns:
        int: Product of all odd numbers up to n.
    """
    return prod(i for i in range(1, n, 2))


def bracket_has_event(
    bracket: List[Tuple[Team, Team]], event: Tuple[Team, Team]
) -> bool:
    """Check if an event is inside a bracket.

    Args:
        bracket (List[Tuple[Team, Team]]):
            Bracket to check in.
        event (Tuple[Team, Team]):
            Event to find.

    Returns:
        bool: True if bracket contains the event, False otherwise.
    """
    a: Team
    b: Team
    a, b = event
    return (a, b) in bracket or (b, a) in bracket


def brute_force(
    teams: List[Team],
    events: Optional[List[Tuple[Team, Team]]] = None,
    rules: Optional[List[Callable[[Team, Team], bool]]] = None,
    use_any: bool = False,
    debug: bool = False,
) -> Tuple[int, int]:
    """Compute the odds of specific events occurring within a bracket by
    iterating over all the possible brackets given a list of teams.

    Args:
        teams (List[Team]):
            List of teams in the bracket.
        events (Optional[List[Tuple[Team, Team]]]):
            List of specific events that we want to see. Defaults to None.
        rules (Optional[List[Callable[[Team, Team], bool]]], optional):
            List of rules that all have to be satisfied. Defaults to None.
        use_any (bool, optional):
            Flag to specify if all or any events have to be satisfied. Defaults to False.
        debug (bool, optional):
            Flag to specify if brackets should be printed. Defaults to False.
    Returns:
        out (Tuple[int, int]):
            - The number of times all events were satisfied.
            - The number of brackets that satisfy the rules.
    """
    if events is None:
        events = []
    if rules is None:
        rules = []
    func: Callable[[Iterable], bool] = any if use_any else all

    # Iterate over all brackets that satisfy rules.
    total: int = 0
    satisfies: int = 0
    msg_str: List[str] = ["All brackets that satisfy the rules:"]
    for bracket in generate_brackets(teams, rules):
        total += 1

        line: str = f"[{", ".join([f"{a} vs {b}" for a, b in bracket])}]"

        # Check if a bracket satisfies all events.
        if func(bracket_has_event(bracket, event) for event in events):
            satisfies += 1

            line += " <-"

        msg_str.append(line)

    # Print all the brackets with an arrow for the ones that satisfy all events.
    if debug:
        print("\n".join(msg_str))

    return satisfies, total


def print_odds(
    description: str,
    algorithm: Callable[
        [
            List[Team],
            List[Tuple[Team, Team]],
            List[Callable[[Team, Team], bool]],
            bool,
            bool,
        ],
        Tuple[int, int],
    ],
    *args: Any,
    **kwargs: Any,
) -> None:
    """Print the odds of certain events occurring within a bracket.

    Args:
        Description (str):
            Description of the conditions.
        Algorithm (Callable[ [teams, events, rules, debug], Tuple[int, int] ]):
            Algorithm to use.
        *args (Any):
            Positional arguments for the algorithm.
        **kwargs (Any):
            Keyword arguments for the algorithm.
    """
    numerator: int
    denominator: int

    numerator, denominator = algorithm(*args, **kwargs)
    print(f"{description}: {numerator}/{denominator}\n")


def test_brute_force() -> None:
    """Test the accuracy of the brute_force() function."""
    teams: List[Team]
    events: List[Tuple[Team, Team]]
    rules: List[Callable[[Team, Team], bool]]

    teams = [T1, GEN, HLE, DK, G2, FNC, BLG, FLY]
    events = [(T1, G2)]
    rules = []
    assert brute_force(teams, events=events, rules=rules, debug=False) == (15, 105)

    rules = [diff_region]
    assert brute_force(teams, events=events, rules=rules, debug=False) == (6, 24)

    rules = [
        invalid_matchup(T1, GEN),
        invalid_matchup(T1, HLE),
        invalid_matchup(T1, DK),
        invalid_matchup(GEN, HLE),
        invalid_matchup(GEN, DK),
        invalid_matchup(HLE, DK),
        invalid_matchup(FNC, G2),
    ]
    assert brute_force(teams, events=events, rules=rules, debug=False) == (6, 24)

    events = [(T1, G2)]
    rules = [invalid_matchup(T1, G2)]
    assert brute_force(teams, events=events, rules=rules, debug=False) == (0, 90)

    events = [(T1, GEN), (HLE, G2)]
    assert brute_force(teams, events=events, rules=rules, debug=False) == (3, 90)

    teams = [GEN, DK, G2, FNC, BLG, FLY]
    events = []
    rules = [diff_region]
    assert brute_force(teams, events=events, rules=rules, debug=False) == (10, 10)

    teams = [GEN, HLE, DK, FNC, BLG, FLY]
    assert brute_force(teams, events=events, rules=rules, debug=False) == (6, 6)


def main() -> None:
    """Main function."""
    test_brute_force()

    # Example usage.
    print_odds(
        "Odds for T1 vs G2 when there are no same region matches",
        brute_force,
        teams=[T1, GEN, HLE, DK, G2, FNC, BLG, FLY],
        events=[(T1, G2)],
        rules=[diff_region],
        debug=False,
    )

    print_odds(
        "Odds for DK vs FNC or DK vs FLY occurring when there are no same region matches",
        brute_force,
        teams=[T1, GEN, HLE, DK, G2, FNC, BLG, FLY],
        events=[(DK, FNC), (DK, FLY)],
        rules=[diff_region],
        use_any=True,
        debug=True,
    )


if __name__ == "__main__":
    main()
