import config

def generatePermutationMatrix(mat):
    permutationMatrix = [0]*config.SIZE
    for i in range(config.SIZE):
        for j in range(config.SIZE):
            if mat[i][j] == 1:
                permutationMatrix[i] = j
    print("The permutation matrix: ", permutationMatrix)
    return permutationMatrix

def generateSequence(op_type, row_operations, col_operations, permutationMatrix):
    sequence = []
    if op_type == 1:
        row_op = reversed(row_operations)
        for row_operator_seq in row_op:
            i = row_operator_seq
            sequence.append((permutationMatrix[i[0]], permutationMatrix[i[1]], 0))
    elif op_type == 2:
        for col_op in col_operations:
            col_operator_seq = col_op
            sequence.append((col_operator_seq[1], col_operator_seq[0], 1))
    elif op_type == 3:
        for i in col_operations:
            col_operator_seq = i
            sequence.append((col_operator_seq[1], col_operator_seq[0], 1))#append the column operaitons
    
        for row_operator_seq in reversed(row_operations):
            i = row_operator_seq
            sequence.append((permutationMatrix[i[0]], permutationMatrix[i[1]], 0))#store the row operations from permutation matrix
    print("The sequence:", sequence)
    return sequence

def generateLayers(op_type, layers_r, layers_c, permutationMatrix):
    layers = []
    if op_type == 1:
        layers_r.reverse()
    
        for lay_r in layers_r:
            nl_r = []
            for l_r in lay_r:
                nl_r.append((permutationMatrix[l_r[0]], permutationMatrix[l_r[1]], l_r[2]))
            if nl_r:
                layers.append(nl_r)
    elif op_type == 2:
        for lay_c in layers_c:
            nl_c = []
            for l_c in lay_c:
                nl_c.append((l_c[1], l_c[0], l_c[2]))
            if nl_c:
                layers.append(nl_c)
    elif op_type == 3:
        for lay_c in layers_c:
            nl_c = []
            for l_c in lay_c:
                nl_c.append((l_c[1], l_c[0], l_c[2]))
            if nl_c:
                layers.append(nl_c)

        layers_r.reverse()
        for lay_r in layers_r:
            nl_r = []
            for l_r in lay_r:
                nl_r.append((permutationMatrix[l_r[0]], permutationMatrix[l_r[1]], l_r[2]))
            if nl_r:
                layers.append(nl_r)

    print("All layers processed:", layers)
    return layers
