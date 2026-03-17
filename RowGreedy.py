import operations
import sys
import selector
import configparser
from cost_function import cost_mat
import numpy as np

def rowGreedy(mat, inverse, L_r, L_c, Ls_r, Ls_c, row_op, col_op, p_value, flag, depth):
    SIZE = len(mat)
    minm_cost = sys.float_info.max
    select_list = []
    row_visi = [0]*SIZE; col_visi = [0]*SIZE
    one = False
    config = configparser.ConfigParser(); config.optionxform = str; config.read('RowConfig.ini')
    LIMIT = int(config.get('DEPTH', 'rowLimit'))

    while not operations.is_permutation_matrix(mat):
        print("\n=== Starting new iteration ===")
        print("Current depth:", depth)
        print("Current Row visited list:", row_visi)
        print("Current Col visited list:", col_visi)
        select_list = []
        L_row = []; L_col = []
        L_row_cst = []; L_col_cst = []

        if p_value != "1":
            H_r = cost_mat(mat, p_value) + cost_mat(np.transpose(inverse), p_value)
            H_c = cost_mat(np.transpose(mat), p_value) + cost_mat(inverse, p_value)
            minm_cost = max(H_r, H_c)
        else:
            minm_cost = cost_mat(mat, p_value) + cost_mat(np.transpose(inverse), p_value)

        print("Current Minm Cost:", minm_cost)

        #if the matrix is not achieve can depth one property
        if not one:
            L_col = operations.L_collection(L_col, col_visi, SIZE)
            select_list, minm_cost = selector.available_col_operator_selection(L_col, L_col_cst, mat, inverse, p_value, minm_cost, select_list)
 
        L_row = operations.L_collection(L_row, row_visi, SIZE)
        select_list, minm_cost = selector.available_row_operator_selection(L_row, L_row_cst, mat, inverse, p_value, minm_cost, select_list)

        print("The select list and current minm cost: ", select_list, minm_cost)
                    
        select_list, L_r, L_c, Ls_r, Ls_c, mat, inverse, row_op, col_op, row_visi, col_visi, depth, one = operations.available_operator_execution(select_list, L_r, L_c, Ls_r, Ls_c, mat, inverse, row_op, col_op, row_visi, col_visi, depth, SIZE, one)  

        if depth > LIMIT:
            print(f"Depth {depth} over minimum limit {LIMIT}, so break this iteration")
            flag = True
            return L_r, L_c, Ls_r, Ls_c, mat, row_op, col_op, depth, flag

    return L_r, L_c, Ls_r, Ls_c, mat, row_op, col_op, depth, flag
