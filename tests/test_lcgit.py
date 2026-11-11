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
    for i, current_state in lcg1:
        count += 1
        accumulated.append(i)
        state = current_state
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
            x, x_state = next(i)
            y, y_state = next(j)
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


invalid_states = [
    (1, 0, 110, 0),  # even increment; seed is a fixed point >= seqlength
    (2, 1, 1, 0),  # multiplier is not congruent to 1 (mod 4)
    (5, 2, 1, 0),  # even increment
    (5, 3, -1, 0),  # negative seed
    (5, 3, 200, 0),  # seed >= modulus
    (5, 3, 1, -1),  # negative index
    (5, 3, 1, 101),  # index past the end of the sequence
    (5.0, 3, 1, 0),  # non-integer multiplier
    (5, 3, 1.0, 0),  # non-integer seed
]


@pytest.mark.parametrize("state", invalid_states)
def test_invalid_state(state):
    """Check for expected exception when constructed with an invalid state."""
    with pytest.raises(ValueError):
        lcg(range(100), state=state)


def test_invalid_state_small_sequence():
    """Check for expected exception for a bad state on the shuffle path."""
    with pytest.raises(ValueError):
        lcg(range(3), state=(1, 1, 1.0, 0))


def test_repr():
    """Verify that the repr is in the expected format."""
    lcg1 = lcg("foobar")
    r = repr(lcg1)
    assert r == "lcg(0, 5)"
