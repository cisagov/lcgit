"""A fast generator of random, non-repeating, maximal length sequences.

This library is used to generate randomized sequences from Python sequences
and IP networks.
"""
# We disable a Flake8 check for "Module imported but unused (F401)" here because
# although this import is not directly used, it populates the value
# package_name.__version__, which is used to get version information about this
# Python package.
from ._version import __version__  # noqa: F401
from .lcgit import lcg

__all__ = ["lcg"]
