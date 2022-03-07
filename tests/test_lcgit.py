#!/usr/bin/env pytest -vs
"""Tests for lcgit."""

# Standard Python Libraries
from ipaddress import ip_network as net

# Third-Party Libraries
import pytest

# cisagov Libraries
from lcgit import lcg, lcgit

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
    answer = sorted(i for i in sequence)
    my_lcg = lcg(sequence)
    accumulated = []
    count = 0
    for i in my_lcg:
        count += 1
        accumulated.append(i)
    assert (
        sorted(accumulated) == answer
    ), "accumulated list should be identical to answer list"


@pytest.mark.parametrize("sequence", sequences)
def test_state_save_and_restore(sequence):
    """Verify state save and restore."""
    answer = sorted(i for i in sequence)
    lcg1 = lcg(sequence, emit=True)
    accumulated = []
    break_at = len(lcg1) / 2
    count = 0
    state = None
    for i, state in lcg1:
        count += 1
        accumulated.append(i)
        if count == break_at:
            break
    assert (
        len(lcg1) <= 1 or sorted(accumulated) != answer
    ), "accumulated list should NOT be identical to answer list yet"
    if state:  # empty sequences won't generate state
        lcg2 = lcg(sequence, state)
        for i in lcg2:
            count += 1
            accumulated.append(i)
        assert (
            sorted(accumulated) == answer
        ), "accumulated list should be identical to answer list"


@pytest.mark.parametrize("sequence", sequences)
def test_iter_consistency(sequence):
    """Verify that iterators are consistent for an LCG."""
    lcg1 = lcg(sequence, emit=True)
    i = iter(lcg1)
    j = iter(lcg1)
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
        lcg(1)


def test_repr():
    """Verify that the repr is in the expected format."""
    lcg1 = lcg("foobar")
    r = repr(lcg1)
    assert r == "lcg(0, 5)"
