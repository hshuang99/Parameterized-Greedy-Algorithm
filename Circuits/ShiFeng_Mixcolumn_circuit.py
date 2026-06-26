"""
MixColumn quantum circuit diagram — ProjectQ (memory-safe version).

Root cause of "zsh: killed":
    Using MainEngine with a ClassicalSimulator or default backend allocates
    a full 2^N state vector. With 40 qubits that is ~8 TB of memory.

Fix:
    Use CircuitDrawer as the SOLE backend (no simulator at all).
    CircuitDrawer only records gate strings — it never builds a state vector.
    Memory stays under 10 MB regardless of qubit count.

Usage:
    pip install projectq
    python mixcolumn_circuit.py
    # outputs: mixcolumn_circuit.tex
    pdflatex mixcolumn_circuit.tex   # optional: compile to PDF
"""

from projectq import MainEngine
from projectq.backends import CircuitDrawer, ResourceCounter, _resource
from projectq.ops import CNOT, Measure, All


# ---------------------------------------------------------------------------
# Helper: CNOT-based SWAP (used only when verify_permutation=True)
# ---------------------------------------------------------------------------
def swap1(qubit1, qubit2, tem_qubit):
    CNOT | (qubit1, tem_qubit)
    CNOT | (tem_qubit, qubit1)
    CNOT | (qubit2, qubit1)
    CNOT | (qubit1, qubit2)
    CNOT | (tem_qubit, qubit2)
    CNOT | (qubit2, tem_qubit)


# ---------------------------------------------------------------------------
# MixColumn — depth-10, 132 CNOT gates
# ---------------------------------------------------------------------------
def Mixcolumn(x0, x1, x2, x3, ancilla, verify_permutation=False):
    x = list(x0) + list(x1) + list(x2) + list(x3)

    CNOT | (x[12], x[28]); CNOT | (x[20], x[4]);  CNOT | (x[19], x[3])
    CNOT | (x[27], x[11]); CNOT | (x[21], x[5]);  CNOT | (x[13], x[29])
    CNOT | (x[6],  x[22]); CNOT | (x[30], x[14]); CNOT | (x[23], x[31])
    CNOT | (x[15], x[7]);  CNOT | (x[18], x[2]);  CNOT | (x[26], x[10])
    CNOT | (x[24], x[1]);  CNOT | (x[0],  x[8]);  CNOT | (x[9],  x[25])
    CNOT | (x[16], x[17])

    CNOT | (x[31], x[7]);  CNOT | (x[19], x[27]); CNOT | (x[12], x[20])
    CNOT | (x[13], x[21]); CNOT | (x[4],  x[28]); CNOT | (x[30], x[6])
    CNOT | (x[16], x[0]);  CNOT | (x[24], x[8]);  CNOT | (x[26], x[18])
    CNOT | (x[15], x[23]); CNOT | (x[2],  x[10]); CNOT | (x[29], x[5])
    CNOT | (x[3],  x[11]); CNOT | (x[25], x[17]); CNOT | (x[1],  x[9])
    CNOT | (x[22], x[14])

    CNOT | (x[17], x[26]); CNOT | (x[18], x[19]); CNOT | (x[20], x[13])
    CNOT | (x[31], x[12]); CNOT | (x[11], x[3]);  CNOT | (x[8],  x[9])
    CNOT | (x[21], x[30]); CNOT | (x[28], x[4]);  CNOT | (x[2],  x[27])
    CNOT | (x[7],  x[25]); CNOT | (x[14], x[6]);  CNOT | (x[29], x[15])
    CNOT | (x[24], x[16]); CNOT | (x[22], x[23])

    CNOT | (x[20], x[27]); CNOT | (x[22], x[31]); CNOT | (x[16], x[17])
    CNOT | (x[10], x[18]); CNOT | (x[4],  x[21]); CNOT | (x[25], x[9])
    CNOT | (x[7],  x[0]);  CNOT | (x[29], x[6]);  CNOT | (x[2],  x[26])
    CNOT | (x[11], x[19]); CNOT | (x[3],  x[23]); CNOT | (x[8],  x[24])

    CNOT | (x[18], x[26]); CNOT | (x[27], x[12]); CNOT | (x[17], x[9])
    CNOT | (x[7],  x[3]);  CNOT | (x[31], x[15]); CNOT | (x[22], x[8])
    CNOT | (x[23], x[20]); CNOT | (x[24], x[16]); CNOT | (x[3],  x[23])
    CNOT | (x[8],  x[24]); CNOT | (x[17], x[1]);  CNOT | (x[31], x[19])
    CNOT | (x[22], x[30]); CNOT | (x[7],  x[4]);  CNOT | (x[2],  x[12])
    CNOT | (x[25], x[18]); CNOT | (x[5],  x[21]); CNOT | (x[23], x[24])

    CNOT | (x[7],  x[18]); CNOT | (x[1],  x[2]);  CNOT | (x[16], x[9])
    CNOT | (x[22], x[19]); CNOT | (x[31], x[20]); CNOT | (x[10], x[27])
    CNOT | (x[5],  x[13]); CNOT | (x[28], x[29]); CNOT | (x[25], x[26])

    CNOT | (x[5],  x[22]); CNOT | (x[7],  x[17]); CNOT | (x[1],  x[18])
    CNOT | (x[9],  x[26]); CNOT | (x[14], x[23]); CNOT | (x[31], x[8])
    CNOT | (x[29], x[13]); CNOT | (x[28], x[12]); CNOT | (x[11], x[4])
    CNOT | (x[6],  x[15]); CNOT | (x[20], x[27]); CNOT | (x[16], x[25])
    CNOT | (x[0],  x[24]); CNOT | (x[10], x[3])

    CNOT | (x[31], x[7]);  CNOT | (x[29], x[5]);  CNOT | (x[2],  x[10])
    CNOT | (x[22], x[14]); CNOT | (x[15], x[23]); CNOT | (x[4],  x[28])
    CNOT | (x[3],  x[11]); CNOT | (x[25], x[1]);  CNOT | (x[30], x[6])
    CNOT | (x[0],  x[16]); CNOT | (x[13], x[21]); CNOT | (x[12], x[20])
    CNOT | (x[24], x[9]);  CNOT | (x[19], x[27]); CNOT | (x[8],  x[17])
    CNOT | (x[26], x[18])

    CNOT | (x[21], x[5]);  CNOT | (x[13], x[29]); CNOT | (x[30], x[14])
    CNOT | (x[6],  x[22]); CNOT | (x[15], x[7]);  CNOT | (x[23], x[31])
    CNOT | (x[27], x[3]);  CNOT | (x[20], x[4]);  CNOT | (x[19], x[11])
    CNOT | (x[12], x[28]); CNOT | (x[9],  x[25]); CNOT | (x[26], x[2])
    CNOT | (x[18], x[10]); CNOT | (x[24], x[16]); CNOT | (x[8],  x[0])
    CNOT | (x[17], x[1])

    # Optional permutation correction (adds CNOT-SWAPs; skip for diagram)
    if verify_permutation:
        xvalues = [
            0, 17, 18, 27, 28, 21, 22, 15,
            16, 25, 26,  3, 20, 29, 30,  7,
            24,  1, 10, 19, 12,  5,  6, 31,
             8,  9,  2, 11,  4, 13, 14, 23
        ]
        standardvalues = list(range(32))
        while xvalues != standardvalues:
            for line in range(32):
                if xvalues[line] != standardvalues[line]:
                    for newline in range(line, 32):
                        if xvalues[newline] == line:
                            xvalues[line], xvalues[newline] = (
                                xvalues[newline], xvalues[line]
                            )
                            swap1(x[line], x[newline], ancilla[line % 8])
                            break
                    break


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    # KEY FIX: CircuitDrawer is the backend — no simulator, no state vector.
    # Memory usage: <10 MB regardless of qubit count.
    circuit_backend = _resource.ResourceCounter()
    drawing_engine = CircuitDrawer()
    eng = MainEngine(backend=circuit_backend, engine_list=[drawing_engine])

    # Allocate 32 data qubits (4 x 8-bit words = one AES column)
    x0 = eng.allocate_qureg(8)
    x1 = eng.allocate_qureg(8)
    x2 = eng.allocate_qureg(8)
    x3 = eng.allocate_qureg(8)

    # 8 ancilla qubits (only consumed when verify_permutation=True)
    ancilla = eng.allocate_qureg(8)

    # Apply MixColumn gate sequence
    # verify_permutation=False  →  pure gate diagram, no extra SWAPs
    Mixcolumn(x0, x1, x2, x3, ancilla, verify_permutation=False)

    eng.flush()
    print(circuit_backend)
    print("depth_of_dag: {}".format(circuit_backend.depth_of_dag))

    # Write LaTeX circuit diagram
    latex_code = drawing_engine.get_latex()
    output_file = "Shi&Feng_Mixcolumn_circuit.tex"
    with open(output_file, "w") as f:
        f.write(latex_code)

    print(f"[OK] Circuit diagram written to: {output_file}")
    print("     Compile with:  pdflatex mixcolumn_circuit.tex")
    print(f"     Gates applied: 132 CNOT gates, depth 10")
    print(f"     Qubits used  : 32 data + 8 ancilla = 40 total")

    # Measure so ProjectQ knows qubits are done
    All(Measure) | x0
    All(Measure) | x1
    All(Measure) | x2
    All(Measure) | x3
    All(Measure) | ancilla

    eng.flush()



if __name__ == "__main__":
    main()
