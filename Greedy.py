import numpy as np
import config
import Can_depth_one
import operations
import cost_function
import sys
import random
import copy
import writers

'''
This function will execute the two kind of greedy algorithm depends on selection parameter
0: Square cost function
1: Product cost function
'''
def Greedy(mat, select):
	def Cost_Condition(select):
		if select == 0:
			return cost_function.cost_sq(mat)+cost_function.cost_sq(np.transpose(inverse)) > ((2*config.SIZE)+config.epsilon)
		elif select == 1:
			return cost_function.cost_prod(mat)+cost_function.cost_prod(inverse) > config.epsilon
		else:
			return cost_function.cost_sq(mat)+cost_function.cost_sq(np.transpose(inverse)) > ((2*config.SIZE)+config.epsilon)

	minm = config.minm
	#copy the current matrix from input
	origin = copy.deepcopy(mat) #which is B describe in paper
	#compute the inverse of current matrix
	inverse = operations.inv(mat)

	print("The inverse of loaded block data: ")
	print(inverse)
	
	depth = 0 #depth counting for d <-- 0
	#assign a huge number that used float point maximum number which is 1.7976931348623157e+308 we think it is enough
	minm_cost = sys.float_info.max
	
	#Predefine the operator and lists
	row_visi = [0]*config.SIZE
	col_visi = [0]*config.SIZE
	select_list = []
	layer_r = []
	layer_c = []
	layers_r = []
	layers_c = []
	row_op = []
	col_op = []
	
	one = False #can_one first setting to False
	
	#According to the paper the greedy algorithm will limited for double SIZE
	while Cost_Condition(select):
		#clear the select list for each time
		select_list.clear()

		#compare the H_{sqr} and H_{sqc} to find the maximum cost
		if select == 0:
			minm_cost = max(cost_function.cost_sq(mat)+cost_function.cost_sq(np.transpose(inverse)), cost_function.cost_sq(np.transpose(mat))+cost_function.cost_sq(inverse))
		elif select == 1:
			minm_cost = cost_function.cost_prod(mat)+cost_function.cost_prod(inverse)

		#check the can_one
		if not one:
			#go through the matrix and execute the column operation under not can_one
			for i in range(config.SIZE):
				if row_visi[i] == 1: #find any control exist
					continue
				for j in range(config.SIZE): #find any target exist
					#check the target exist or in the diagonal index
					if row_visi[j] == 1 or j == i:
						continue
					#execute the column operation from col_visi
					tmp_mat = operations.row_i2j(mat, i, j)
					tmp_inverse = operations.col_i2j(inverse, j, i) #calculate the row operation on inverse
					if select == 0:
						tmp_cost = cost_function.cost_sq(tmp_mat)+cost_function.cost_sq(np.transpose(tmp_inverse)) #re-calculate the cost function for H_{sqc}
					elif select == 1:
						tmp_cost = cost_function.cost_prod(tmp_mat) + cost_function.cost_prod(tmp_inverse)

					#The new one cost should reduced over the epsilon range
					if tmp_cost < minm_cost+config.epsilon:
						if tmp_cost < minm_cost-config.epsilon:
							select_list.clear() #clear the select_list and push the available operator
							operator = (i, j, 0) #in this choose is column operator so that record the 1
							select_list.append(operator) #append this operator to select_list as available operator
							minm_cost = tmp_cost #redueced success so that update the minm_cost
						else:
							operator = (i, j, 0) #otherwise just push the operator 1
							select_list.append(operator) #then append to the select_list
		
		for i in range(config.SIZE):
			if col_visi[i] == 1: #check the has any row operator exist in recently
				continue
			for j in range(config.SIZE):
				if col_visi[j] == 1 or j == i: #if identity operator exist in recently
					continue
				tmp_mat = operations.col_i2j(mat, i, j) #execute the row operation on normal matrix
				tmp_inverse = operations.row_i2j(inverse, j, i) #execute the column operation on inverse matrix
				if select == 0:
					tmp_cost = cost_function.cost_sq(np.transpose(tmp_mat))+cost_function.cost_sq(tmp_inverse) #re-calculate the square cost function
				elif select == 1:
					tmp_cost = cost_function.cost_prod(tmp_mat) + cost_function.cost_prod(tmp_inverse)

				#The new cost should over the epsilon range
				if tmp_cost < minm_cost+config.epsilon:
					if tmp_cost < minm_cost-config.epsilon:
						select_list.clear() #clear the select list
						operator = (i, j, 1) #the row operation record the 0 according to the paper setting
						select_list.append(operator) #append to the select list
						minm_cost = tmp_cost #update the new cost
					else:
						operator = (i, j, 1) #otherwise just record the row operation for 0
						select_list.append(operator) #then append to the select list
		
		if len(select_list) == 0: #every time check the select list is empty
			if len(layer_r)>0: #if layer r L_{r} has available operator
				print("The layer_r when select list is empty: ", layer_r)
				layers_r.append(layer_r[:]) #append the available to the layers r
				layer_r.clear() #then clear the L_{r} each time
				print("The layers_r in while: ", layers_r)
				row_visi = [0]*config.SIZE #also clear possible row operations
			if len(layer_c)>0: #if layer c L_{c} has available operation
				print("The layer_c when select list is empty: ", layer_c)
				layers_c.append(layer_c[:]) #append it to layers c
				layer_c.clear() #clear L_{c} for parallel
				print("The layers_c in while: ", layers_c)
				col_visi = [0]*config.SIZE #also clear the possible column operation
			if select == 0:
				if Can_depth_one.can_one(mat): #check whether currently matrix whether use one operation can achieve identity
					one = True
		else: #otherwise no available operator exist then
			rand = random.randint(0, len(select_list)-1) #setting a random seed
			select_operator = select_list[rand] #for find the randomly operations on the select list
			print("The random pick", rand, "is: ", select_operator)
			
			if select_operator[2] == 0: #pick operation is row 
				mat = operations.row_i2j(mat, select_operator[0], select_operator[1]) #then execute the row operation
				inverse = operations.col_i2j(inverse, select_operator[1], select_operator[0]) #then inverse calculate select column
				layer_r.append((select_operator[0], select_operator[1], 0)) #append this opertion to layer r L_{r}
				row_op.append((select_operator[0], select_operator[1], 0)) #also record for the row operation list
				if all(x == 0 for x in row_visi): #if currently doesn't any row operation on the row visi list
					depth += 1 #then this is available operation and new one depth
				row_visi[select_operator[0]] = 1 #the control setting 1
				row_visi[select_operator[1]] = 1 #the target setting 1
			else:
				mat = operations.col_i2j(mat, select_operator[0], select_operator[1]) #otherwise pick the column operation for matrix
				inverse = operations.row_i2j(inverse, select_operator[1], select_operator[0]) #and inverse execute the row operation
				layer_c.append((select_operator[0], select_operator[1], 1)) #append the operation as 1 to L_{c}
				col_op.append((select_operator[0], select_operator[1], 1)) #record the column operation on col op list
				if all(x ==0 for x in col_visi): #if doesn't exist any column operation on col visi list
					depth += 1 #then depth add
				col_visi[select_operator[0]] = 1 #on the col visi list record the control to 1
				col_visi[select_operator[1]] = 1 #also record 1 for target

		if depth > config._maximum_depth: #one of limit in paper is depth over 100 is bad performance and is not a valued reference
			print("Depth too large") #then just show this matrix after reduced became too large
			print(mat) #and show the matrix for user
			break #finally break this while
	
	if len(layer_r)>0: #after record the
		print("The layer_r: ", layer_r)
		layers_r.append(layer_r[:])
		layer_r.clear()
		print("The layers_r in the check out while in the layer_r has reamin: ", layers_r)
		row_visi = [0]*config.SIZE

	if len(layer_c)>0:
		print("The layer_c: ", layer_c)
		layers_c.append(layer_c[:])
		layer_c.clear()
		print("The layers_c in the check out while in the layer_c has reamin: ", layers_c)
		col_visi = [0]*config.SIZE

	reducedMat = copy.deepcopy(origin)
	size = 0
	for row_operator in row_op:
		reducedMat = operations.row_i2j(reducedMat, row_operator[0], row_operator[1])
		size += 1
	for col_operator in col_op:
		reducedMat = operations.col_i2j(reducedMat, col_operator[0], col_operator[1])
		size += 1

	reduced = True
	if ((reducedMat != mat).all()):
		reduced = False

	if (depth > minm or (depth == minm and size >= size_minm) or not reduced):
		return
	
	minm = depth
	size_minm = size
	if select == 0:
		print(str(config.SIZE) + "-block size for Square Cost that the depth is: ", minm, " and size is: ", size_minm)
	elif select == 1:
		print(str(config.SIZE) + "-block size for Product Cost that the depth is: ", minm, " and size is: ", size_minm)
	
	permutationMatrix = [0]*config.SIZE

	for i in range(config.SIZE):
		for j in range(config.SIZE):
			if mat[i][j] == 1:
				permutationMatrix[i] = j

	print("The permutation matrix: ")
	print(permutationMatrix)
	
	sequence = [] #store the operations
	layers = [] #store each depth and operations

	for i in col_op:
		col_operator_seq = i
		sequence.append((col_operator_seq[1], col_operator_seq[0], 1))#append the column operaitons
	
	for row_operator_seq in reversed(row_op):
		i = row_operator_seq
		sequence.append((permutationMatrix[i[0]], permutationMatrix[i[1]], 0))#store the row operations from permutation matrix
	
	for lay_c in layers_c:
		nl_c = []
		for l_c in lay_c:
			nl_c.append((l_c[0], l_c[1], 1))
		if nl_c:
			layers.append(nl_c)

	print("Column layers processed: ", layers)

	layers_r.reverse()
	
	for lay_r in layers_r:
		nl_r = []
		for l_r in lay_r:
			nl_r.append((permutationMatrix[l_r[0]], permutationMatrix[l_r[1]], 0))
		if nl_r:
			layers.append(nl_r)

	print("All layers processed:", layers)
	
	#write the results
	writers.Recording(sequence, layers, select)	
