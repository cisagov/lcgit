#!/usr/bin/env pytest -vs
"""Tests for lcgit."""

import pytest
from ipaddress import ip_network as net
from lcgit import LCG

sequences = [
    "foobar",
    range(10),
    # net("192.168.1.0/32"),
    # net("192.168.1.0/31"),
    # net("192.168.1.0/30"),
    net("192.168.1.0/29"),
    net("192.168.1.0/28"),
    net("192.168.1.0/24"),
    net("192.168.0.0/20"),
    # net("172.16.0.0/12"), # execution time too long
    # net("10.0.0.0/8"), # execution time too long
]


@pytest.mark.parametrize("sequence", sequences)
def test_counts_and_dups(sequence):
    """Verify LCG output integrity."""
    answer = sorted([i for i in sequence])
    lcg = LCG(sequence)
    accumulated = []
    count = 0
    for i, state in lcg:
        count += 1
        accumulated.append(i)
    assert (
        sorted(accumulated) == answer
    ), "accumulated list should be identical to answer list"


@pytest.mark.parametrize("sequence", sequences)
def test_state_save_and_restore(sequence):
    """Verify state save and restore."""
    answer = sorted([i for i in sequence])
    lcg = LCG(sequence)
    accumulated = []
    break_at = len(lcg) / 2
    count = 0
    for i, state in lcg:
        print(f"a: {state}")
        count += 1
        accumulated.append(i)
        if count == break_at:
            break
    assert (
        sorted(accumulated) != answer
    ), "accumulated list should NOT be identical to answer list yet"
    lcg2 = LCG(sequence, state)
    for i, state in lcg2:
        print(f"b: {state}")
        count += 1
        accumulated.append(i)
    assert (
        sorted(accumulated) == answer
    ), "accumulated list should be identical to answer list"
