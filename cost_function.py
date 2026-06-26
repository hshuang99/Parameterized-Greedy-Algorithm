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
                HammingWeight = 0.0
                for j in range(0, SIZE): #column
                    if mat[i][j]: #non-zero entry
                        HammingWeight +=  mat[i][j]
            ret += HammingWeight ** 2
            return ret
        case "3":
            identity = np.identity(SIZE)
            ret = float(np.sum(np.logical_xor(mat, identity).astype(int)))
            return ret

def functionCost(mat, inverse, p):
    if p != "1" or "3":
        H_r = cost_mat(mat, p) + cost_mat(np.transpose(inverse), p)
        H_c = cost_mat(np.transpose(mat), p) + cost_mat(inverse, p)
        minm_cost = max(H_r, H_c)
    else:
        minm_cost = cost_mat(mat, p) + cost_mat(inverse, p)
    return minm_cost

def operationCost(mat, inverse, p, op):
    if p != "1" or "3":
        if op == "0":
            cost = cost_mat(mat, p) + cost_mat(np.transpose(inverse, p))
        else:
            cost = cost_mat(np.transpose(mat), p) + cost_mat(inverse, p)
    else:
        cost = cost_mat(mat, p) + cost_mat(inverse, p)
    return cost
