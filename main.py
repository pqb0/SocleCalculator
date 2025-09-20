# ------------------------------------------------------------
# 1.  Helper functions (the same ones you already have)
# ------------------------------------------------------------
def degree(partition):
    """Sum of the parts of a partition."""
    return sum(partition)


def generate_partitions(n, max_part=None):
    """Yield all integer partitions of n (order not important)."""
    if n == 0:
        yield ()
    else:
        if max_part is None or max_part > n:
            max_part = n
        for first in range(max_part, 0, -1):
            for rest in generate_partitions(n - first, first):
                yield (first,) + rest


def subset_partitions(partition):
    """All partitions whose total degree is ≤ |partition|."""
    d = degree(partition)
    result = []
    for n in range(d + 1):
        result.extend(generate_partitions(n))
    return result


# ------------------------------------------------------------
# 2.  Solver that respects the *chosen* λ′ and μ′
# ------------------------------------------------------------
def solve_system(k, k1, k2, k3, k4):
    """
    Solve the system

        2*x2 + x1 + x3 + x4 = k                (1)
        k1 - k2 = x2 + x1 + x3                  (2)
        k3 - k4 = x2 + x1 + x4                  (3)

    together with the bounds

        x1,x2,x3,x4 < k1   and   x1,x2,x3,x4 < k3
        k2 < k1 ,   k4 < k3   (these are assumed true, but are checked)

    Parameters
    ----------
    k  : int   – the constant that appears in (1)
    k1 : int   – |λ|
    k2 : int   – |λ'| (already chosen)
    k3 : int   – |μ|
    k4 : int   – |μ'| (already chosen)

    Returns
    -------
    list of dicts, each dict containing the six numbers
    {"deg δ":x1, "deg γ":x2, "p":x3, "q":x4,
     "deg λ'":k2, "deg μ'":k4}
    """
    # -----------------------------------------------------------------
    # 0.  sanity checks that are required by the statement
    # -----------------------------------------------------------------
    if not (k2 < k1 and k4 < k3):
        # the user supplied inadmissible degrees – nothing to do
        return []

    # -----------------------------------------------------------------
    # 1.  Derive x1 directly from (1) + (2) + (3)
    # -----------------------------------------------------------------
    # Adding (2) and (3) and subtracting (1) eliminates x2 completely:
    #   (k1 - k2) + (k3 - k4) - k = x1
    x1 = k1 - k2 + k3 - k4 - k
    if x1 < 0:                     # x1 must be non‑negative
        return []

    # -----------------------------------------------------------------
    # 2.  The remaining unknown is x2 ; once we know x2 we get x3,x4
    # -----------------------------------------------------------------
    # From (2)   :  x3 = (k1 - k2) - (x1 + x2)
    # From (3)   :  x4 = (k3 - k4) - (x1 + x2)
    # Both x3 and x4 must be ≥ 0, therefore
    #   x1 + x2 ≤ k1 - k2   and   x1 + x2 ≤ k3 - k4
    max_sum = min(k1 - k2, k3 - k4)      # the largest allowed value of (x1+x2)

    # The smallest possible sum is just x1 (when x2 = 0)
    if x1 > max_sum:                     # no room for a non‑negative x2
        return []

    solutions = []
    # x2 can range from 0 up to the value that keeps the sum ≤ max_sum
    max_x2 = max_sum - x1
    for x2 in range(max_x2 + 1):         # inclusive upper bound
        s = x1 + x2                       # s = x1 + x2

        x3 = (k1 - k2) - s
        x4 = (k3 - k4) - s

        # all variables must be non‑negative
        if x3 < 0 or x4 < 0:
            continue

        # condition (4): each of x1,x2,x3,x4 < k1 and < k3
        if not (x1 < k1 and x2 < k1 and x3 < k1 and x4 < k1):
            continue
        if not (x1 < k3 and x2 < k3 and x3 < k3 and x4 < k3):
            continue

        # everything checks out – store the solution
        solutions.append({
            "deg δ": x1,
            "deg γ": x2,
            "p":    x3,
            "q":    x4,
            "deg λ'": k2,
            "deg μ'": k4
        })

    return solutions



# ------------------------------------------------------------
# 3.  Minimal interactive driver (the “Master” part)
# ------------------------------------------------------------
def Master():
    # ----  INPUT λ and μ  ----------------------------------------
    lam = tuple(map(int, input("Enter λ (space‑separated parts): ").split()))
    mu  = tuple(map(int, input("Enter μ (space‑separated parts): ").split()))

    k1, k3 = degree(lam), degree(mu)
    print(f"\n|λ| = {k1}, |μ| = {k3}")

    # ----  show all partitions ≤ those degrees --------------------
    lam_subset = subset_partitions(lam)
    mu_subset  = subset_partitions(mu)

    print("\nPartitions with degree ≤ |λ|:")
    for i, p in enumerate(lam_subset):
        print(f"{i}: {p}")

    print("\nPartitions with degree ≤ |μ|:")
    for i, p in enumerate(mu_subset):
        print(f"{i}: {p}")

    # ----  user picks λ' and μ' ----------------------------------
    lam_choice = int(input("\nSelect index for λ': "))
    mu_choice  = int(input("Select index for μ': "))

    lam_prime = lam_subset[lam_choice]
    mu_prime  = mu_subset[mu_choice]

    k2 = degree(lam_prime)   # degree of the chosen λ'
    k4 = degree(mu_prime)    # degree of the chosen μ'

    print(f"\nChosen λ' = {lam_prime}, degree = {k2}")
    print(f"Chosen μ' = {mu_prime}, degree = {k4}")

    # ----  constant k -------------------------------------------
    k = int(input("\nEnter fixed constant k: "))

    # ----  solve -------------------------------------------------
    sols = solve_system(k, k1, k3, k2, k4)

    print(f"\nGiven k = {k}, |λ| = {k1}, |μ| = {k3}, "
          f"deg λ' = {k2}, deg μ' = {k4}, solutions are:")
    if not sols:
        print("❗  No solutions found – check the feasibility conditions.")
    else:
        for s in sols:
            print(s)


# ------------------------------------------------------------
# 4.  Run the demo
# ------------------------------------------------------------
if __name__ == "__main__":
    Master()
