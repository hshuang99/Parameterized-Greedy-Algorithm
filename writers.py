import config
def Recording(sequence, layers, type):
    if type == 0:
        #Open a file that Layers and sequences with SIZE for square cost function to store the operations
        layer_file = config.row_Sq_Layer_File
        seq_file = config.row_Sq_Seq_File
    elif type == 1:
        #Open a file that Layers and sequences with SIZE for square cost function to store the operations
        layer_file = config.col_Sq_Layer_File
        seq_file = config.col_Sq_Seq_File
    if type == 2:
        #Open a file that Layers and sequences with SIZE for square cost function to store the operations
        layer_file = config.localminima_Sq_Layer_File
        seq_file = config.localminima_Sq_Seq_File
    if type == 3:
        #Open a file that Layers and sequences with SIZE for square cost function to store the operations
        layer_file = config.parallel_Sq_Layer_File
        seq_file = config.parallel_Sq_Seq_File
    #store the operaiton sequences and store the amounts of CNOT and length of sequence
    with open(layer_file, "a") as f:
        for l in layers:
            for lay in l:
                f.write("%d %d " % (lay[0], lay[1]))
            f.write("\n")
        f.write("CNOT: %d, depth: %d\n" % (len(sequence), len(layers)))
    f.close()
    #store the operations from sequence
    with open(seq_file, "a") as f:
        for i in sequence:
            f.write("%d %d %d\n" % (i[0], i[1], i[2]))
        f.write("CNOT: %d\n" % (len(sequence)))
    f.close()
