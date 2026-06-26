from projectq import MainEngine
from projectq.backends import ResourceCounter, _resource, ClassicalSimulator, CommandPrinter, CircuitDrawer
from projectq.meta import Uncompute, Compute, Dagger
from projectq.ops import H, Tdag, CNOT, T, X, S, Sdag, Toffoli, Measure, All, Allocate
import random



def bin2list(binary_num, n):
    binary_str = bin(binary_num)[2:].zfill(n)
    binary_list = [int(bit) for bit in binary_str]
    return binary_list


MixColumns_GF256 = [[0x2, 0x3, 0x1, 0x1],
                    [0x1, 0x2, 0x3, 0x1],
                    [0x1, 0x1, 0x2, 0x3],
                    [0x3, 0x1, 0x1, 0x2]]


def gf256_multiply(a, b):
    result = 0
    while b > 0:
        if b & 1:
            result ^= a
        a <<= 1
        if a & 0x100:
            a ^= 0x11B
        b >>= 1
    return result


def AES_MixColumns(State):
    result = [0] * 4
    for i in range(4):
        for j in range(4):
            result[i] ^= gf256_multiply(MixColumns_GF256[i][j], State[j])

    result_list = []
    for item in result:
        result_list += bin2list(item, 8)[::-1]
    return result_list


def MixColumns_Circuit(X):
    CNOT | (X[12], X[28])
    CNOT | (X[20], X[4])
    CNOT | (X[19], X[3])
    CNOT | (X[27], X[11])
    CNOT | (X[21], X[5])
    CNOT | (X[13], X[29])
    CNOT | (X[6], X[22])
    CNOT | (X[30], X[14])
    CNOT | (X[23], X[31])
    CNOT | (X[15], X[7])
    CNOT | (X[18], X[2])
    CNOT | (X[26], X[10])
    CNOT | (X[24], X[1])
    CNOT | (X[0], X[8])
    CNOT | (X[9], X[25])
    CNOT | (X[16], X[17])
    CNOT | (X[31], X[7])
    CNOT | (X[19], X[27])
    CNOT | (X[12], X[20])
    CNOT | (X[13], X[21])
    CNOT | (X[4], X[28])
    CNOT | (X[30], X[6])
    CNOT | (X[16], X[0])
    CNOT | (X[24], X[8])
    CNOT | (X[26], X[18])
    CNOT | (X[15], X[23])
    CNOT | (X[2], X[10])
    CNOT | (X[29], X[5])
    CNOT | (X[3], X[11])
    CNOT | (X[25], X[17])
    CNOT | (X[1], X[9])
    CNOT | (X[22], X[14])
    CNOT | (X[17], X[26])
    CNOT | (X[18], X[19])
    CNOT | (X[20], X[13])
    CNOT | (X[31], X[12])
    CNOT | (X[11], X[3])
    CNOT | (X[8], X[9])
    CNOT | (X[21], X[30])
    CNOT | (X[28], X[4])
    CNOT | (X[2], X[27])
    CNOT | (X[7], X[25])
    CNOT | (X[14], X[6])
    CNOT | (X[29], X[15])
    CNOT | (X[24], X[16])
    CNOT | (X[22], X[23])
    CNOT | (X[20], X[27])
    CNOT | (X[22], X[31])
    CNOT | (X[16], X[17])
    CNOT | (X[10], X[18])
    CNOT | (X[4], X[21])
    CNOT | (X[25], X[9])
    CNOT | (X[7], X[0])
    CNOT | (X[29], X[6])
    CNOT | (X[2], X[26])
    CNOT | (X[11], X[19])
    CNOT | (X[3], X[23])
    CNOT | (X[8], X[24])
    CNOT | (X[18], X[26])
    CNOT | (X[27], X[12])
    CNOT | (X[17], X[9])
    CNOT | (X[7], X[3])
    CNOT | (X[31], X[15])
    CNOT | (X[22], X[8])
    CNOT | (X[23], X[20])
    CNOT | (X[24], X[16])
    CNOT | (X[3], X[23])
    CNOT | (X[8], X[24])
    CNOT | (X[17], X[1])
    CNOT | (X[31], X[19])
    CNOT | (X[22], X[30])
    CNOT | (X[7], X[4])
    CNOT | (X[2], X[12])
    CNOT | (X[25], X[18])
    CNOT | (X[5], X[21])
    CNOT | (X[23], X[24])
    CNOT | (X[7], X[18])
    CNOT | (X[1], X[2])
    CNOT | (X[16], X[9])
    CNOT | (X[22], X[19])
    CNOT | (X[31], X[20])
    CNOT | (X[10], X[27])
    CNOT | (X[5], X[13])
    CNOT | (X[28], X[29])
    CNOT | (X[25], X[26])
    CNOT | (X[5], X[22])
    CNOT | (X[7], X[17])
    CNOT | (X[1], X[18])
    CNOT | (X[9], X[26])
    CNOT | (X[14], X[23])
    CNOT | (X[31], X[8])
    CNOT | (X[29], X[13])
    CNOT | (X[28], X[12])
    CNOT | (X[11], X[4])
    CNOT | (X[6], X[15])
    CNOT | (X[20], X[27])
    CNOT | (X[16], X[25])
    CNOT | (X[0], X[24])
    CNOT | (X[10], X[3])
    CNOT | (X[31], X[7])
    CNOT | (X[29], X[5])
    CNOT | (X[2], X[10])
    CNOT | (X[22], X[14])
    CNOT | (X[15], X[23])
    CNOT | (X[4], X[28])
    CNOT | (X[3], X[11])
    CNOT | (X[25], X[1])
    CNOT | (X[30], X[6])
    CNOT | (X[0], X[16])
    CNOT | (X[13], X[21])
    CNOT | (X[12], X[20])
    CNOT | (X[24], X[9])
    CNOT | (X[19], X[27])
    CNOT | (X[8], X[17])
    CNOT | (X[26], X[18])
    CNOT | (X[21], X[5])
    CNOT | (X[13], X[29])
    CNOT | (X[30], X[14])
    CNOT | (X[6], X[22])
    CNOT | (X[15], X[7])
    CNOT | (X[23], X[31])
    CNOT | (X[27], X[3])
    CNOT | (X[20], X[4])
    CNOT | (X[19], X[11])
    CNOT | (X[12], X[28])
    CNOT | (X[9], X[25])
    CNOT | (X[26], X[2])
    CNOT | (X[18], X[10])
    CNOT | (X[24], X[16])
    CNOT | (X[8], X[0])
    CNOT | (X[17], X[1])
 

def Format_Input(binary_list, Input):
    for i in range(32):
        if binary_list[i] == 1:
            X | Input[i]


def Format_Output(Output):
    binary_str = ''.join(map(str, Output)) 
    binary_num = int(binary_str, 2)
    return "0x{:08X}".format(binary_num)

if __name__ == "__main__":
    CORRECTNESS_CHECK = 0
    RESOURCE_CHECK = 1


    """---------------Correctness Check--------------"""
    if CORRECTNESS_CHECK == 1:
        eng = MainEngine(backend=ClassicalSimulator())

        for i in range(10):
            random_state = [random.getrandbits(8) for _ in range(4)]
            input_x = []
            for item in random_state:
                input_x += bin2list(item, 8)[::-1]

            State = eng.allocate_qureg(32)
            Format_Input(input_x, State)

            MixColumns_Circuit(State)
            All(Measure) | State

            output_standard = AES_MixColumns(random_state)
            output_circuit = [int(qubit) for qubit in State]

            print('-' * 51)
            print('Multiply by MixColumn_GF256:\t\t', Format_Output(output_standard))
            print("Output of Quantum Circuit:\t\t", Format_Output(output_circuit))

            eng.flush()

    """----------------Resource Check---------------"""
    if RESOURCE_CHECK == 1:
        print("# Quantum Resource Estimation of MixColumn Matrix")
        circuit_backend = _resource.ResourceCounter()
        drawing_engine = CircuitDrawer()
        eng = MainEngine(backend=circuit_backend, engine_list=[drawing_engine])

        State = eng.allocate_qureg(32)
        MixColumns_Circuit(State)
        eng.flush()


        print(circuit_backend)
        print("depth_of_dag: {}".format(circuit_backend.depth_of_dag))

        # get_latex() already returns a full standalone document — write it directly
        with open(f"MixColumn_In_Place_depth_{format(circuit_backend.depth_of_dag)}.tex", "w") as f:
            f.write(drawing_engine.get_latex())
