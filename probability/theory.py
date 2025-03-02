#!/usr/bin/python
"""
Filename: theory.py
Authors: Yoshi Fu
Project: Probability Theory Terminology
Date: February 2025

Summary:
TODO
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from fractions import Fraction
from random import choices
from typing import Any, Callable, Generator, Iterable, Union


@dataclass
class ProbabilitySpace:
    """A probability space or a probability triple (Ω, F, P) is a mathematical
    construct that provides a formal model of a random process or experiment.

    The sample space Ω is the set of all possible outcomes of a random process.
    For a dice roll, the sample space is {1, 2, 3, 4, 5, 6}.

    The event space F is a collection of subsets of the sample space.
    For a dice roll, the event space could be {odd, even}.

    The probability function P assigns a probability to each event in the event
    space. For the example above, P(odd) = 1/2 and P(even) = 1/2.

    Source: https://en.wikipedia.org/wiki/Probability_space

    Attributes:
        omega (set): sample space.
        f (set): event space.
        p (dict): probability function.
    """

    omega: set[Any]
    f: set[Any]
    p: dict[Any, float]


class ProbabilityDistribution(ABC):
    """A probability distribution is a mathematical function that provides the
    probabilities of occurrence of different possible outcomes in an experiment.
    """

    @abstractmethod
    def mean(self) -> float:
        """Expected value of a random variable."""

    @abstractmethod
    def variance(self) -> float:
        """Measure of the spread of a random variable."""


class RandomVariable(ABC):
    """A random variable is a variable whose value is subject to variations due
    to randomness.

    A random variable can take on a set of possible different values (similar to
    a discrete random variable) or an interval of values (similar to a continuous
    random variable).
    """

    @abstractmethod
    def mean(self) -> Union[Fraction, float]:
        """Expected value of a random variable."""

    @abstractmethod
    def variance(self) -> Union[Fraction, float]:
        """Measure of the spread of a random variable."""


@dataclass
class DiscreteRandomVariable(RandomVariable):
    """A discrete random variable is a random variable that has a finite number
    of possible outcomes or countable number of outcomes.

    Attributes:
        values (set): possible values of the discrete random variable.
        weights (dict): weights or probabilities of the values.
    """

    values: set[Any]
    weights: dict[Any, Fraction]

    def sample(self) -> Any:
        """Sample a value from the discrete random variable."""
        return choices(list(self.values), weights=list(self.weights.values()))[0]

    def odds(self, *args, satisfies_all: bool = False) -> Fraction:
        """Compute the odds for an event to occur."""
        if all([isinstance(arg, set) for arg in args]):
            return self._odds_events(*args)
        if all(callable(arg) for arg in args):
            return self._odds_functions(*args, satisfies_all=satisfies_all)
        return Fraction(0)

    def _odds_events(self, events: set[Any]) -> Fraction:
        """Compute the odds for any event in events to occur."""
        if self.values.isdisjoint(events):
            return Fraction(0)
        return Fraction(sum(self.weights[v] for v in events))

    def _odds_functions(
        self, *functions: Callable[[Any], bool], satisfies_all: bool = False
    ) -> Fraction:
        """Compute the odds for any event satisfying a function in functions to occur."""
        func: Callable[[Iterable], bool] = all if satisfies_all else any

        outcomes: set[Any] = {v for v in self.values if func(f(v) for f in functions)}
        return Fraction(sum(self.weights[outcome] for outcome in outcomes))

    def mean(self) -> Fraction:
        """Expected value of a random variable."""
        return sum(Fraction(self.weights[v]) * v for v in self.values)

    def variance(self) -> Fraction:
        """Measure of the spread of a random variable."""
        mean_value: Fraction = self.mean()
        return sum(
            Fraction(self.weights[v]) * (v - mean_value) ** 2 for v in self.values
        )


@dataclass
class ContinuousRandomVariable(RandomVariable):
    """A continuous random variable is a random variable that has an uncountable
    number of possible outcomes.

    Attributes:
        pdf (Callable): probability density function of the continuous random variable.
    """

    min_value: float
    max_value: float
    pdf: Callable[[float], float]
    dx: float = 0.01

    def set_dx(self, dx: float) -> None:
        """Set the step size for the range of the continuous random variable."""
        self.dx = dx

    def range(self) -> Generator[float, None, None]:
        """Calculate the range of a continuous random variable."""
        x: float = self.min_value
        while x < self.max_value:
            yield x
            x += self.dx

    def mean(self) -> float:
        """Expected value of a random variable."""
        return sum(x * self.pdf(x) for x in self.range())

    def variance(self) -> float:
        """Measure of the spread of a random variable."""
        mean_value: float = self.mean()
        return sum((x - mean_value) ** 2 * self.pdf(x) for x in self.range())


def join(
    rv1: DiscreteRandomVariable, rv2: DiscreteRandomVariable
) -> DiscreteRandomVariable:
    """Join two random variables into a joint random variable."""
    values: set[tuple[Any, Any]] = {(v1, v2) for v1 in rv1.values for v2 in rv2.values}
    pmf: dict[tuple[Any, Any], Fraction] = {
        (v1, v2): rv1.weights[v1] * rv2.weights[v2]
        for v1 in rv1.values
        for v2 in rv2.values
    }
    return DiscreteRandomVariable(values=values, weights=pmf)
