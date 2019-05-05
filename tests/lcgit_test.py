#!/usr/bin/env pytest -vs
"""Tests for lcgit."""

import pytest
from ipaddress import ip_network as net
from lcgit import LCG, lcgit

sequences = [
    [],
    [1],
    "foobar",
    range(10),
    net("192.168.1.0/32"),
    net("192.168.1.0/31"),
    net("192.168.1.0/30"),
    net("192.168.1.0/29"),
    net("192.168.1.0/28"),
    net("192.168.1.0/24"),
    net("192.168.0.0/20"),
    pytest.param(net("172.16.0.0/12"), marks=pytest.mark.slow),
    pytest.param(net("10.0.0.0/8"), marks=pytest.mark.slow),
]


@pytest.mark.parametrize("sequence", sequences)
def test_counts_and_dups(sequence):
    """Verify LCG output integrity."""
    answer = sorted([i for i in sequence])
    lcg = LCG(sequence)
    accumulated = []
    count = 0
    for i in lcg:
        count += 1
        accumulated.append(i)
    assert (
        sorted(accumulated) == answer
    ), "accumulated list should be identical to answer list"


@pytest.mark.parametrize("sequence", sequences)
def test_state_save_and_restore(sequence):
    """Verify state save and restore."""
    answer = sorted([i for i in sequence])
    lcg = LCG(sequence, emit=True)
    accumulated = []
    break_at = len(lcg) / 2
    count = 0
    state = None
    for i, state in lcg:
        count += 1
        accumulated.append(i)
        if count == break_at:
            break
    assert (
        len(lcg) <= 1 or sorted(accumulated) != answer
    ), "accumulated list should NOT be identical to answer list yet"
    if state:  # empty sequences won't generate state
        lcg2 = LCG(sequence, state)
        for i in lcg2:
            count += 1
            accumulated.append(i)
        assert (
            sorted(accumulated) == answer
        ), "accumulated list should be identical to answer list"


@pytest.mark.parametrize("sequence", sequences)
def test_iter_consistency(sequence):
    """Verify that iterators are consistent for an LCG."""
    lcg = LCG(sequence, emit=True)
    i = iter(lcg)
    j = iter(lcg)
    try:
        while True:
            (x, x_state) = next(i)
            (y, y_state) = next(j)
            assert x == y, "identical iterators should generate identical values"
            assert (
                x_state == y_state
            ), "identical iterators should generate identical states"
    except StopIteration:
        pass


def test_too_small_range():
    """Check for expected exception when range is too small."""
    with pytest.raises(ValueError):
        lcgit._lcg_params(1, 2)


def test_invalid_input():
    """Check for expected exception when constructed with improper input."""
    with pytest.raises(ValueError):
        LCG(1)


def test_repr():
    """Verify that the repr is in the expected format."""
    lcg = LCG("foobar")
    r = repr(lcg)
    assert r == "LCG(0, 5)"
