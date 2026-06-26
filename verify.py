import config
import operations
import copy
'''
This function is used to verify whether the operations work
'''
def Verify(mat, select):
	#define a verify matrix which copy the input matrix cause we need modify it so can not just use shallow copy
	verify = copy.deepcopy(mat)
	
	#This variable is used to stroe the sequence data
	seq_data_list = []
	#Then open the sequence file depends on selection
	if select == 0:
		seq_file = open(config.sq_Seq_File, "r")
	elif select == 1:
		seq_file = open(config.prod_Seq_File, "r")

	#Readline with seq_file
	for line in seq_file:
		if not line.strip():
			continue
		#Separate each space in the line
		seq_data = line.split()
		#if read the CNOT in the line then break
		if seq_data and seq_data[0] == 'CNOT:':
			break
		#Insert the tuple element into list
		seq_data_list.append(seq_data)

	#Execution the operations from sequence list
	for op in seq_data_list:
		if int(op[2]) == 0:
			verify = operations.col_i2j(verify, int(op[1]), int(op[0]))
		elif int(op[2]) == 1:
			verify = operations.col_i2j(verify, int(op[1]), int(op[0]))
	
	if select == 0:
		print("The permutation matrix after exection all square operations is:")
	elif select == 1:
		print("The permutation matrix after exection all product operations is:")
	print(verify)
	permutation = [0]*config.SIZE
	
	for i in range(config.SIZE):
		for j in range(config.SIZE):
			if verify[i][j] == 1:
				permutation[i] = j
	if select == 0:
		print("The permutation after square operations is: ", permutation)
	elif select == 1:
		print("The permutation after product operations is: ", permutation)
		

	origin = copy.deepcopy(verify)
	
	seq_data_list.reverse()
	for op in seq_data_list:
		if int(op[2]) == 0:
			origin = operations.col_i2j(origin, int(op[1]), int(op[0]))
		elif int(op[2]) == 1:
			origin = operations.col_i2j(origin, int(op[1]), int(op[0]))
	
	if select == 0:
		print("The matrix after execute square operations from verify matrix is: ")
	elif select == 1:
		print("The matrix after execute product operations from verify matrix is: ")
		
	print(origin)
	
	#Comparing the origin matrix and input mat whether both are same, which means the permutation matrix can recover to input matrix
	if (origin==mat).all():
		if select == 0:
			print("The square operations are work")
		elif select == 1:
			print("The product operations are work")
			

	seq_file.close()
