# lcgit 🎰 #

[![GitHub Build Status](https://github.com/cisagov/lcgit/workflows/build/badge.svg)](https://github.com/cisagov/lcgit/actions)
[![CodeQL](https://github.com/cisagov/lcgit/workflows/CodeQL/badge.svg)](https://github.com/cisagov/lcgit/actions/workflows/codeql-analysis.yml)
[![Coverage Status](https://coveralls.io/repos/github/cisagov/lcgit/badge.svg?branch=develop)](https://coveralls.io/github/cisagov/lcgit?branch=develop)
[![Known Vulnerabilities](https://snyk.io/test/github/cisagov/lcgit/develop/badge.svg)](https://snyk.io/test/github/cisagov/lcgit)

Do you want to loop randomly through every item in huge sequence without
outputting the same item twice?  Would you like to do this while keeping
minimal state?  Then you need a
[Linear Congruential Generator](https://en.wikipedia.org/wiki/Linear_congruential_generator)
iterator!

```python
from lcgit import lcg
from ipaddress import ip_network

for i in lcg(ip_network("10.0.0.0/8")):
  print(i)
```

The code above, will print out each of the 16,777,216 IPs in the `10.0.0.0/8`
network in random order.  Which is useful.  But what would be more useful is
if you can output some now, save your state, and do some more later!

This is where `emit` comes in.  Creating an `lcg` with `emit=True` will cause
the iterator to emit its state along with the sequence value.  If you save
this state, and pass it back to a new `lcg` it will produce iterators that will
continue the random sequence where you left off.

```python
from lcgit import lcg
from ipaddress import ip_network

my_lcg = lcg(ip_network("192.168.1.0/24"), emit=True)
it = iter(my_lcg)
# print the first 32 random values
for i in range(32):
  value, state = next(it)
  print(value)

# save state, and come back later
save_it(state, to_something)
```

How large is the state?  Am I going to need a flag bit for each item?  Will I
need to buy more RAM and disk?  How about a tuple of four integers, no matter
how large the sequence is!?  The `state` variable at the end of the code block
above would be storing something very similar to: `(149, 223, 161, 32)`

To continue the generator where we left off, you simply create a new one for
the same sequence, and pass in your stored `state`:

```python
restored = load_it(from_somewhere) # (149, 223, 161, 32)
my_new_lcg = lcg(ip_network("192.168.1.0/24"), state=restored)
# print the remaining values
for i in my_new_lcg:
  print(i)
```

`lcgit` doesn't just work with networks.  It will also work with any of the
[Python sequence types](https://docs.python.org/3/library/stdtypes.html#typesseq).

```python
for i in lcg(range(100_000_000_000_000)):
  print(i)
```

## NOOICE! 🕺 ##

## Contributing ##

We welcome contributions!  Please see [`CONTRIBUTING.md`](CONTRIBUTING.md) for
details.

## License ##

This project is in the worldwide [public domain](LICENSE).

This project is in the public domain within the United States, and
copyright and related rights in the work worldwide are waived through
the [CC0 1.0 Universal public domain
dedication](https://creativecommons.org/publicdomain/zero/1.0/).

All contributions to this project will be released under the CC0
dedication. By submitting a pull request, you are agreeing to comply
with this waiver of copyright interest.
