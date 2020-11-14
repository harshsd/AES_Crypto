from BitVector import *
import numpy as np

        # #Converting byte level matrix to 2-bit level matrix
        # mat2bit = np.zeros((4,4))
        # for i in range(2):
        #     for j in range(2):
        #         byt = inp_mat[i][j]
        #         col = 2*i + j
        #         mat2bit[0][col] = int(byt/64)
        #         byt = byt % 64
        #         mat2bit[1][col] = int(byt/16)
        #         byt = byt%16
        #         mat2bit[2][col] = int(byt/4)
        #         byt = byt%4
        #         mat2bit[3][col] = int(byt)

        # print("After 2-bit conversion: ",mat2bit)

        # inp_mat = mat2bit.astype(int)

def matmul(a,b):
    assert len(a)==len(b)
    ans = []
    modulus = BitVector(bitstring='100011011') # AES modulus
    for i in range(len(a)):
        row = []
        for j in range(len(a[0])):
            sum = 0
            for k in range(len(a)):
                a1 = BitVector(intVal= a[i][k],size=8)
                b1 = BitVector(intVal =b[k][j],size=8)
                sum = sum ^ (int(a1.gf_multiply_modular(b1, modulus, 8)))
            row.append(sum)
        ans.append(row)
    return np.array(ans).astype(int)


def get4b4(input_stream,index):
    mat = np.zeros((4,4))
    for i in range(4):
        for j in range(4):
            mat[i][j]=input_stream[index+i+4*j]
    return mat.astype(int)

def add_round_key(inp_mat,four_keys):
    q1 = 2**24
    q2 = 2**16
    q3 = 2**8
    byte = np.zeros((4)).astype(int)
    for j in range(4):
        kkey = four_keys[j]
        byte[0] = int(kkey/q1)
        kkey = kkey%(q1)
        byte[1] = int(kkey/q2)
        kkey = kkey % (q2)
        byte[2] = int(kkey / (q3))
        byte[3] = kkey % (q3)
        for i in range(4):
            inp_mat[i][j] = inp_mat[i][j] ^ byte[i]
    return inp_mat


def encrypt_stream(inp_stream,S_table,num_rounds,key_stream):
    print("********************Encrypting***************************************")
    print("Length of input stream bits:",8*len(inp_stream))
    encrypted_stream = []
    # padding_req = (8*len(inp_stream)) % 128
    while ((8*len(inp_stream))%128 != 0):
        inp_stream.append(0)  #Padding of 0 to make divisible by 128
    print("Length of input stream bits:",8*len(inp_stream))

    assert len(key_stream)==4*(num_rounds+1)

    index = 0
    while(index<len(inp_stream)):
        i = index
        inp_mat = get4b4(inp_stream,index)
        inp_mat = add_round_key(inp_mat,key_stream[0:4])
        print("After Adding original Key: ",inp_mat)
        for round in range(num_rounds):
            print("-----------------------Round "+str(round+1)+"-----------------------------")
            sub_mat = np.copy(inp_mat)

            print("Input stream in matrix format: ",inp_mat)

            #Substitution step
            for j in range(2):
                for k in range(2):
                    inp_byte = inp_mat[j][k]
                    sub_mat[j][k] = S_table[inp_byte]

            inp_mat = sub_mat

            print("After Substitution: ",inp_mat)


            #Shift Rows step.
            for i in range(1,len(inp_mat)):
                #Shift row i times to the left
                for j in range(i):
                    temp = inp_mat[i][0]
                    for k in range(len(inp_mat)-1):
                        inp_mat[i][k]=inp_mat[i][k+1]
                    inp_mat[i][k+1]=temp

            print("After Row Shift: ",inp_mat)

            #Mix Columns Step.
            mult_mat = [[2,3,1,1],[1,2,3,1],[1,1,2,3],[3,1,1,2]]
            if round<num_rounds-1:
                inp_mat = matmul(inp_mat,mult_mat)

            print("After Column Mix: ",inp_mat)

            # inv = [[14,11,13,9],[9,14,11,13],[13,9,14,11],[11,13,9,14]]
            # out_mat = matmul(inp_mat,inv)
            # print("Possible inveser: ",out_mat)

            #Key adding step (Add round Key)
            inp_mat = add_round_key(inp_mat.astype(int),key_stream[4*round+4:4*round+8])

            print("After Adding round Key: ",inp_mat)

        for j in range(4):
            for i in range(4):
                encrypted_stream.append(inp_mat[i][j])
        index = index + 16
    return encrypted_stream

def decrypt_stream(inp_stream,inv_S_table,num_rounds,key_stream):
    print("********************Decrypting***************************************")
    decrypted_stream = []
    index = 0
    while(index<len(inp_stream)):
        i = index
        inp_mat = get4b4(inp_stream,index)
        inp_mat = add_round_key(inp_mat,key_stream[4*num_rounds:4*num_rounds+4])
        print("After adding final key: ",inp_mat)
        # inp_mat = add_round_key(inp_mat,key_stream[4*inverse_round+4:4*inverse_round+8])
        for round in range(num_rounds):
            print("-----------------------Round "+str(round+1)+"-----------------------------")
            inv_round = num_rounds-1-round
            #Inverse Shift Rows step.
            for i in range(1,len(inp_mat)):
                #Shift row i times to the right
                for j in range(i):
                    temp = inp_mat[i][len(inp_mat)-1]
                    for k in range(1,len(inp_mat)):
                        l = len(inp_mat)-k
                        inp_mat[i][l]=inp_mat[i][l-1]
                    inp_mat[i][0]=temp
            print("After Row Shift: ",inp_mat)

            #Inverse Substitute Bytes step
            sub_mat = np.copy(inp_mat)
            #Substitution step
            for j in range(2):
                for k in range(2):
                    inp_byte = inp_mat[j][k]
                    sub_mat[j][k] = inv_S_table[inp_byte]

            inp_mat = sub_mat

            print("After Substitution: ",inp_mat)

            #Add round Key step
            inverse_round = num_rounds-1-round
            # inverse_round = round
            inp_mat = add_round_key(inp_mat,key_stream[4*inverse_round:4*inverse_round+4])
            print("After Adding round Key: ",inp_mat)

            #Inverse Mix Columns Step.
            mult_mat = [[14,11,13,9],[9,14,11,13],[13,9,14,11],[11,13,9,14]]
            if round<num_rounds-1:
                inp_mat = matmul(inp_mat,mult_mat)

            print("After Column Mix: ",inp_mat)

        for j in range(4):
            for i in range(4):
                decrypted_stream.append(inp_mat[i][j])
        index = index+16
    return decrypted_stream
