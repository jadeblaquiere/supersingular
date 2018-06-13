#BSD 3-Clause License
#
# Copyright (c) 2018, Joseph deBlaquiere <jadeblaquiere@yahoo.com>
# All rights reserved
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.
#
# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
#
# * Neither the name of ecpy nor the names of its
#   contributors may be used to endorse or promote products derived from
#   this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import gc
from math import sqrt
from rabinmiller import isPrime
from ECC import FieldElement

primes = []

def product(lx):
    pi = 1
    for x in lx:
        pi *= x
    return pi

def factor(x):
    factors = []
    a = 2
    while ((x // a) * a) == x:
        factors.append(a)
        x //= a
        while ((x // a) * a) == x:
            factors.append(a)
            x //= a
        if x == 1:
            return factors
        if isPrime(x):
            factors.append(x)
            return factors
    assert x > 1
    xmax = (x // 2) + 1
    for a in range(3, xmax, 2):
        if isPrime(a) is False:
            continue
        if a > x:
            print(a,x,factors)
        assert a <= x
        while ((x // a) * a) == x:
            factors.append(a)
            x //= a
            while ((x // a) * a) == x:
                factors.append(a)
                x //= a
            if x == 1:
                return factors
            if isPrime(x):
                factors.append(x)
                #print(a)
                return factors
    assert x > 1
    print(factors)
    print(x)
    assert isPrime(x)
    return factors

def divisors(factors):
    a = len(factors)
    expa = int(pow(2,a))
    divs = []
    for i in range(1,expa):
        d = 1
        jj = 1
        for j in range(0,a):
            if (jj & i) != 0:
                d *= factors[j]
            jj *= 2
        assert d > 1
        if d not in divs:
            divs.append(d)
    return divs

for a in range(4, 28):
    for b in range(1, a-1):
        for c in range(1, a-1):
            for m in range(-1,2,2):
                for n in range(-1,2,1):
                    for o in range(-1,2,2):
                        solinas = int(pow(2,a) + (m * pow(2, b)) + (n * pow(2, c)) + o)
                        if solinas in primes:
                            continue
                        if (solinas % 12) != 11:
                            continue
                        if isPrime(solinas):
                            primes.append(solinas)
                            #print("%d 0x%X" % (solinas, solinas))

for p in primes:
    f = factor(p+1)
    r = f[-1]
    h = (p+1) // r
    if r > (h >> 1):
        rf = factor(r-1)
        print("p = %d 0x%X" % (p, p))
        print("factors p+1(%d) = " % (p+1), f)
        print(f[:-1])
        assert h == product(f[:-1])
        print("order = %d, cofactor= %d" % (r, h))
        print(r-1, rf)
        divs = divisors(f[:-1])
        print(divs)
        for d in divs:
            dm = d - 1
            rm = r - 1
            if dm > 1:
                if ((rm // dm) * dm) == rm:
                    print(d, dm, rm//dm)
        print("p = %d" % (p))
        print("n = %d" % (r))
        print("h = %d" % (h))
        afe = FieldElement(1, p)
        bfe = FieldElement(0, p)
        print("a = %d" % (int(afe)))
        print("b = %d" % (int(bfe)))
        for x in range(2, p):
            xfe = FieldElement(x, p)
            right = (xfe * xfe * xfe) + (afe * xfe) + bfe
            yfe = right.sqrt()
            if yfe is not None:
                print("gx = %d" % (int(xfe)))
                print("gy = %d" % (int(yfe)))
                break
        print("bits = %d" % p.bit_length())
        print()
    gc.collect()
