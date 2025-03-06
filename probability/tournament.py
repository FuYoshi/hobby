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
from typing import Callable, Generator, List, Optional, Tuple


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
    name: str = ""

    def __str__(self) -> str:
        return self.tag


T1: Team = Team(Region.LCK, "T1 ", "T1")
GEN: Team = Team(Region.LCK, "GEN", "Gen.G")
HLE: Team = Team(Region.LCK, "HLE", "Hanwha Life Esports")
DK: Team = Team(Region.LCK, "DK ", "Dplus Kia")
G2: Team = Team(Region.LEC, "G2 ", "G2 Esports")
FNC: Team = Team(Region.LEC, "FNC", "Fnatic")
BLG: Team = Team(Region.LPL, "BLG", "Bilibili Gaming")
FLY: Team = Team(Region.LCS, "FLY", "FlyQuest")


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
        Generator[Tuple[List[Tuple[Team, Team]], List[Team]], None, None]:
            the chosen matchup and a list with the other teams that are left.
    """
    team1: Team = teams[0]
    other_teams: List[Team] = teams[1:]
    for i, team2 in enumerate(other_teams):
        if all(rule(team1, team2) for rule in rules):
            yield [(team1, team2)], other_teams[:i] + other_teams[(i + 1) :]


def generate_brackets(
    teams: List[Team], rules: Optional[List[Callable[[Team, Team], bool]]] = None
) -> Generator[List[Tuple[Team, Team]], None, None]:
    """Generate all possible matchups that can form inside a bracket.

    Args:
        teams (List[Team]):
            list of teams in the bracket.
        rules (Optional[List[Callable[[Team, Team], bool]]]):
            list of rules that all have to be satisfied. Defaults to None.

    Yields:
        Generator[List[Tuple[Team, Team]], None, None]:
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
                for other_matchup in generate_brackets(other_teams):
                    yield matchup + other_matchup


def count_brackets(
    teams: List[Team], rules: Optional[List[Callable[[Team, Team], bool]]] = None
) -> int:
    """Count the number of different brackets for the given teams and conditions.

    Args:
        teams (List[Team]):
            list of teams in the bracket.
        rules (Optional[List[Callable[[Team, Team], bool]]], optional):
            list of rules that all have to be satisfied. Defaults to None.

    Returns:
        int: number of different brackets possible.
    """
    if rules is None:
        rules = []

    return sum(1 for _ in generate_brackets(teams, rules))


def print_bracket(bracket: List[Tuple[Team, Team]]) -> None:
    """Print the bracket in readable format.

    Args:
        bracket (List[Tuple[Team, Team]]): list of all matchups in the bracket.
    """
    for matchup in bracket:
        print(" vs ".join(map(str, matchup)))
    print()


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
        Callable[[Team, Team], bool]:
            function that returns True if it does not see a and b again, False otherwise.
    """
    return lambda x, y: not ((x == a and y == b) or (x == b and y == a))


def odds_bracket(
    teams: List[Team],
    conds: List[Tuple[Team, Team]],
    rules: Optional[List[Callable[[Team, Team], bool]]] = None,
) -> Tuple[int, int]:
    """Compute the odds of specific matchups occuring within a bracket.

    Args:
        teams (List[Team]):
            list of teams in the bracket.
        conds (List[Tuple[Team, Team]]):
            list of specific matchups that we want to see.
        rules (Optional[List[Callable[[Team, Team], bool]]], optional):
            list of rules that all have to be satisfied. Defaults to None.

    Returns:
        Fraction: odds of the specific matchups occuring within the bracket.
    """
    # If the specified matchup cannot be possible, return 0.
    for team1, team2 in conds:
        if team1 not in teams or team2 not in teams or team1 is team2:
            return 0, 0

    # Remove the forced matchups to simplify the rest of the computation.
    remaining_teams: List[Team] = teams[:]
    for team1, team2 in conds:
        remaining_teams.remove(team1)
        remaining_teams.remove(team2)

    # Compute the amount of times the conditions are and are not satisfied.
    satisfies: int = count_brackets(remaining_teams, rules)
    return satisfies, count_brackets(teams, rules)


def print_odds(
    description: str,
    teams: List[Team],
    conds: List[Tuple[Team, Team]],
    rules: Optional[List[Callable[[Team, Team], bool]]] = None,
) -> None:
    """Print the odds of certain matchups occuring within a bracket.

    Args:
        description (str):
            description of the conditions.
        teams (List[Team]):
            list of teams in the bracket.
        conds (List[Tuple[Team, Team]]):
            list of specific matchups that we want to see.
        rules (Optional[List[Callable[[Team, Team], bool]]], optional):
            list of rules that all have to be satisfied. Defaults to None.
    """
    numerator: int
    denominator: int

    numerator, denominator = odds_bracket(teams, conds, rules)
    print(description, f"{numerator}/{denominator}")


def main() -> None:
    """Main function."""
    # List of teams in the bracket.
    teams: List[Team] = [T1, GEN, HLE, DK, G2, FNC, BLG, FLY]

    print_odds(
        "Odds of T1 vs GEN and HLE vs G2, if T1 vs G2 is invalid:",
        teams,
        [(T1, GEN), (HLE, G2)],
        [invalid_matchup(T1, G2)],
    )

    print_odds(
        "Odds of seeing T1 vs G2, if there can't be same region matchups",
        teams,
        [(T1, G2)],
        [diff_region],
    )

    print_odds(
        "Odds of seeing T1 vs G2, if there are no conditions:",
        teams,
        [(T1, G2)],
    )


if __name__ == "__main__":
    main()
