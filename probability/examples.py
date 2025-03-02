#!/usr/bin/python
"""
Filename: examples.py
Authors: Yoshi Fu
Project: Examples
Date: February 2025

Summary:
TODO
"""

from enum import StrEnum, auto
from fractions import Fraction
from typing import Any, Callable, Optional

from theory import DiscreteRandomVariable, join


class Coin(StrEnum):
    """Class for the outcomes of a coin flip."""

    HEADS = auto()
    TAILS = auto()


CARD_RANKS: str = "23456789TJQKA"
CARD_SUITS: str = "♠♡♢♣"


class CoinFlip(DiscreteRandomVariable):
    """A random variable representing the outcome of a coin flip."""

    def __init__(self, p: Optional[Fraction] = None) -> None:
        # If p is not provided, assume a fair coin.
        if p is None:
            p = Fraction(1, 2)
        q: Fraction = 1 - p

        super().__init__(
            values={Coin.HEADS, Coin.TAILS}, weights={Coin.HEADS: p, Coin.TAILS: q}
        )
        self.p: Fraction = p

    def flip(self) -> str:
        """Flip the coin."""
        return self.sample()

    def mean(self) -> Fraction:
        """Expected value of a random variable."""
        return self.p

    def variance(self) -> Fraction:
        """Measure of the spread of a random variable."""
        return self.p * (1 - self.p)


class DiceRoll(DiscreteRandomVariable):
    """A random variable representing the outcome of a dice roll."""

    def __init__(
        self,
        values: Optional[set[int]] = None,
        weights: Optional[dict[Any, Fraction]] = None,
    ) -> None:
        # If values are not provided, assume a fair dice.
        if values is None:
            values = {1, 2, 3, 4, 5, 6}
        if weights is None:
            weights = {i: Fraction(1, len(values)) for i in values}

        super().__init__(values=values, weights=weights)

    def roll(self) -> int:
        """Roll the dice."""
        return self.sample()


class CardDraw(DiscreteRandomVariable):
    """A random variable representing the outcome of a card draw."""

    def __init__(
        self,
        values: Optional[set[str]] = None,
        weights: Optional[dict[str, Fraction]] = None,
    ) -> None:
        # If values are not provided, assume a standard deck of cards.
        if values is None:
            values = {f"{r}{s}" for r in CARD_RANKS for s in CARD_SUITS}
        if weights is None:
            weights = {v: Fraction(1, len(values)) for v in values}

        super().__init__(values=values, weights=weights)

    def _odds_events(self, events: set[str]) -> Fraction:
        """Odds of an event in the discrete random variable."""
        filtered_events: set[str] = {
            v
            for v in self.values
            if any(v == e or v.startswith(e) or v.endswith(e) for e in events)
        }
        return Fraction(sum(self.weights[v] for v in filtered_events))

    def draw(self) -> str:
        """Draw a card."""
        return self.sample()


def main() -> None:
    """Main function."""
    coin: CoinFlip = CoinFlip()
    dice: DiceRoll = DiceRoll()
    cards: CardDraw = CardDraw()
    joint: DiscreteRandomVariable = join(coin, dice)

    # Dice test sets.
    even: set[int] = {2, 4, 6}
    prime: set[int] = {2, 3, 5}
    # Dice test functions.
    is_even: Callable[[int], bool] = lambda v: v % 2 == 0
    is_prime: Callable[[int], bool] = lambda v: v == 2 or v == 3 or v == 5

    print("Dice:")
    print(f"\tPr(Even):           {dice.odds(even)}")
    print(f"\tPr(Prime):          {dice.odds(prime)}")
    print(f"\tPr(Even or Prime):  {dice.odds(even | prime)}")
    print(f"\tPr(Even and Prime): {dice.odds(even & prime)}")
    print(f"\tPr(Even and Prime): {dice.odds(is_even, is_prime, satisfies_all=True)}")

    print("Coin and Dice:")
    print(
        f"\tPr(Heads -> Even):  {joint.odds({(Coin.HEADS, 2), (Coin.TAILS, 4), (Coin.HEADS, 6)})}"
    )

    print("Deck:")
    print(f"\tPr(2 in deck):      {cards.odds({"2"})}")
    print(f"\tPr(♡ in deck):      {cards.odds({"♡"})}")
    print(f"\tPr(2 | ♡ in deck):  {cards.odds({"♡", "2"})}")


if __name__ == "__main__":
    main()
