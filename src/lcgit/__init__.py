"""A fast generator of random, non-repeating, maximal length sequences.

This library is used to generate randomized sequences from python sequences
and IP networks.
"""
from .lcgit import lcg
from ._version import __version__  # noqa: F401

__all__ = ["lcg"]
