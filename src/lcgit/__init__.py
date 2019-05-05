"""A fast generator of random, non-repeating, maximal length sequences.

This library is used to generate randomized sequences from python sequences
and IP networks.
"""
from .lcgit import lcg

__all__ = ["lcg"]
__version__ = "1.0"
