import operations
import selector
import configparser
import sys
from cost_function import functionCost
import numpy as np
from pathlib import Path

def rowGreedy(mat, inverse, fileName, L_r, L_c, Ls_r, Ls_c, row_op, col_op, p_value, over_depth, depth):
    SIZE = len(mat)
    minm_cost = sys.float_info.max
    LIMIT = sys.float_info.max
    config = configparser.ConfigParser(); config.optionxform = str; 
    if "RAND" not in fileName:
        config.read(Path("Config")/f'RowConfig_{fileName}.ini')
        LIMIT = int(config.get('DEPTH', 'rowLimit'))
    close_permu = False
    row_visi = [0]*SIZE; col_visi = [0]*SIZE

    while not operations.is_permutation_matrix(mat):
        print("\n=== Starting new iteration ===")
        print("Current depth:", depth)
        print("Current Row visited list:", row_visi)
        print("Current Col visited list:", col_visi)
        select_list = []
        L_row = []; L_col = []
        L_row_cst = []; L_col_cst = []

        minm_cost = functionCost(mat, inverse, p_value)

        print("Current Minimum Cost:", minm_cost)
                
        L_row = operations.L_collection(L_row, row_visi, SIZE)
        select_list, minm_cost = selector.ops_sel(L_row, L_row_cst, [], [], mat, inverse, p_value, minm_cost, select_list, 0)

        if not close_permu:
            L_col = operations.L_collection(L_col, col_visi, SIZE)
            select_list, minm_cost = selector.ops_sel([], [], L_col, L_col_cst, mat, inverse, p_value, minm_cost, select_list, 1)

        print("The select list and current minimum cost: ", select_list, minm_cost)

        select_list, L_r, L_c, Ls_r, Ls_c,  mat, inverse, row_op, col_op, row_visi, col_visi, depth, close_permu = operations.available_operator_execution(select_list, L_r, L_c, Ls_r, Ls_c, mat, inverse, row_op, col_op, row_visi, col_visi, depth, SIZE, close_permu)

        if depth > LIMIT: #the depth is over latest minimum depth
            print(f"Depth {depth} over minimum limit {LIMIT}, so break this iteration")
            over_depth = True
            return L_r, L_c, Ls_r, Ls_c, mat, row_op, col_op, depth, over_depth

    return L_r, L_c, Ls_r, Ls_c, mat, row_op, col_op, depth, over_depth
