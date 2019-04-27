#!/usr/bin/env python3

"""
see: https://stackoverflow.com/questions/44818884/all-numbers-in-a-given-range-but-random-order
see: https://en.wikipedia.org/wiki/Linear_congruential_generator
"""


import ipaddress
from random import randint, shuffle


def lcg_params(u, v):
    # Generate parameters for an LCG that produces a maximal length sequence
    # of numbers in the range (u..v)
    diff = v - u
    if diff < 4:
        raise ValueError("Sorry, range must be at least 4.")
    m = 2 ** diff.bit_length()  # Modulus
    a = (randint(1, (m >> 2) - 1) * 4) + 1  # Random odd integer, (a-1) divisible by 4
    c = randint(3, m) | 1  # Any odd integer will do
    return (m, a, c)


def network_length(network):
    return int(network[-1]) - int(network[0]) + 1


class RandomNetworkIterator(object):
    def __init__(self, network, state=None):
        self.network = network
        first_ip_int = int(network[0])
        last_ip_int = int(network[-1])
        self.offset = first_ip_int
        self.seqlength = last_ip_int - first_ip_int + 1
        (m, a, c) = lcg_params(first_ip_int, last_ip_int)
        self.modulus = m
        if state is None:
            (self.multiplier, self.increment) = (a, c)
            self.seed = 1
            self.index = 0
        else:
            (self.multiplier, self.increment, self.seed, self.index) = state

    def __next__(self):
        if self.index >= self.seqlength:
            raise StopIteration
        while True:
            self.seed = (self.seed * self.multiplier + self.increment) % self.modulus
            if self.seed < self.seqlength:
                break
        self.index += 1
        return ipaddress.ip_address(self.seed + self.offset)

    def __repr__(self):
        return "%s(%s)" % (self.__class__.__name__, repr(self.network))

    def save(self):
        return (self.multiplier, self.increment, self.seed, self.index)


class RandomNetworkSequence(object):
    def __init__(self, network):
        self.network = network

    def __iter__(self):
        # the LCG does not work with small sequences, so we'll just use shuffle
        if network_length(self.network) <= 4:
            ip_list = [i for i in self.network]
            shuffle(ip_list)
            return iter(ip_list)
        else:
            return RandomNetworkIterator(self.network)

    def __repr__(self):
        return "%s(%s)" % (self.__class__.__name__, repr(self.network))
