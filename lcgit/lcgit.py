#!/usr/bin/env python3

"""
see: https://stackoverflow.com/questions/44818884/all-numbers-in-a-given-range-but-random-order
see: https://en.wikipedia.org/wiki/Linear_congruential_generator
"""


from random import randint, shuffle
from collections.abc import Sequence
from ipaddress import _BaseNetwork


def lcg_params(u, v):
    # Generate parameters for an LCG that produces a maximal length sequence
    # of numbers in the range (u..v)
    diff = v - u
    if diff < 4:
        raise ValueError("Sorry, range must be at least 4.")
    m = 2 ** diff.bit_length()  # Modulus
    a = (randint(1, (m >> 2) - 1) * 4) + 1  # Random odd integer, (a-1) divisible by 4
    c = randint(3, m) | 1  # Any odd integer will do
    return (m, a, c)


class LCG(object):
    def __init__(self, sequence, state=None):
        if isinstance(sequence, Sequence):
            self.seqlength = len(sequence)
            self.start = 0
            self.end = self.seqlength - 1
        elif isinstance(sequence, _BaseNetwork):
            self.start = int(sequence[0])
            self.end = int(sequence[-1])
            self.seqlength = self.end - self.start + 1
        else:
            raise ValueError(
                "sequence must be an instance of sequence or ipaddress._BaseNetwork"
            )
        self.seq = sequence
        (m, a, c) = lcg_params(self.start, self.end)
        self.modulus = m
        if state is None:
            # create a new state
            (self.multiplier, self.increment) = (a, c)
            self.seed = 1
            self.index = 0
        else:
            # load passed in state
            (self.multiplier, self.increment, self.seed, self.index) = state

    def __iter__(self):
        return LCGIterator(self)

    def __repr__(self):
        return f"{self.__class__.__name__}({self.start}, {self.end})"

    def __len__(self):
        return self.seqlength


class LCGIterator(object):
    def __init__(self, parent):
        self.parent = parent
        self.index = self.parent.index
        self.seed = self.parent.seed

    def __next__(self):
        if self.index >= self.parent.seqlength:
            raise StopIteration
        while True:
            self.seed = (
                self.seed * self.parent.multiplier + self.parent.increment
            ) % self.parent.modulus
            if self.seed < self.parent.seqlength:
                break
        self.index += 1
        return self.parent.seq[self.seed]

    def save(self):
        return (self.parent.multiplier, self.parent.increment, self.seed, self.index)
