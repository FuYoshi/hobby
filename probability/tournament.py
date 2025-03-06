#!/usr/bin/python
"""
Filename: tournament.py
Authors: Yoshi Fu
Project: Probability Calculations for Tournament Settings
Date: March 2025

Summary:
TODO
"""


from dataclasses import dataclass
from enum import StrEnum, auto
from math import prod
from typing import Callable, Generator, List, Optional, Tuple

from probability import choose, permutation


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

    def __str__(self) -> str:
        return self.tag


T1: Team = Team(Region.LCK, "T1 ")
GEN: Team = Team(Region.LCK, "GEN")
HLE: Team = Team(Region.LCK, "HLE")
DK: Team = Team(Region.LCK, "DK ")
G2: Team = Team(Region.LEC, "G2 ")
FNC: Team = Team(Region.LEC, "FNC")
BLG: Team = Team(Region.LPL, "BLG")
FLY: Team = Team(Region.LCS, "FLY")


def choose_matchup(
    teams: List[Team], rules: List[Callable[[Team, Team], bool]]
) -> Generator[Tuple[List[Tuple[Team, Team]], List[Team]], None, None]:
    """Choose a matchup from a list of teams.

    Args:
        teams (List[Team]):
            list of teams in the bracket.
        rules (List[Callable[[Team, Team], bool]]):
            list of rules that all have to be satisfied.

    Yields:
        out (Generator[Tuple[List[Tuple[Team, Team]], List[Team]], None, None]):
            - a possible matchup
            - a list with the remaining teams.
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
            list of teams in the bracket.
        rules (Optional[List[Callable[[Team, Team], bool]]], optional):
            list of rules that all have to be satisfied. Defaults to None.

    Yields:
        out (Generator[List[Tuple[Team, Team]], None, None]):
            a possible bracket given the list of teams.
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
        a (Team): team a
        b (Team): team b

    Returns:
        bool: True if the regions are different, False otherwise.
    """
    return a.region != b.region


def invalid_matchup(a: Team, b: Team) -> Callable[[Team, Team], bool]:
    """Create and return a function that takes two teams and returns True when
    given two teams that are not a and b.

    Args:
        a (Team): team a
        b (Team): team b

    Returns:
        out (Callable[[Team, Team], bool]):
            function that returns True if it does not see a and b again, False otherwise.
    """
    return lambda x, y: not ((x == a and y == b) or (x == b and y == a))


def prod_odd_to(n: int) -> int:
    """Get the product of all odd numbers up to n.

    Args:
        n (int): upper limit of the odd numbers to multiply.

    Returns:
        int: product of all odd numbers up to n.
    """
    return prod(i for i in range(1, n, 2))


def bracket_has_event(
    bracket: List[Tuple[Team, Team]], event: Tuple[Team, Team]
) -> bool:
    """Check if an event is inside a bracket.

    Args:
        bracket (List[Tuple[Team, Team]]):
            bracket to check in.
        event (Tuple[Team, Team]):
            event to find.

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
    debug: bool = False,
) -> Tuple[int, int]:
    """Compute the odds of specific events occurring within a bracket by
    iterating over all the possible brackets given a list of teams.

    Args:
        teams (List[Team]):
            list of teams in the bracket.
        events (Optional[List[Tuple[Team, Team]]]):
            list of specific events that we want to see. Defaults to None.
        rules (Optional[List[Callable[[Team, Team], bool]]], optional):
            list of rules that all have to be satisfied. Defaults to None.
        debug (bool, optional):
            flag to specify if brackets should be printed. Defaults to False.
    Returns:
        out (Tuple[int, int]):
            - the number of times all events were satisfied.
            - the number of brackets that satisfy the rules.
    """
    if events is None:
        events = []
    if rules is None:
        rules = []

    # Iterate over all brackets that satisfy rules.
    total: int = 0
    satisfies: int = 0
    msg_str: List[str] = ["All brackets that satisfy the rules:"]
    for bracket in generate_brackets(teams, rules):
        total += 1

        line: str = f"[{", ".join([f"{a} vs {b}" for a, b in bracket])}]"

        # Check if a bracket satisfies all events.
        if all(bracket_has_event(bracket, event) for event in events):
            satisfies += 1

            line += " <-"

        msg_str.append(line)

    # Print all the brackets with an arrow for the ones that satisfy all events.
    if debug:
        print("\n".join(msg_str))

    return satisfies, total


def mathematics(
    teams: List[Team],
    events: Optional[List[Tuple[Team, Team]]] = None,
    rules: Optional[List[Callable[[Team, Team], bool]]] = None,
    debug: bool = False,
) -> Tuple[int, int]:
    """Compute the odds of specific events occurring within a bracket using
    mathematics.

    Args:
        teams (List[Team]):
            list of teams in the bracket.
        events (Optional[List[Tuple[Team, Team]]]):
            list of specific events that we want to see. Defaults to None.
        rules (Optional[List[Callable[[Team, Team], bool]]], optional):
            list of rules that all have to be satisfied. Defaults to None.
        debug (bool, optional):
            flag to specify if brackets should be printed. Defaults to False.
    Returns:
        out (Tuple[int, int]):
            - the number of times all events were satisfied.
            - the number of brackets that satisfy the rules.
    """
    if events is None:
        events = []
    if rules is None:
        rules = []

    num_teams: int = len(teams)
    num_events: int = len(events)
    num_rules: int = len(rules)

    satisfies: int = prod_odd_to(num_teams - 2 * num_events)

    sign: int = 1
    total: int = prod_odd_to(num_teams)
    delta: int = 0
    for i in range(1, num_rules + 1):
        n: int = num_teams - 2 * i
        delta += sign * prod_odd_to(n) * choose(num_rules, i)
        sign = -sign

    return satisfies, total - delta


def print_odds(
    description: str,
    algorithm: Callable[
        [
            List[Team],
            List[Tuple[Team, Team]],
            List[Callable[[Team, Team], bool]],
            bool,
        ],
        Tuple[int, int],
    ],
    teams: List[Team],
    events: Optional[List[Tuple[Team, Team]]] = None,
    rules: Optional[List[Callable[[Team, Team], bool]]] = None,
    debug: bool = False,
) -> None:
    """Print the odds of certain events occurring within a bracket.

    Args:
        description (str):
            description of the conditions.
        algorithm (Callable[ [teams, events, rules, debug], Tuple[int, int] ]):
            algorithm to use.
        teams (List[Team]):
            list of teams in the bracket.
        events (Optional[List[Tuple[Team, Team]]]):
            list of specific events that we want to see. Defaults to None.
        rules (Optional[List[Callable[[Team, Team], bool]]], optional):
            list of rules that all have to be satisfied. Defaults to None.
        debug (bool, optional):
            flag to specify if brackets should be printed. Defaults to False.
    """
    if events is None:
        events = []
    if rules is None:
        rules = []

    numerator: int
    denominator: int

    numerator, denominator = algorithm(teams, events, rules, debug)
    print(f"{description}: {numerator}/{denominator}")


def test(
    algorithm: Callable[
        [List[Team], List[Tuple[Team, Team]], List[Callable[[Team, Team], bool]], bool],
        Tuple[int, int],
    ],
) -> None:
    """Test the accuracy of the algorithm."""
    teams: List[Team]
    events: List[Tuple[Team, Team]]
    rules: List[Callable[[Team, Team], bool]]
    debug: bool = False

    teams = [T1, GEN, HLE, DK, G2, FNC, BLG, FLY]
    events = [(T1, G2)]
    rules = []
    assert algorithm(teams, events, rules, debug) == (15, 105)

    rules = [diff_region]
    assert algorithm(teams, events, rules, debug) == (6, 24)

    rules = [
        invalid_matchup(T1, GEN),
        invalid_matchup(T1, HLE),
        invalid_matchup(T1, DK),
        invalid_matchup(GEN, HLE),
        invalid_matchup(GEN, DK),
        invalid_matchup(HLE, DK),
        invalid_matchup(FNC, G2),
    ]
    assert algorithm(teams, events, rules, debug) == (6, 24)

    events = [(T1, G2)]
    rules = [invalid_matchup(T1, G2)]
    assert algorithm(teams, events, rules, debug) == (0, 90)

    events = [(T1, GEN), (HLE, G2)]
    assert algorithm(teams, events, rules, debug) == (3, 90)

    teams = [GEN, DK, G2, FNC, BLG, FLY]
    events = []
    rules = [diff_region]
    assert algorithm(teams, events, rules, debug) == (10, 10)

    teams = [GEN, HLE, DK, FNC, BLG, FLY]
    assert algorithm(teams, events, rules, debug) == (6, 6)


def main() -> None:
    """Main function."""
    test(brute_force)


if __name__ == "__main__":
    main()
