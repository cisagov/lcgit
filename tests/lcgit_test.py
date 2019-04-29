#!/usr/bin/env pytest -vs
"""Tests for lcgit."""

import pytest
from ipaddress import ip_network as net
from lcgit import LCG

sequences = [
    "foobar",
    range(10),
    net("192.168.1.0/32"),
    net("192.168.1.0/31"),
    net("192.168.1.0/30"),
    net("192.168.1.0/29"),
    net("192.168.1.0/28"),
    net("192.168.1.0/24"),
    net("192.168.0.0/20"),
    # net("172.16.0.0/12"), # execution time too long
    # net("10.0.0.0/8"), # execution time too long
]


@pytest.mark.parametrize("sequence", sequences)
def test_counts_and_dups(sequence):
    """Test a sequence."""
    rns = LCG(sequence)
    accumulated = []
    count = 0
    for i in rns:
        count += 1
        accumulated.append(i)
    answer = sorted([i for i in sequence])
    accumulated = sorted(accumulated)
    assert accumulated == answer, "accumulated list should be identical to answer list"
