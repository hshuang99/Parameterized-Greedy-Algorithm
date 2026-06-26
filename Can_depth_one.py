import numpy as np
import config
'''
The bool function to check whether matrix is close identity matrix
if close to identity then return True
otherwise return False
'''
def can_one(mat):
        #check each row that every Hamming Weight not over 2
	for i in range(mat.shape[0]):#Iterate through rows
		#Counting non-zeros for each row
		if np.count_nonzero(mat[i]) > 2:
			#cannot depth one if 
			return False

	#check each column that every Hamming Weight not over 2
	column_counts = np.count_nonzero(mat, axis=0)
	if np.any(column_counts > 2):
		return False
	#if row and column perspective Hamming Weight lower 2, then return True
	return True
