import operations
from cost_function import operationCost
import numpy as np
"""
All available operations from L_row or L_col to select the operator can reduce current cost depends on operator type.
Args:
    Large row list, Large row op cost list, Large column list, Large column op cost list, matrix M, inverse M', p value, minimum cost, select list, operator type
Returns:
    select list, minimum cost
"""
def ops_sel(L_row, L_row_cst, L_col, L_col_cst, mat, inverse, p_value, minm_cost, select_list, op_type):
    #running row operator if op_type is 0
    if op_type == 0:
        #select row operator from Large row list
        for row_op in L_row:
            #calculate row operator against M
            tmp_row_mat = operations.row_i2j(mat, row_op[0], row_op[1])
            #calculate row operator against M'
            tmp_row_inverse = operations.col_i2j(inverse, row_op[1], row_op[0])
            #calculate the cost for M and M' then collect it
            L_row_cst.append(operationCost(tmp_row_mat, tmp_row_inverse, p_value, 0))
        #enumerate the Large row cost list to find each operator
        for index, row_op_cst in enumerate(L_row_cst):
            #check the operator cost is less than current minimum cost
            if row_op_cst < minm_cost:
                #clearing the select list
                select_list = []
                #insert the operator to select list
                select_list.append((L_row[index][0], L_row[index][1], 0))
                #update the current minimum cost
                minm_cost = row_op_cst
            #otherwise, accept operator that cost is equal to current minimum cost which is using for prevent local minimum condition
            elif row_op_cst == minm_cost:
                #insert the row operator directly
                select_list.append((L_row[index][0], L_row[index][1], 0))
    #running column operator if op_type is 1
    else:
        #select column operator from Large column list
        for col_op in L_col:
            #calculate column operator against M
            tmp_col_mat = operations.col_i2j(mat, col_op[0], col_op[1])
            #calculate column operator against M'
            tmp_col_inverse = operations.row_i2j(inverse, col_op[1], col_op[0])
            #calculate the cost for M and M' then collect it
            L_col_cst.append(operationCost(tmp_col_mat, tmp_col_inverse, p_value, 1))
        #enumerate Large column list to find each operator
        for index, col_op_cst in enumerate(L_col_cst):
            #check the operator cost is less than current minimum cost
            if col_op_cst < minm_cost:
                #clearing select list
                select_list = []
                #insert the operator to select list
                select_list.append((L_col[index][0], L_col[index][1], 1))
                #update the current minimum cost
                minm_cost = col_op_cst
            #otherwise, accept operaotr that cost is equal to current minimum cost which is using for prevent local minimum condition
            elif col_op_cst == minm_cost:
                #insert the column operator directly
                select_list.append((L_col[index][0], L_col[index][1], 1))
    #return the select list and current minimum cost
    return select_list, minm_cost
"""
If the greedy algorithm fails into local minimum condition, then we decide adopt randomly operator that allow increase cost to escape this condition.
The criteria is over 3 times threshold that not find any available operator then trigger this kind of selection approach.
Input: Large row list, Large column list, Matrix M, Inverse M', p value, Escape Candidates, operator type
Output: Escape Candidates List
"""
def rand_ops_sel(L_row, L_col, mat, inverse, p_value, escapeCandidates, op_type):
    #execute row operator if operator type is 0
    if op_type == 0:
        #select row operator from Large row list
        for op_row in L_row:
            #calculate row operator against M
            tmp_row_mat = operations.row_i2j(mat, op_row[0], op_row[1])
            #calculate row operator against M'
            tmp_row_inv = operations.col_i2j(inverse, op_row[1], op_row[0])
            #calculate the row cost for M and M'
            tmp_row_cst = operationCost(tmp_row_mat, tmp_row_inv, p_value, 0)
            #insert the operator and current M to escape candidate list
            escapeCandidates.append((tmp_row_cst, op_row[0], op_row[1], 0))
    #execute column operator if operator type is 1
    else:
        #select column operator from Large column list
        for op_col in L_col:
            #calculate column operator against M
            tmp_col_mat = operations.col_i2j(mat, op_col[0], op_col[1])
            #calculate column operator against M'
            tmp_col_inv = operations.row_i2j(inverse, op_col[1], op_col[0])
            #calculate column cost for M and M'
            tmp_col_cst = operationCost(tmp_col_mat, tmp_col_inv, p_value, 1)
            #insert operator and current M to escape candiate list
            escapeCandidates.append((tmp_col_cst, op_col[0], op_col[1], 1))
    #return the escape candidate list
    return escapeCandiates
