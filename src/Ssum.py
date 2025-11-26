import math
from itertools import permutations


# --- Partition Methods ---

def degree(partition):
    return sum(partition)

def compare_by_degree(p1, p2):
    d1, d2 = degree(p1), degree(p2)
    if d1 < d2:
        return -1
    elif d1 > d2:
        return 1
    return 0

def ones_partition(x):
    """Return the partition (1, 1, ..., 1) with x ones."""
    if x < 0:
        raise ValueError("x must be nonnegative")
    return tuple(1 for _ in range(x))

def generate_partitions(n, max_part=None):
    """Generate all partitions of n."""
    if n == 0:
        yield ()
    else:
        if max_part is None or max_part > n:
            max_part = n
        for first in range(max_part, 0, -1):
            for rest in generate_partitions(n - first, first):
                yield (first,) + rest

def subset_partitions(partition):
    """Return all partitions with degree <= degree(partition)."""
    d = degree(partition)
    result = []
    for n in range(d + 1):
        result.extend(generate_partitions(n))
    return result

def restrict_partitions(part1_list, part2_list, d_lam):
    """
    Filters two lists of partitions (part1_list, part2_list) so that
    only pairs (a, b) satisfy |a| + |b| = |lam|, where |.| is the degree (sum of parts).
    """

    filtered_part1 = []
    filtered_part2 = []

    for a in part1_list:
        for b in part2_list:
            if sum(a) + sum(b) == d_lam:
                filtered_part1.append(a)
                filtered_part2.append(b)

    return filtered_part1, filtered_part2


# ----------------- Littlewood-Richardson Coefficient (2-Order) ------------------


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
        
    # Corner case for littlewood
    if mu == () and degree(nu) == degree(lam) and nu != lam:
        return 0
    if nu == () and degree(mu) == degree(lam) and mu != lam:
        return 0
    # naive enumeration for small cases
    entries = weight_to_list(nu)
    c = 0
    for perm in set(permutations(entries)):
        if is_yamanouchi(perm):
            c += 1
    return c

# ------------------ Solving System for Degrees of Partitions Lambda, Delta, and Values of P and Q -----------------
def solveOne(k, k1, k2, k3, k4):

    if k2 > k1 or k4 > k3:
        return []

    solutions = []

    for x1 in range(k + 1):

        max_x2 = math.floor((k - x1))
        range_Max = math.ceil((max_x2)/2 + 1)
        
        for x2 in range(range_Max):



            if range_Max == 0:

                sol1 = {
                "deg δ": x1,
                "deg γ": 0,
                "p": 0,
                "q": 0,
                "deg λ'": k2,
                "deg μ'": k4
                
                }
                solutions.append(sol1)

            x3 = k1 - k2 - (x1 + x2)
            x4 = k3 - k4 - (x1 + x2)

            if (x3 < 0 or x4 < 0):
                continue

            
            if (x1 + 2 * x2 + x3 + x4 != k) or (x1 + x2 + x3 != k1 - k2) + (x1 + x2 + x4 != k3 - k4):
                continue
            
            sol = {
                "deg δ": x1,
                "deg γ": x2,
                "p": x3,
                "q": x4,
                "deg λ'": k2,
                "deg μ'": k4
                }
            solutions.append(sol)

    return solutions


# --------------------- Littlewood Richardon Coefficient (Order 4) ---------------------------

def lrcoef4(mu1, mu2, mu3, mu4, lam):

    d_mu1 = degree(mu1)
    d_mu2 = degree(mu2)
    d_mu3 = degree(mu3)
    d_mu4 = degree(mu4)
    d_lam = degree(lam)
    
    total1 = d_mu1 + d_mu2                # degree of the first intermediate partition
    total2 = d_mu3 + d_mu4                # degree of the second intermediate partition

    parts_a = list(generate_partitions(total1))
    parts_b = list(generate_partitions(total2))
    parts_v1, parts_v2 = restrict_partitions(parts_a, parts_b, d_lam)

    s = 0
    i = 1
    for a in parts_a:

        i += 1


        
        for b in parts_b:
            N1 = int(lrcoefP(mu1, mu2, a))   # N^{a}_{mu1,mu2}
            
            if N1 == 0: 
                continue
    
            N2 = int(lrcoefP(mu3, mu4, b))   # N^{b}_{mu3,mu4}

            if N2 == 0:
                continue
            N3 = int(lrcoefP(a, b, lam))           # N^{lam}_{a,b}
            if N3 == 0:
                continue   
            s_term = N1 * N2 * N3
            s += s_term


    return s

# ------------------------------------- SOCLE METHOD -----------------------------------------

def CalcSoc(k, lam, lamP, mu, muP):
    """
    k1 = |lam|,   k3 = |mu|
    """

    k1 = degree(lam)
    k2 = degree(lamP)
    k3 = degree(mu)
    k4 = degree(muP)

    L = solveOne(k, k1, k2, k3, k4)
    # print(L)
    tot_sum = 0

    for sol in L:

        d_list = list(generate_partitions(sol["deg δ"]))
        g_list = list(generate_partitions(sol["deg γ"]))

        
        p = ones_partition(sol["p"])
        q = ones_partition(sol["q"])

        for d in d_list:
            for g in g_list:

                # lam
                term1 = lrcoef4(lamP, g, d, p, lam)

                # mu 
                term2 = lrcoef4(muP, g, d, q, mu)

                tot_sum += term1 * term2

    return tot_sum


# -------------------------- Master Method ------------------------

def Master(k, lam, lamP, mu, muP, ex_string = ''):
    print(f'''|-- Calc for {k+1}-th soc given partitions: --| \n 
            l = {lam}
            lP = {lamP}
            m = {mu}
            mP = {muP} \n
            k = {k} \n''')
    # print(solveOne(k, degree(lam), degree(lamP), degree(mu), degree(muP)))
    print(f'<<<<<<<<<<<<< {k + 1}-th Soc is : {CalcSoc(k, lam, lamP, mu, muP)} >>>>>>>>>>>>>\n')

# Soc4 for Lam = (1, 1) Mu = (1,1)
# Master(4, (1,1), (), (1,1), ())

if __name__ == '__main__':
    k = 1
    lam = (1, 1)
    mu = (1,)

    lamP = (2,)
    muP = ()
    #
    Master(k, lam, lamP, mu, muP)

