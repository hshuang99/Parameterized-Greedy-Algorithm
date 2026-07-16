import numpy as np
from projectq import MainEngine
from projectq.ops import X, CNOT, H, T, Tdag
from projectq.backends import ResourceCounter, CircuitDrawer
from projectq.cengines import BasicEngine


# =========================
# Toffoli decomposition (7T + Clifford)
# =========================
def toffoli_7T(eng, a, b, c):
    """
    CCX(a,b -> c) Clifford+T decomposition with 7 T/Tdag gates (no ancilla).
    (CNOT count changes automatically because CCX is expanded.)
    """
    H | c

    CNOT | (b, c)
    Tdag | c
    CNOT | (a, c)
    T | c
    CNOT | (b, c)
    Tdag | c
    CNOT | (a, c)

    T | b
    T | c

    H | c

    CNOT | (a, b)
    T | a
    Tdag | b
    CNOT | (a, b)


# =========================
# KLEIN LIGHTER-R S-box (in-place, 4 qubits) with CCX decomposed
# Target bitsliced: 368E C497 A674 9E43
# =========================
def klein_lighter_r_sbox_clt(eng, b):
    F0 = b[1]
    F1 = b[0]
    F2 = b[2]
    F3 = b[3]

    toffoli_7T(eng, F3, F0, F2)
    CNOT | (F3, F0)
    CNOT | (F3, F2)

    toffoli_7T(eng, F2, F1, F3)
    CNOT | (F1, F0)

    toffoli_7T(eng, F3, F1, F0)
    toffoli_7T(eng, F2, F0, F1)

    X | F0
    X | F1

    CNOT | (F0, F3)
    CNOT | (F3, F1)

    toffoli_7T(eng, F3, F0, F2)

    CNOT | (F0, F2)
    CNOT | (F1, F0)

    return [F0, F1, F2, F3]


# =========================
# Round components (state is 64 qubits = 16 nibbles)
# =========================
def add_round_key(eng, state64, rk64):
    for i in range(64):
        CNOT | (rk64[i], state64[i])

def subnibbles_klein64(eng, state64):
    out = list(state64)
    for i in range(16):
        nib = out[4*i:4*i+4]
        out[4*i:4*i+4] = klein_lighter_r_sbox_clt(eng, nib)
    return out

def rotate_nibbles_logical(state64):
    nibs = [state64[4*i:4*i+4] for i in range(16)]
    nibs = nibs[4:] + nibs[:4]
    return [q for nib in nibs for q in nib]


# =========================
# MixNibbles (exact Rijndael MixColumns on 2 columns) - CNOT only
# Layout: byte k = state64[8*k : 8*k+8], LSB-first.
# =========================
def _byte_to_bits(x): return [(x >> i) & 1 for i in range(8)]
def _bits_to_byte(bits): return sum((bits[i] & 1) << i for i in range(8))

def _xtime(b):
    b2 = (b << 1) & 0xFF
    if b & 0x80:
        b2 ^= 0x1B
    return b2

def _mul(b, c):
    if c == 1: return b
    if c == 2: return _xtime(b)
    if c == 3: return _xtime(b) ^ b
    raise ValueError

def _mixcolumn_bytes(col4):
    a0, a1, a2, a3 = col4
    return [
        _mul(a0,2) ^ _mul(a1,3) ^ _mul(a2,1) ^ _mul(a3,1),
        _mul(a0,1) ^ _mul(a1,2) ^ _mul(a2,3) ^ _mul(a3,1),
        _mul(a0,1) ^ _mul(a1,1) ^ _mul(a2,2) ^ _mul(a3,3),
        _mul(a0,3) ^ _mul(a1,1) ^ _mul(a2,1) ^ _mul(a3,2),
    ]

def _build_mixcol_matrix_32():
    A = np.zeros((32, 32), dtype=np.uint8)
    for i in range(32):
        xbits = [0]*32
        xbits[i] = 1
        col = []
        for b in range(4):
            col.append(_bits_to_byte(xbits[8*b:8*b+8]))
        out = _mixcolumn_bytes(col)
        outbits = []
        for b in range(4):
            outbits += _byte_to_bits(out[b])
        for r in range(32):
            A[r, i] = outbits[r]
    return A

def _gauss_jordan_ops_to_I(A):
    A = A.copy().astype(np.uint8)
    n = A.shape[0]
    ops = []
    for p in range(n):
        piv = None
        for rr in range(p, n):
            if A[rr, p]:
                piv = rr
                break
        if piv is None:
            raise ValueError("Singular matrix (unexpected).")
        if piv != p:
            A[[p, piv]] = A[[piv, p]]
            ops.append(('swap', p, piv))
        for rr in range(n):
            if rr != p and A[rr, p]:
                A[rr] ^= A[p]
                ops.append(('rowxor', p, rr))
    return ops

_MIXCOL_OPS = _gauss_jordan_ops_to_I(_build_mixcol_matrix_32())

def mixcolumn_cnot_inplace(eng, col32):
    q = list(col32)
    for op in reversed(_MIXCOL_OPS):
        if op[0] == 'swap':
            i, j = op[1], op[2]
            q[i], q[j] = q[j], q[i]   # logical swap
        else:
            src, dst = op[1], op[2]
            CNOT | (q[src], q[dst])
    return q

def mixnibbles_klein64(eng, state64):
    left = state64[0:32]
    right = state64[32:64]
    left2 = mixcolumn_cnot_inplace(eng, left)
    right2 = mixcolumn_cnot_inplace(eng, right)
    return left2 + right2


# =========================
# Key schedule for KLEIN-64 (on-the-fly), on 64 qubits = 8 bytes
# bytes are LSB-first bit lists.
# =========================
def _split_bytes_8(key64):
    return [key64[8*i:8*i+8] for i in range(8)]

def _join_bytes_8(bytes8):
    return [q for b in bytes8 for q in b]

def _xor_bytes_inplace(eng, src_byte, dst_byte):
    for k in range(8):
        CNOT | (src_byte[k], dst_byte[k])

def _apply_sbox_to_byte(eng, byte8):
    low = byte8[0:4]
    high = byte8[4:8]
    low2 = klein_lighter_r_sbox_clt(eng, low)
    high2 = klein_lighter_r_sbox_clt(eng, high)
    return low2 + high2

def key_schedule_klein64(eng, key64, round_i):
    bytes8 = _split_bytes_8(key64)
    a = bytes8[0:4]
    b = bytes8[4:8]

    a1 = a[1:] + a[:1]
    b1 = b[1:] + b[:1]

    left = b1
    right = list(a1)
    for j in range(4):
        _xor_bytes_inplace(eng, left[j], right[j])

    ctr = round_i & 0xFF
    for k in range(8):
        if (ctr >> k) & 1:
            X | left[2][k]

    right[1] = _apply_sbox_to_byte(eng, right[1])
    right[2] = _apply_sbox_to_byte(eng, right[2])

    return _join_bytes_8(left + right)


# =========================
# One round (with provided round key)
# =========================
def klein_round_1(eng, state64, rk64):
    add_round_key(eng, state64, rk64)
    s1 = subnibbles_klein64(eng, state64)
    s2 = rotate_nibbles_logical(s1)
    s3 = mixnibbles_klein64(eng, s2)
    return s3


# =========================
# Full KLEIN-64 encryption: 16 rounds + final AddRoundKey
# (with key schedule each round)
# =========================
def klein64_encrypt_16r(eng, state64, master_key64):
    s = list(state64)
    k = list(master_key64)
    for r in range(1, 17):          # <-- 16 rounds
        s = klein_round_1(eng, s, k)
        k = key_schedule_klein64(eng, k, r)
    add_round_key(eng, s, k)        # final whitening with sk_{17}
    return s


# =========================
# Run: gate counts (16 rounds)
# =========================
def run_full_16round_with_keyschedule_clt():
    rc = ResourceCounter()
    eng1 = MainEngine(backend=rc)
    state = eng1.allocate_qureg(64)
    mk = eng1.allocate_qureg(64)
    _ = klein64_encrypt_16r(eng1, state, mk)
    eng1.flush()
    print("=== TOTAL (16 rounds + key schedule + final AddRoundKey), Toffoli decomposed ===")
    print(rc)

def run_1round():
    rc = ResourceCounter()
    eng1 = MainEngine(backend=rc)
    state = eng1.allocate_qureg(64)
    rk = list(eng1.allocate_qureg(64))
    _ = klein_round_1(eng1, state, rk)
    print("--- One Round ---")
    print(rc)

def draw_MixNibbles_circuit():
    dw = CircuitDrawer()
    eng = MainEngine(backend=dw)
    nib = eng.allocate_qureg(64)
    results = mixnibbles_klein64(eng, nib)
    eng.flush()
    with open("Circuits/origin_MixNibbles_circuit.tex", "w") as f:
        f.write(dw.get_latex())

if __name__ == "__main__":
    run_1round()
    draw_MixNibbles_circuit()
    #run_full_16round_with_keyschedule_clt()
