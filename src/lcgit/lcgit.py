#!/usr/bin/env python3
"""
Implementation of a Linear Congruential Generator.

This LCG can be used to quickly generate random, non-repeating, maximal length sequences
from existing sequences and IP networks.

see: https://stackoverflow.com/questions/44818884/all-numbers-in-a-given-range-but-random-order
see: https://en.wikipedia.org/wiki/Linear_congruential_generator
"""

# Standard Python Libraries
from collections.abc import Sequence
from ipaddress import _BaseNetwork
from math import sin
from random import Random, randint


def _lcg_params(u, v):
    """Generate parameters for an LCG.

    The parameters will produces a maximal length sequence of numbers
    in the range (u..v)
    """
    diff = v - u
    if diff < 4:
        raise ValueError("range must be at least 4.")
    # Modulus
    m = 2 ** diff.bit_length()
    # Random odd integer, (a-1) divisible by 4
    a = (randint(1, (m >> 2) - 1) * 4) + 1  # nosec
    # Any odd integer will do
    c = randint(3, m) | 1  # nosec
    return (m, a, c)


class lcg(object):
    """A Linear Congruential Generator object.

    This LCG class contains methods which are used to generate random, non-repeating,
    maximal length sequences from sequences or IP networks.
    """

    def __init__(self, sequence, state=None, emit=False):
        """Instanciate a new LCG.

        Args:
            sequence: A Python Sequence, IPv4, or IPv6 network.
                range(10)
                [1, 2, 3, 4, 5]
                foobarbaz
                IPv4Network("192.0.2.0/24")
                IPv6Network('::8bad:f00d:0/112')
            state: A tuple describing state, saved from a previous LCG iterator.
                An LCG iterator can be configured to emit state along with its
                randomized sequence.  This state can be saved and used to resume an LCG
                at a later time.
                State is of the form: (multiplier, increment, seed, index)
            emit: A boolean that enables the state emission of iterators.  When state
                emission is on, LCG iterators will yield random sequence values as well
                as the current state of the generator.

        Raises:
            ValueError: If the sequence is not of the correct type.

        """
        self.emit = emit
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
        if self.seqlength > 4:
            (m, a, c) = _lcg_params(self.start, self.end)
        else:
            (m, a, c) = (1, 1, 1)
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
        """Generate Iterator over the randomized sequence.

        Yields:
            if the LCG was created with emit=True: (random_value, state_tuple)
            if the LCG was created with emit=False only the value is yielded.

        """
        seed = self.seed
        index = self.index
        if self.seqlength > 4:
            # use LCG
            while index < self.seqlength:
                while True:
                    seed = (seed * self.multiplier + self.increment) % self.modulus
                    if seed < self.seqlength:
                        break
                index += 1
                if self.emit:
                    yield self.seq[seed], (self.multiplier, self.increment, seed, index)
                else:
                    yield self.seq[seed]
        else:
            # use shuffle
            shuffled_seq = list(self.seq)
            seeded_random = Random()
            seeded_random.seed(
                abs(sin(self.multiplier + self.increment + seed)), version=1
            )
            seeded_random.shuffle(shuffled_seq)
            for i in shuffled_seq[index:]:
                index += 1
                if self.emit:
                    yield i, (self.multiplier, self.increment, seed, index)
                else:
                    yield i

    def __repr__(self):
        """Return repr(self)."""
        return f"{self.__class__.__name__}({self.start}, {self.end})"

    def __len__(self):
        """Return len(self)."""
        return self.seqlength
