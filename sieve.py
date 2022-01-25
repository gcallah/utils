#!/usr/bin/python3
from typing import List  # noqa F401
ints = []  # type: List[bool]

n = 20  # type: int


def init(n: int) -> None:
    for i in range(2, n + 1):
        ints.append(True)


def sieve(n: int) -> None:
    stop = n**(1/2)   # type: float
    stop = int(stop)
    print("stop = " + str(stop))
    for i in range(2, stop + 1):
        print(i)
        if ints[i - 2] is True:
            j = (i * 2) - 2
            while j < len(ints):
                print("j = " + str(j))
                ints[j] = False
                j = j + i


init(n)
sieve(n)
print(ints)
