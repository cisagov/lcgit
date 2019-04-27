#!/usr/bin/env pytest -vs
"""Tests for lcgit."""

import pytest
from ipaddress import ip_network as net
from lcgit import RandomNetworkSequence

networks = [
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


@pytest.mark.parametrize("network", networks)
def test_counts_and_dups(network):
    """Test with different networks."""
    rns = RandomNetworkSequence(network)
    acc = set()
    count = 0
    for i in rns:
        count += 1
        print(count, i)
        assert i not in acc, "address duplicated during generation"
        acc.add(i)
    net_size = int(network[-1]) - int(network[0]) + 1
    assert count == net_size, "iterator loop not equal to network size"
    assert len(acc) == net_size, "accumulated set of addresses to equal to network size"
