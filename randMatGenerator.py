import numpy as np
import sys

np.set_printoptions(threshold=sys.maxsize)

"""
Compute the inverse of a binary matrix over GF(2). 
Returns the inverse if it exists, else None.
"""
def gf2_inverse(bin_matrix):
    n = bin_matrix.shape[0]
    # Augment matrix with identity: [A | I]
    aug = np.hstack([bin_matrix.copy(), np.eye(n, dtype=int)]) % 2

    for col in range(n):
        # Find pivot row
        pivot = None
        for row in range(col, n):
            if aug[row, col] == 1:
                pivot = row
                break
        if pivot is None:
            return None  # Singular over GF(2)

        # Swap pivot row into place
        aug[[col, pivot]] = aug[[pivot, col]]

        # Eliminate all other rows with a 1 in this column
        for row in range(n):
            if row != col and aug[row, col] == 1:
                aug[row] = (aug[row] + aug[col]) % 2

    return aug[:, n:]  # Right half is the inverse

def main(n, rng_seed):
    while True:
        np.random.seed(rng_seed)
        bin_matrix = np.random.randint(0, 2, size=(n, n))
        inv = gf2_inverse(bin_matrix)
        if inv is not None:
            return bin_matrix, inv

if __name__ == "__main__":
    if len(sys.argv) == 3:
        n = int(sys.argv[1])
        rng_seed = int(sys.argv[2])
        bin_matrix, inv = main(n, rng_seed)
        print("Random Binary Matrix:\n", bin_matrix)
        print("\nGF(2) Inverse:\n", inv)

        # Verify: A @ A^-1 should be identity mod 2
        identity_check = (bin_matrix @ inv) % 2
        if np.array_equal(identity_check, np.eye(n, dtype=int)):
            print("\nVerified: A @ A^-1 = I (mod 2) ✅")
            np.savetxt(f'rand_matrix_{rng_seed}', bin_matrix, fmt='%d')
        else:
            print("\nVerification failed!")
    else:
        print(f"Usage: python3 {sys.argv[0]} <SIZE> <RANDOM SEED>")
        sys.exit(1)
