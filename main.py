import sys
from substitute import *
from encrypt import *
import BitVector

[S_table,inv_S_table] = getTables()

input_stream = [121,232,0,45]  #Input stream with 8 bits(1 byte) at a time

encrypt_stream(input_stream,S_table)
