from BitVector import *
import numpy as np

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
    return ans

# def get_inv_mat(mat):
#     for i in range(2):
#         for j in range(2):
#             mat[i][j] =

def encrypt_stream(inp_stream,S_table):
    print("Length of input stream bits:",8*len(inp_stream))
    encrypted_stream = []
    for i in range(len(inp_stream)%4):
        inp_stream.append(0)  #Padding of 0 to make divisible by 32

    index = 0
    while(index<len(inp_stream)):
        i = index
        inp_mat = [[inp_stream[i],inp_stream[i+2]],[inp_stream[i+1],inp_stream[i+3]]]
        sub_mat = np.copy(inp_mat)

        #Substitution step
        for j in range(2):
            for k in range(2):
                inp_byte = inp_mat[j][k]
                # print(type(inp_byte))
                # print(type(S_table))
                sub_mat[j][k] = S_table[inp_byte]
                # print(S_table[inp_byte])

        inp_mat = sub_mat

        print("After Substitution: ",inp_mat)

        #Converting byte level matrix to 2-bit level matrix
        mat2bit = np.zeros((4,4))
        for i in range(2):
            for j in range(2):
                byt = inp_mat[i][j]
                col = 2*i + j
                mat2bit[0][col] = int(byt/64)
                byt = byt % 64
                mat2bit[1][col] = int(byt/16)
                byt = byt%16
                mat2bit[2][col] = int(byt/4)
                byt = byt%4
                mat2bit[3][col] = int(byt)

        print("After 2-bit conversion: ",mat2bit)

        inp_mat = mat2bit.astype(int)

        #Shift Rows step. Our is a 32 bit scheme So format is [[s00,s01],[s10,s11]]. Hence, we only interchange the last row.
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
        inp_mat = matmul(inp_mat,mult_mat)

        print("After Column Mix: ",inp_mat)

        inv = [[14,11,13,9],[9,14,11,13],[13,9,14,11],[11,13,9,14]]
        out_mat = matmul(inp_mat,inv)

        print("Possible inveser: ",out_mat)

        index = index + 4
