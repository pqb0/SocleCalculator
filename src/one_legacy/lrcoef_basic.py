# Caluclator for basic Littlewood richardson coefficient

from itertools import permutations

def is_partition(p):
    return all(p[i] >= p[i+1] for i in range(len(p)-1))

def subtract_partitions(lam, mu):
    """Return skew shape lam/mu as list of row lengths."""
    if len(mu) > len(lam) or any(mu[i] > lam[i] for i in range(len(mu))):
        return None
    skew = [lam[i] - (mu[i] if i < len(mu) else 0) for i in range(len(lam))]
    return skew

def weight_to_list(weight):
    """Expand weight partition to list, e.g. (2,1) -> [1,1,2]."""
    res = []
    for i, m in enumerate(weight):
        res += [i+1]*m
    return res

def is_yamanouchi(word):
    """Check lattice word (Yamanouchi) condition."""
    counts = {}
    for x in word:
        counts[x] = counts.get(x, 0) + 1
        for y in range(1, x):
            if counts.get(y, 0) < counts[x]:
                return False
    return True

def lrcoefP(mu, nu, lam):
    """Compute c^{lam}_{mu,nu} using Yamanouchi condition."""
    skew = subtract_partitions(lam, mu)
    if skew is None:
        return 0
    num_boxes = sum(skew)
    if num_boxes != sum(nu):
        return 0

    # naive enumeration for small cases
    entries = weight_to_list(nu)
    c = 0
    for perm in set(permutations(entries)):
        if is_yamanouchi(perm):
            c += 1
    return c


print(lrcoefP((1,), (1,), (2,)))    # Expect 1  (since s_1 * s_1 = s_2 + s_{1,1})
print(lrcoefP((1,), (1,), (1,1)))   # Expect 1
print(lrcoefP((2,), (1,), (3,)))    # Expect 1
print(lrcoefP((2,), (1,), (2,1)))   # Expect 1
print(lrcoefP((2,), (2,), (4,)))    # Expect 1
