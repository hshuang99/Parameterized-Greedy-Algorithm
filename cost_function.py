import numpy as np
import math

def cost_mat(mat, p):
    ret = 0.0
    SIZE = len(mat)
    match p:
        case "-1": #log from Brugière: Gaussian elimination versus greedy methods for the synthesis of linear reversible circuits
            row_counts = np.sum(mat, axis=1)
            non_zero_counts = row_counts[row_counts > 0]
            ret = np.sum(np.log2(non_zero_counts))
            return ret
        case "1": #sum: from Brugière: Gaussian elimination versus greedy methods for the synthesis of linear reversible circuits
            for i in range(SIZE):
                for j in range(SIZE):
                    ret += mat[i][j]
            return ret
        case "2":#square: from Shi and Feng: Quantum Circuits of AES with a Low-depth Linear Layer and a New Structure
            for i in range(0, SIZE):
                hammingWeight = 0.0
                for j in range(0, SIZE): #column
                    if mat[i][j]: #non-zero entry
                        hammingWeight +=  mat[i][j]
                ret += hammingWeight ** 2
            return ret
        case "3": #cube
            for i in range(0, SIZE):
                hammingWeight = 0.0
                for j in range(0, SIZE): #column
                    if mat[i][j]: #non-zero entry
                        hammingWeight +=  mat[i][j]
                ret += hammingWeight ** 3
            return ret
        case "4": #fourth
            for i in range(0, SIZE):
                hammingWeight = 0.0
                for j in range(0, SIZE): #column
                    if mat[i][j]: #non-zero entry
                        hammingWeight +=  mat[i][j]
                ret += hammingWeight ** 4
            return ret
        case "5":
            I = np.eye(SIZE)
            P = np.random.permutation(I)
            ret = float(np.sum(np.logical_xor(mat, P)))
            return ret
