import sys
from substitute import *
from encrypt import *
from key_expansion import *
import BitVector
import numpy as np

[S_table,inv_S_table] = getTables()

Key =[np.random.randint(2**32) for x in range(4)]
num_rounds = 4

key_stream = expand_key(Key,num_rounds,S_table)

print(key_stream)

input_stream = [np.random.randint(128) for x in range(16)]  #Input stream with 8 bits(1 byte) at a time
print(input_stream)


encrypt_stream = encrypt_stream(input_stream,S_table,num_rounds,key_stream)

decrypt_stream = decrypt_stream(input_stream,inv_S_table,num_rounds,key_stream)

print(input_stream)
print(decrypt_stream)
