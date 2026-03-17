import operations
from cost_function import cost_mat
import sys
import selector
import configparser
import numpy as np

def row_or_Col(mat, inverse, L_r, L_c, Ls_r, Ls_c, row_op, col_op, p_value, flag, depth):
    SIZE = len(mat)
    minm_cost = sys.float_info.max; best_row_cst = sys.float_info.max; best_col_cst = sys.float_info.max
    one = False
    select_list = []
    row_visi = [0]*SIZE; col_visi = [0]*SIZE
    config = configparser.ConfigParser(); config.optionxform = str; config.read('row_or_Col_Config.ini')
    LIMIT = int(config.get('DEPTH', 'row_or_Col_Limit'))

    stuck_counter = 0; max_stuck_iterations = 3

    #go through the matrix and execute the row operations
    #outter while check matrix whether permutation
    while not operations.is_permutation_matrix(mat):
        print("\n=== Starting new iteration ===")
        print("Current depth:", depth)
        print("Stuck counter:", stuck_counter)
        print("Row visited:", row_visi)
        print("Col visited:", col_visi)
        L_row = []; L_col = []
        select_list = []
        L_row_cst = []; L_col_cst = []
        B_row = []; B_col = []

        if p_value != "1":
            H_r = cost_mat(mat, p_value) + cost_mat(np.transpose(inverse), p_value)
            H_c = cost_mat(np.transpose(mat), p_value) + cost_mat(inverse, p_value)
            minm_cost = max(H_r, H_c)
        else:
            minm_cost = cost_mat(mat, p_value) + cost_mat(np.transpose(inverse), p_value)

        print("Current cost:", minm_cost)

        L_row = operations.L_collection(L_row, row_visi, SIZE)
        B_row, best_row_cst, minm_cost = selector.modified_available_row_operator_selection(L_row, L_row_cst, mat, inverse, p_value, minm_cost, best_row_cst, B_row)

        L_col = operations.L_collection(L_col, col_visi, SIZE)
        B_col, best_col_cst, minm_cost = selector.modified_available_col_operator_selection(L_col, L_col_cst, mat, inverse, p_value, minm_cost, best_col_cst, B_col)

        print("The B_row and best_row_cst:", B_row, best_row_cst)
        print("The B_col and best_col_cst:", B_col, best_col_cst)

        is_stuck = len(B_row) == 0 and len(B_col) == 0

        if is_stuck:
            stuck_counter += 1
            print(f"WARNING: Local minima detected! Stuck counter: {stuck_counter}/{max_stuck_iterations}")
        else:
            stuck_counter = 0

        if stuck_counter >= max_stuck_iterations or (is_stuck and sum(row_visi) == 0 and sum(col_visi) == 0):
            print("=== ESCAPING LOCAL MINIMA ===")

            escapeCandidates = []

            escapeCandidates = selector.avoid_localMinima_available_row_operator_selection(L_row, mat, inverse, p_value, escapeCandidates)

            escapeCandidates = selector.avoid_localMinima_available_col_operator_selection(L_col, mat, inverse, p_value, escapeCandidates)

            if len(escapeCandidates) > 0:
                escapeCandidates.sort(key=lambda x: x[0])
                best_escape = escapeCandidates[0]

                print(f"The best_escape: {best_escape}")

                print(f"Escaping with operation: ({best_escape[1]}, {best_escape[2]}, {best_escape[3]})")
                print(f"Accepting cost increase from {minm_cost} to {best_escape[0]}")

                select_list = [(best_escape[1], best_escape[2], best_escape[3])]
                minm_cost = best_escape[0]
                stuck_counter = 0
            else:
                # No operations available at all - should not happen
                print("CRITICAL: No operations available. Breaking out of loop.")
                break
        else:
            if best_row_cst < best_col_cst:
                select_list = B_row
                minm_cost = best_row_cst
            elif best_row_cst > best_col_cst:
                select_list = B_col
                minm_cost = best_col_cst
            else:
                select_list = B_col if len(B_col) > 0 else B_row
                minm_cost = best_col_cst if len(select_list) > 0 else minm_cost

        print("The select list and current minm cost:", select_list, minm_cost)
        
        select_list, L_r, L_c, Ls_r, Ls_c, mat, inverse, row_op, col_op, row_visi, col_visi, depth, one = operations.available_operator_execution(select_list, L_r, L_c, Ls_r, Ls_c, mat, inverse, row_op, col_op, row_visi, col_visi, depth, SIZE, one)

        if depth > LIMIT:
            print(f"Depth {depth} over minimum limit {LIMIT}, so break this iteration")
            flag = True
            return L_r, L_c, Ls_r, Ls_c, mat, row_op, col_op, depth, flag

    return L_r, L_c, Ls_r, Ls_c, mat, row_op, col_op, depth, flag
