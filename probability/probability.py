#!/usr/bin/python
"""
Filename: probability.py
Authors: Yoshi Fu
Project: Probability Calculations
Date: February 2025

Summary:
TODO
"""


def complement(p: float) -> float:
    """Calculate the complement of a probability p."""
    return 1 - p


def factorial(n: int) -> int:
    """Calculate the factorial of a number n."""
    product: int = 1
    for i in range(1, n + 1):
        product *= i
    return product


def binomial_coefficient(n: int, k: int) -> int:
    """Calculate the binomial coefficient C(n, k).

    In mathematics, the binomial coefficients are the positive integers that
    occur as coefficients in the binomial theorem.
    """
    # n choose k = n choose (n - k).
    if k > n - k:
        return binomial_coefficient(n, n - k)

    res: int = 1
    for i in range(k):
        res = res * (n - i)
        res = res // (i + 1)
    return res


def choose(n: int, k: int) -> int:
    """Calculate the number of ways to choose k elements from a set of n elements."""
    return binomial_coefficient(n, k)


def permutation(n: int, k: int, repetition: bool = False) -> int:
    """Calculate the number of ways to choose k elements from a set of n elements."""
    if repetition:
        return n**k
    return factorial(n) // factorial(n - k)


def combination(n: int, k: int, repetition: bool = False) -> int:
    """Calculate the number of ways to choose k elements from a set of n elements."""
    if repetition:
        return choose(n + k - 1, k)
    return choose(n, k)


def main() -> None:
    """Main function."""


if __name__ == "__main__":
    main()
