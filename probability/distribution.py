#!/usr/bin/python
"""
Filename: distribution.py
Authors: Yoshi Fu
Project: Probability Distributions
Date: February 2025

Summary:
TODO
"""


from probability import choose, complement
from theory import ProbabilityDistribution


class Bernoulli(ProbabilityDistribution):
    """Discrete probability distribution of a random variable which takes the
    value 1 with probability p and the value 0 with probability q = 1 - p.

    Calculation of the mean:
        E[X] = Pr(X = 1) * 1 + Pr(X = 0) * 0
             = p * 1 + q * 0
             = p

    Calculation of the variance:
        Var(X) = E[X^2] - (E[X])^2
               = Pr(X = 1) * 1^2 + Pr(X = 0) * 0^2 - (E[X])^2
               = p * 1 + q * 0 - p^2
               = p - p^2
               = p(1 - p)
               = pq

    Source: https://en.wikipedia.org/wiki/Bernoulli_distribution

    Attributes:
        p (float): probability of success.
        q (float): probability of failure.
    """

    def __init__(self, p: float) -> None:
        self.p: float = p
        self.q: float = complement(p)

    def mean(self) -> float:
        return self.p

    def variance(self) -> float:
        return self.p * self.q


class Binomial(ProbabilityDistribution):
    """Discrete probability distribution of the number of successes in a
    sequence of n independent Bernoulli trials.

    Calculation of the mean:
        E[X] = E[X_1 + ... + X_n]
             = E[X_1] + ... + E[X_n]
             = p + ... + p
             = np

    Calculation of the variance:
        Var(X) = Var(X_1 + ... + X_n)
               = Var(X_1) + ... + Var(X_n)
               = pq + ... + pq
               = npq

    Source: https://en.wikipedia.org/wiki/Binomial_distribution

    Attributes:
        n (int): number of trials.
        p (float): probability of success.
        q (float): probability of failure.
    """

    def __init__(self, n: int, p: float) -> None:
        self.n: int = n
        self.p: float = p
        self.q: float = complement(p)

    def probability(self, k: int) -> float:
        """Probability of exactly k successes in n trials."""
        return choose(self.n, k) * self.p**k * self.q ** (self.n - k)

    def mean(self) -> float:
        return self.n * self.p

    def variance(self) -> float:
        return self.n * self.p * self.q


class Normal(ProbabilityDistribution):
    """Continuous probability distribution that is symmetric about the mean,
    showing that data near the mean are more frequent in occurrence than data
    far from the mean.

    Calculation of the mean:
        E[X] = μ

    Calculation of the variance:
        Var(X) = σ^2

    Source: https://en.wikipedia.org/wiki/Normal_distribution

    Attributes:
        mu (float): mean.
        sigma (float): standard deviation.
    """

    def __init__(self, mu: float, sigma: float) -> None:
        self.mu: float = mu
        self.sigma: float = sigma

    def mean(self) -> float:
        return self.mu

    def variance(self) -> float:
        return self.sigma**2
