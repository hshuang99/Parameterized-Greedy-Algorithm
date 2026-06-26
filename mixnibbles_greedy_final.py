"""
KLEIN MixNibbles greedy-optimised CNOT circuit.
119 CNOTs per 4-byte column  (orig code: 312, Shi & Feng: 131)
Input wire relabelling by col_perm is FREE (zero gate cost).
Verified: reversed ops on permutation P reconstructs M32.

Savings over original code:
  KLEIN-64/64 (12 rounds): 7488 → 2856  CNOTs (−4632, −61%)
  KLEIN-64/80 (16 rounds): 9984 → 3808  CNOTs (−6176, −61%)
  KLEIN-64/96 (20 rounds): 12480 → 4760 CNOTs (−7720, −61%)
"""
import numpy as np

# Row ops: (ctrl, tgt) — each reduces M32 one step toward permutation P
_ROW_OPS = [[13, 21], [21, 5], [5, 29], [22, 6], [29, 6], [30, 14], [29, 14], [6, 30], [14, 22], [22, 13], [24, 16], [16, 0], [8, 16], [0, 9], [9, 17], [17, 25], [15, 23], [6, 15], [7, 15], [15, 16], [31, 7], [14, 23], [14, 7], [23, 0], [7, 24], [0, 24], [0, 1], [16, 24], [23, 25], [15, 25], [16, 25], [23, 11], [8, 17], [1, 17], [7, 17], [16, 1], [15, 1], [24, 17], [24, 9], [25, 9], [9, 1], [17, 9], [23, 8], [16, 8], [24, 8], [23, 31], [18, 10], [9, 18], [10, 26], [2, 10], [26, 2], [1, 26], [25, 26], [25, 10], [17, 10], [17, 18], [18, 2], [7, 19], [26, 18], [10, 18], [11, 3], [18, 11], [3, 19], [29, 21], [15, 3], [28, 20], [20, 4], [27, 28], [4, 12], [7, 27], [3, 27], [2, 27], [10, 27], [10, 11], [15, 20], [12, 28], [5, 12], [12, 13], [13, 30], [30, 14], [14, 31], [31, 15], [31, 7], [13, 21], [15, 23], [19, 28], [28, 4], [4, 21], [21, 6], [21, 30], [21, 14], [19, 11], [26, 20], [11, 20], [2, 20], [3, 11], [11, 28], [20, 12], [4, 12], [28, 20], [28, 4], [12, 22], [21, 22], [21, 13], [13, 29], [12, 13], [22, 29], [12, 5], [28, 5], [27, 11], [23, 11], [15, 11], [11, 3], [26, 3], [2, 3], [26, 19], [10, 19], [15, 19], [23, 19]]

# Input-wire permutation (free relabeling, 0 extra gates)
_COL_PERM = [8, 9, 18, 3, 12, 4, 22, 31, 24, 17, 26, 11, 29, 5, 30, 15, 0, 25, 10, 27, 20, 6, 21, 23, 16, 1, 2, 19, 28, 13, 14, 7]


def _build_M32():
    def gfmul(a, b):
        p=0
        for _ in range(8):
            if b&1: p^=a
            hb=a&0x80; a=(a<<1)&0xFF
            if hb: a^=0x1B
            b>>=1
        return p
    MDS=[[2,3,1,1],[1,2,3,1],[1,1,2,3],[3,1,1,2]]
    A=np.zeros((32,32),dtype=np.uint8)
    for br in range(4):
        for r in range(8):
            for bc in range(4):
                for c in range(8):
                    A[br*8+r,bc*8+c]=(gfmul(MDS[br][bc],1<<c)>>r)&1
    return A


def _selftest():
    M=_build_M32()
    A=M.copy()
    for i,j in _ROW_OPS: A[j]^=A[i]
    is_p=bool((A.sum(1)==1).all() and (A.sum(0)==1).all())
    st=A.copy()
    for i,j in reversed(_ROW_OPS): st[j]^=st[i]
    return is_p and np.array_equal(st,M)


def mixcolumn_cnot_inplace(eng, col32):
    """
    Apply KLEIN MixNibbles / AES MixColumns to 32 qubits (one 4-byte column).
    Uses 119 CNOTs (greedy row-only, vs 312 in original code).
    Input wires are remapped by _COL_PERM at zero cost (free wire relabeling).
    """
    from projectq.ops import CNOT
    q = [col32[_COL_PERM[i]] for i in range(32)]
    for i, j in reversed(_ROW_OPS):
        CNOT | (q[i], q[j])
    return list(col32)


def mixnibbles_klein64(eng, state64):
    left  = mixcolumn_cnot_inplace(eng, state64[0:32])
    right = mixcolumn_cnot_inplace(eng, state64[32:64])
    return left + right


if __name__ == "__main__":
    ok = _selftest()
    print(f"Self-test: {ok}")
    print(f"CNOTs/column: {len(_ROW_OPS)}  (orig 312)")
