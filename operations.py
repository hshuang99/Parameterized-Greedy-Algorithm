import copy
import numpy as np
import random
#Define a inverse operation for binary matrix over F_{2}
def inv(mat):
    size = mat.shape[0]
    identity = np.eye(size, dtype=int)
    B = copy.deepcopy(mat)
    augmented = np.hstack((B, identity))
    for i in range(size):
        if augmented[i, i] == 0:
            for j in range(i+1, size):
                if augmented[j, i] == 1:
                    augmented[[i, j]] = augmented[[j, i]]
                    break
            else:
                raise ValueError("Matrix is not invertible in F_{2}")
        for k in range(size):
            if k != i and augmented[k, i] == 1:
                augmented[k, :] = np.logical_xor(augmented[k, :], augmented[i, :]).astype(int)
    if not np.array_equal(augmented[:, :size], np.eye(size, dtype=int)):
        raise ValueError("Matrix is not invertible in F_{2}")
    inverse = augmented[:, size:]
    return inverse
#The function execute the row operation for row i with row j
def row_i2j(mat, i, j):
    #copy the input matrix for calculate the row operation
    ret_mat = copy.deepcopy(mat)
    #select the rows i to xor with row j
    ret_mat[j, :] = np.logical_xor(ret_mat[i, :], ret_mat[j, :])
    #return the calculated matrix
    return ret_mat
#The function execute the column operation for row i with row j
def col_i2j(mat, i, j):
    #copy the input matrix for calculate the column operation
    ret_mat = copy.deepcopy(mat)
    #Find the column i has 1s
    for k in range(len(mat)):
        if ret_mat[k][i] == 1:
            ret_mat[k][j] = ret_mat[k][j] ^ 1 #flip the column j through xor with 1
    #return the calcualted matrix
    return ret_mat
def is_permutation_matrix(matrix):
    """
    Checks if a given matrix is a permutation matrix.
    Args:
        matrix M: A 2D list or NumPy array representing the matrix.
    Returns:
        True if the matrix is a permutation matrix, False otherwise.
    """
    # Check if each row has exactly one 1
    if not np.all(np.sum(matrix, axis=1) == 1):
        return False 
    # Check if each column has exactly one 1
    if not np.all(np.sum(matrix, axis=0) == 1):
        return False
    return True
def L_collection(L, visited, SIZE):
    for i in range(0, SIZE):
        if visited[i] == 1:
            continue
        for j in range(0, SIZE):
            if visited[j] == 1 or j == i:
                continue
            L.append((i, j))
    return L
def can_close_permutation(mat):
    for i in range(mat.shape[0]):
        if np.count_nonzero(mat[i]) > 2:
            return False
    column_counts = np.count_nonzero(mat, axis=0)
    if np.any(column_counts > 2):
        return False
    return True
def available_operator_execution(select_list, layer_r, layer_c, layers_r, layers_c, mat, inverse, row_op, col_op, row_visited, col_visited, depth, SIZE, close_permu):
    if len(select_list) == 0: #every time check the select list is empty
        if len(layer_r) > 0:
            layers_r.append(layer_r)
            layer_r = []
            row_visited = [0]*SIZE
        if len(layer_c) > 0:
            layers_c.append(layer_c)
            layer_c = []
            col_visited = [0]*SIZE
        if can_close_permutation(mat):
            close_permu = True
    else:
        rand = random.randint(0, len(select_list)-1)
        select_operator = select_list[rand] #for find the randomly operations on the select list
        i, j = select_operator[0], select_operator[1]
        if select_operator[2] == 0:
            mat = row_i2j(mat, i, j) #then execute the row operation
            inverse = col_i2j(inverse, j, i) #then inverse calculate select column
            layer_r.append((i, j, 0)) #append this opertion to layer r L_{r}
            row_op.append((i, j, 0)) #also record for the row operation list
            if sum(row_visited) == 0:
                depth += 1
            row_visited[i] = 1 #the control setting 1
            row_visited[j] = 1 #the target setting 1
            print("Currently Row operations:", row_op)
        else:
            mat = col_i2j(mat, i, j) #otherwise pick the column operation for matrix
            inverse = row_i2j(inverse, j, i) #and inverse execute the row operation
            layer_c.append((i, j, 1)) #append the operation as 1 to L_{c}
            col_op.append((i, j, 1)) #record the column operation on col op list
            if sum(col_visited) == 0:
                depth += 1
            col_visited[i] = 1 #on the col visi list record the control to 1
            col_visited[j] = 1 #also record 1 for target
            print("Currently Column operations:", col_op)
    return select_list, layer_r, layer_c, layers_r, layers_c, mat, inverse, row_op, col_op, row_visited, col_visited, depth, close_permu

def verify_layer_conflicts(layers):
    """
    Verify that no layer contains conflicting operations (same address in same layer).
    Returns True if all layers are conflict-free, False otherwise.
    """
    print("The layers in verify_layer_conflicts:", layers)
    for index, layer in enumerate(layers):
        used = set()
        for op in layer:
            if len(op) == 3:  # (i, j, type) format
                i, j, op_type = op[0], op[1], op[2]
                if i in used or j in used:
                    print(f"Conflict in layer {i}: row operation {op} conflicts with existing operations")
                    return False
                used.add(i)
                used.add(j)
                print("The used list:", used)
    print("All layers are conflict-free!")
    return True

def Verify(origin, layers, sequence, mat):
    try:
        '''
        Check layers that (1,1)...(N,N) which every single layer follow parallel ability
        '''
        SIZE = len(mat)
        # First verify that layers are conflict-free
        if not verify_layer_conflicts(layers):
            return False
            
        #get a signle layer from layers
        for layer in layers:
            layer_visited = [0]*SIZE
            #enumerate all tuple elements in sing layer
            for addr in layer:
                #check the elements address in visited layer, exist denotes violation parallel in single layer
                if layer_visited[addr[0]] or layer_visited[addr[1]]:
                    print(f"Layers contains duplicate elements, please check the layers.")
                    return False
                #otherwise operation did not use before, record it used.
                else:
                    layer_visited[addr[0]] = 1; layer_visited[addr[1]] = 1
        print(f"Layers has all unique elements.")
        '''
        Check recording operations can work on input matrix
        '''
        #read the sequence
        for seq in sequence:
            #execute row operation to input matrix
            if seq[2] == 0:
                origin = col_i2j(origin, seq[1], seq[0])
            #otherwise execute column operation
            else:
                origin = col_i2j(origin, seq[0], seq[1])
        print("The origin:")
        print(origin)
        print("The mat:")
        print(mat)
        #check the input matrix is same as mat after exection operations
        if (origin == mat).all():
            print("The operations is work")
            return True
        else:
            print("The operations are not work, origin is not equal mat")
            return False
    except Exception as e:
        print(f"An unexcept error occured: {e}")
