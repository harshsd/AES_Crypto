import sys
from substitute import *
from encrypt import *
from key_expansion import *
import BitVector
import numpy as np

def convert(s):
    new = ""
    # traverse in the string
    for x in s:
        new += x
    # return string
    return new

[S_table,inv_S_table] = getTables()

Key =[np.random.randint(2**32) for x in range(4)]
num_rounds = 4

key_stream = expand_key(Key,num_rounds,S_table)

print("Key stream is: ",key_stream)

input_stream = [np.random.randint(128) for x in range(32)]  #Input stream with 8 bits(1 byte) at a time
input_string = "Old, but I am not that old. Young, but I am not that bold."
input_stream = [ord(input_string[i]) for i in range(len(input_string))]
print("Input Stream is: ",input_stream)


encrypt_stream = encrypt_stream(input_stream,S_table,num_rounds,key_stream)
encrypted_string = convert([chr(encrypt_stream[i]) for i in range(len(encrypt_stream))])

decrypt_stream = decrypt_stream(encrypt_stream,inv_S_table,num_rounds,key_stream)
decrypted_string = convert([chr(decrypt_stream[i]) for i in range(len(decrypt_stream))])

print("------------------Results---------------------------")

print("Input Stream is: ",input_stream)
print("Encrypted Stream is: ",encrypt_stream)
print("Decrpyted Stream is: ",decrypt_stream)

print("-------------------Result in String Format---------------------")

print("Input String is: ",input_string)
print("Encrypted String is: ",encrypted_string)
print("Decrypted String is: ",decrypted_string)

assert input_stream==decrypt_stream
